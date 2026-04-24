#!/usr/bin/env python3
"""
Rebuild merged PPT by using python-pptx to create a fresh presentation
with the correct slide dimensions, then copy content at XML level.
"""
import os, sys
import re
import zipfile
import shutil
import io
from lxml import etree
from copy import deepcopy

PYTHON = "/tmp/ocr_env/bin/python"

PPTS = [
    ("/home/agentuser/环博会市场观察_完整版_v19.pptx",          "Work-01 环博会市场观察"),
    ("/home/agentuser/Work-02_中国水协2026年会.pptx",           "Work-02 中国水协2026年会"),
    ("/home/agentuser/wiki/projects/work-03-hongmeng/briefing.pptx", "Work-03 华为鸿蒙水质仪表"),
    ("/home/agentuser/wiki/projects/work-04-ims/ims-ib-PSP研究_v1.pptx", "Work-04 IMS IB增长战略"),
    ("/home/agentuser/Work-05_领导力修炼.pptx",                "Work-05 领导力修炼"),
]

OUTPUT = "/home/agentuser/Work全量合集.pptx"

def get_slide_texts(z, slide_names):
    """Extract text preview from each slide."""
    results = []
    for sld_name in slide_names:
        xml = z.read(sld_name)
        texts = etree.fromstring(xml).findall(
            './/{http://schemas.openxmlformats.org/drawingml/2006/main}t'
        )
        t = ' | '.join(x.text or '' for x in texts)
        results.append(t[:80])
    return results

def opc_merge_v3(ppt_list, output_path):
    """Merge using zipfile - copy base structure then add slides."""
    
    base_path = ppt_list[0][0]
    work_dir = f"/tmp/pptx_build_{os.getpid()}"
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.makedirs(work_dir)

    # ── Step 1: extract all slides from all sources ──────────────────────────
    all_slides = []  # (ppt_path, src_sld_name, new_sld_name)
    sld_num = 1
    for ppt_path, title in ppt_list:
        with zipfile.ZipFile(ppt_path, 'r') as z:
            sld_glob = re.compile(r'^ppt/slides/slide\d+\.xml$')
            slide_names = sorted([n for n in z.namelist() if sld_glob.match(n)])
            print(f"[+] {title}: {len(slide_names)} slides")
            for sld in slide_names:
                all_slides.append((ppt_path, sld, f"ppt/slides/slide{sld_num}.xml"))
                sld_num += 1

    total = sld_num - 1
    print(f"Total: {total} slides\n")

    # ── Step 2: build merged zip in memory ───────────────────────────────────
    # Start with base structure (everything EXCEPT slides)
    merged = {}  # path -> bytes

    with zipfile.ZipFile(base_path, 'r') as zbase:
        base_names = zbase.namelist()
        slide_pat = re.compile(r'^ppt/slides/slide\d+\.xml$')
        rels_pat  = re.compile(r'^ppt/slides/_rels/slide\d+\.xml\._rels$')
        
        for name in base_names:
            if slide_pat.match(name) or rels_pat.match(name):
                continue  # skip base slides - we'll add our merged ones
            merged[name] = zbase.read(name)

    # ── Step 3: add slides from all sources ─────────────────────────────────
    rId_base = 200  # start rIds high enough to avoid conflicts
    rid_counter = rId_base

    # Track (sld_id, rId) for presentation.xml
    slide_refs = []

    for src_path, src_sld, new_sld in all_slides:
        with zipfile.ZipFile(src_path, 'r') as z:
            sld_xml = z.read(src_sld)
            # Get slide rels
            src_rels = src_sld + "._rels"
            if src_rels in z.namelist():
                sld_rels_xml = z.read(src_rels)
            else:
                sld_rels_xml = b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'

        # Remap rIds in slide XML
        # Parse rels and build rId map
        rels_root = etree.fromstring(sld_rels_xml)
        new_rels_root = etree.fromstring(
            b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'
        )
        rId_map = {}
        for rel in rels_root.findall('Relationship'):
            old_rid = rel.get('Id')
            new_rid = f"rId{rid_counter}"
            rId_map[old_rid] = new_rid
            rel.set('Id', new_rid)
            new_rels_root.append(deepcopy(rel))
            rid_counter += 1

        # Remap in slide XML
        sld_root = etree.fromstring(sld_xml)
        for elem in sld_root.iter():
            for attr in elem.attrib:
                val = elem.get(attr)
                if attr == 'r:id' and val in rId_map:
                    elem.set(attr, rId_map[val])

        new_sld_bytes = etree.tostring(sld_root, xml_declaration=True, encoding='UTF-8', standalone=True)
        new_rels_bytes = etree.tostring(new_rels_root, xml_declaration=True, encoding='UTF-8', standalone=True)

        merged[new_sld] = new_sld_bytes
        merged[new_sld + "._rels"] = new_rels_bytes

        # sld_id from 256 upward
        sld_id = 256 + len(slide_refs)
        rid_counter += 1          # advance before computing rid
        rid = f"rId{rid_counter - 1}"
        slide_refs.append((str(sld_id), rid))

    # ── Step 4: write merged slides to temp dir ─────────────────────────────
    for path, data in merged.items():
        if path.endswith('/'):
            continue  # skip directory markers
        fpath = os.path.join(work_dir, path)
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        with open(fpath, 'wb') as f:
            f.write(data)

    # ── Step 5: rebuild presentation.xml ────────────────────────────────────
    with zipfile.ZipFile(base_path, 'r') as z:
        pres_xml = z.read('ppt/presentation.xml')
    pres_root = etree.fromstring(pres_xml)

    # Remove old sldIdLst and rebuild
    sldIdLst = pres_root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst')
    if sldIdLst is not None:
        for child in list(sldIdLst):
            sldIdLst.remove(child)
    else:
        # Create it if missing
        sldIdLst = etree.SubElement(
            pres_root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldMasterIdLst'),
            '{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst'
        )

    for sld_id, rid in slide_refs:
        sldId = etree.SubElement(sldIdLst, '{http://schemas.openxmlformats.org/presentationml/2006/main}sldId')
        sldId.set('id', sld_id)
        sldId.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', rid)

    with open(os.path.join(work_dir, 'ppt/presentation.xml'), 'wb') as f:
        f.write(etree.tostring(pres_root, xml_declaration=True, encoding='UTF-8', standalone=True))

    # ── Step 6: rebuild presentation.xml.rels ────────────────────────────────
    with zipfile.ZipFile(base_path, 'r') as z:
        pres_rels = z.read('ppt/_rels/presentation.xml.rels')
    pres_rels_root = etree.fromstring(pres_rels)

    # Find max rId
    max_rid = 0
    for rel in pres_rels_root.findall('Relationship'):
        m = re.search(r'\d+', rel.get('Id',''))
        if m: max_rid = max(max_rid, int(m.group()))

    # Add slide relationships starting after max_rid
    for i, (sld_id, rid) in enumerate(slide_refs):
        new_rel = etree.SubElement(pres_rels_root, 'Relationship')
        new_rel.set('Id', rid)
        new_rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
        new_rel.set('Target', f'slides/slide{i+1}.xml')

    with open(os.path.join(work_dir, 'ppt/_rels/presentation.xml.rels'), 'wb') as f:
        f.write(etree.tostring(pres_rels_root, xml_declaration=True, encoding='UTF-8', standalone=True))

    # ── Step 7: rebuild [Content_Types].xml ──────────────────────────────────
    ct_items = sorted([p for p in merged.keys() if 'slides/slide' in p and p.endswith('.xml')])
    ct_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
<Default Extension="png" ContentType="image/png"/>
<Default Extension="gif" ContentType="image/gif"/>
'''
    for p in ct_items:
        ct_xml += f'<Override PartName="/{p}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
    ct_xml += '</Types>'

    with open(os.path.join(work_dir, '[Content_Types].xml'), 'wb') as f:
        f.write(ct_xml.encode('utf-8'))

    # ── Step 8: write final zip ──────────────────────────────────────────────
    if os.path.exists(output_path):
        os.remove(output_path)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for path, data in sorted(merged.items()):
            zout.writestr(path, data)

    # Overwrite with rebuilt files
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(work_dir):
            for fname in files:
                fpath = os.path.join(root, fname)
                arcname = os.path.relpath(fpath, work_dir)
                zout.write(fpath, arcname)

    size = os.path.getsize(output_path)
    print(f"\n✅ Saved: {output_path}")
    print(f"   {total} slides | {size/1024:.1f} KB")

def main():
    opc_merge_v3(PPTS, OUTPUT)

if __name__ == "__main__":
    main()
