#!/usr/bin/env python3
"""
OPC-level PPTX merger.
Copies slide XML + rels directly from each source PPTX into a new merged PPTX,
with proper rId remapping and relationship tracking.
"""
import os
import re
import zipfile
import shutil
from lxml import etree
from copy import deepcopy

PPTS = [
    ("/home/agentuser/环博会市场观察_完整版_v19.pptx",          "Work-01 环博会市场观察"),
    ("/home/agentuser/Work-02_中国水协2026年会.pptx",           "Work-02 中国水协2026年会"),
    ("/home/agentuser/wiki/projects/work-03-hongmeng/briefing.pptx", "Work-03 华为鸿蒙水质仪表"),
    ("/home/agentuser/wiki/projects/work-04-ims/ims-ib-PSP研究_v1.pptx", "Work-04 IMS IB增长战略"),
    ("/home/agentuser/Work-05_领导力修炼.pptx",                "Work-05 领导力修炼"),
]

OUTPUT = "/home/agentuser/Work全量合集.pptx"
TMPDIR = "/tmp/merged_pptx"
WORK_DIR = "/tmp/pptx_work"

NS = {
    'a':  'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r':  'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p':  'http://schemas.openxmlformats.org/presentationml/2006/main',
    'pr': 'http://schemas.openxmlformats.org/package/2006/relationships',
    'ct': 'http://schemas.openxmlformats.org/package/2006/content-types',
}

def get_text_content(sld_xml_bytes):
    """Extract all text from a slide's XML."""
    root = etree.fromstring(sld_xml_bytes)
    texts = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t')
    return [t.text or '' for t in texts]

def merge_opc(ppt_files_with_titles, output_path):
    """Merge multiple PPTXs at OPC level."""
    global WORK_DIR
    WORK_DIR = f"/tmp/pptx_work_{os.getpid()}"
    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
    os.makedirs(WORK_DIR)

    all_slides = []  # list of (ppt_path, sld_name_in_zip, sld_rels_name_in_zip)

    slide_glob = re.compile(r'^ppt/slides/slide\d+\.xml$')

    for ppt_path, title in ppt_files_with_titles:
        if not os.path.exists(ppt_path):
            print(f"[SKIP] Not found: {ppt_path}")
            continue
        with zipfile.ZipFile(ppt_path, 'r') as zin:
            sld_files = sorted([n for n in zin.namelist() if slide_glob.match(n)])
            print(f"[+] {title}: {len(sld_files)} slides from {os.path.basename(ppt_path)}")
            for sld in sld_files:
                all_slides.append((ppt_path, sld))

    print(f"\nTotal slides to merge: {len(all_slides)}")

    # --- Build merged zip ---
    if os.path.exists(output_path):
        os.remove(output_path)

    # Use first PPTX as structural template (has slideMaster, layouts, theme)
    base_pptx = ppt_files_with_titles[0][0]

    with zipfile.ZipFile(base_pptx, 'r') as zbase:
        base_names = set(zbase.namelist())

    # Get base slide IDs from presentation.xml
    with zipfile.ZipFile(base_pptx, 'r') as zbase:
        pres_xml = zbase.read('ppt/presentation.xml')
        pres_root = etree.fromstring(pres_xml)
        sldIdLst = pres_root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst')
        base_slide_ids = [sldId.get('id') for sldId in sldIdLst]
        if base_slide_ids:
            next_id = max(int(x) for x in base_slide_ids) + 1
        else:
            next_id = 256

    print(f"Base slide IDs: {base_slide_ids[:5]}..., next_id starts at {next_id}")

    # Build the merged zip in memory then write
    merged_parts = {}  # path -> bytes

    # Copy base structure (everything except slides)
    with zipfile.ZipFile(base_pptx, 'r') as zbase:
        for name in zbase.namelist():
            if slide_glob.match(name):
                continue
            if re.match(r'ppt/slides/_rels/slide\d+\.xml\._rels$', name):
                continue
            merged_parts[name] = zbase.read(name)

    # Now add slides from all sources
    sld_num = 1
    new_sld_ids = []  # (id, rId)
    rId_counter = 100

    for ppt_path, sld_name in all_slides:
        with zipfile.ZipFile(ppt_path, 'r') as zin:
            sld_xml = zin.read(sld_name)

            # Check it has content
            texts = get_text_content(sld_xml)
            preview = ' | '.join(t[:20] for t in texts if t.strip())[:80]

            # Read slide rels if exists
            sld_rels_name = sld_name + "._rels"
            if sld_rels_name in zin.namelist():
                sld_rels_xml = zin.read(sld_rels_name)
            else:
                sld_rels_xml = b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>'

        # New slide name in merged zip
        new_sld_name = f"ppt/slides/slide{sld_num}.xml"
        new_sld_rels_name = f"ppt/slides/_rels/slide{sld_num}.xml._rels"

        # Parse rels and remap
        rels_root = etree.fromstring(sld_rels_xml)
        new_rels_root = etree.fromstring(
            b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>'
        )

        rId_map = {}  # old_rId -> new_rId
        for rel in rels_root.findall('Relationship'):
            old_rId = rel.get('Id')
            new_rId = f"rId{rId_counter}"
            rId_map[old_rId] = new_rId
            rel.set('Id', new_rId)
            # Copy the Relationship element into new rels
            new_rels_root.append(deepcopy(rel))
            rId_counter += 1

        # Remap rIds in slide XML
        sld_root = etree.fromstring(sld_xml)
        for elem in sld_root.iter():
            for attr in ('id', 'r:id', 'descr'):
                val = elem.get(attr)
                if not val:
                    continue
                if attr == 'r:id' and val in rId_map:
                    elem.set(attr, rId_map[val])

        # Serialize
        new_sld_bytes = etree.tostring(sld_root, xml_declaration=True, encoding='UTF-8', standalone=True)
        new_rels_bytes = etree.tostring(new_rels_root, xml_declaration=True, encoding='UTF-8', standalone=True)

        merged_parts[new_sld_name] = new_sld_bytes
        merged_parts[new_sld_rels_name] = new_rels_bytes

        # Track for presentation.xml
        sld_id = str(next_id)
        rId = f"rId{rId_counter}"
        new_sld_ids.append((sld_id, rId))
        rId_counter += 1
        next_id += 1
        sld_num += 1

        print(f"    Slide {sld_num-1}: {preview[:70]}")

    # --- Update [Content_Types].xml ---
    ct_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    ct_xml += '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
    ct_xml += '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
    ct_xml += '<Default Extension="xml" ContentType="application/xml"/>\n'
    ct_xml += '<Default Extension="jpeg" ContentType="image/jpeg"/>\n'
    ct_xml += '<Default Extension="png" ContentType="image/png"/>\n'
    for i in range(1, sld_num):
        ct_xml += f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
    ct_xml += '</Types>'
    merged_parts['[Content_Types].xml'] = ct_xml.encode('utf-8')

    # --- Update ppt/_rels/presentation.xml.rels ---
    # Find base rId for slideMaster and layout
    with zipfile.ZipFile(base_pptx, 'r') as zbase:
        pres_rels_xml = zbase.read('ppt/_rels/presentation.xml.rels')
    pres_rels_root = etree.fromstring(pres_rels_xml)

    new_pres_rels = etree.fromstring(
        b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>'
    )
    for rel in pres_rels_root.findall('Relationship'):
        new_pres_rels.append(deepcopy(rel))

    # Find max rId in base
    max_rId_num = 0
    for rel in pres_rels_root.findall('Relationship'):
        rid = rel.get('Id')
        m = re.search(r'\d+', rid)
        if m:
            max_rId_num = max(max_rId_num, int(m.group()))

    # Add slide relationships
    for i, (sld_id, rid) in enumerate(new_sld_ids):
        # rIds from 256+i correspond to rId{prev_max + 1 + i}
        # But we need unique rIds - use sequential from max+1
        slide_rid = f"rId{max_rId_num + 1 + i}"
        rel_elem = etree.SubElement(new_pres_rels, 'Relationship')
        rel_elem.set('Id', slide_rid)
        rel_elem.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
        rel_elem.set('Target', f'slides/slide{i+1}.xml')

    new_pres_rels_bytes = etree.tostring(new_pres_rels, xml_declaration=True, encoding='UTF-8', standalone=True)
    merged_parts['ppt/_rels/presentation.xml.rels'] = new_pres_rels_bytes

    # --- Update ppt/presentation.xml sldIdLst ---
    # We need to match the rIds we assigned in presentation.xml.rels
    with zipfile.ZipFile(base_pptx, 'r') as zbase:
        pres_xml = zbase.read('ppt/presentation.xml')
    pres_root = etree.fromstring(pres_xml)
    sldIdLst = pres_root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst')

    # Clear existing sldIds (from base slides)
    for child in list(sldIdLst):
        sldIdLst.remove(child)

    for i, (sld_id, rid) in enumerate(new_sld_ids):
        slide_rid = f"rId{max_rId_num + 1 + i}"
        sldId_elem = etree.SubElement(sldIdLst, '{http://schemas.openxmlformats.org/presentationml/2006/main}sldId')
        sldId_elem.set('id', str(256 + i))
        sldId_elem.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', slide_rid)

    new_pres_bytes = etree.tostring(pres_root, xml_declaration=True, encoding='UTF-8', standalone=True)
    merged_parts['ppt/presentation.xml'] = new_pres_bytes

    # --- Write final zip ---
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in sorted(merged_parts.items()):
            zout.writestr(name, data)

    size = os.path.getsize(output_path)
    print(f"\n✅ Saved: {output_path}")
    print(f"   {sld_num-1} slides | {size/1024:.1f} KB")

def main():
    merge_opc(PPTS, OUTPUT)

if __name__ == "__main__":
    main()
