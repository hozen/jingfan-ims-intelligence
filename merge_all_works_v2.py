#!/usr/bin/env python3
"""Merge PPTs using zipfile OPC-level manipulation — preserves all content."""
import os
import zipfile
import shutil
import re
from copy import deepcopy
from lxml import etree

PPTS = [
    ("/home/agentuser/环博会市场观察_完整版_v19.pptx",          "Work-01 环博会市场观察"),
    ("/home/agentuser/Work-02_中国水协2026年会.pptx",           "Work-02 中国水协2026年会"),
    ("/home/agentuser/wiki/projects/work-03-hongmeng/briefing.pptx", "Work-03 华为鸿蒙水质仪表"),
    ("/home/agentuser/wiki/projects/work-04-ims/ims-ib-PSP研究_v1.pptx", "Work-04 IMS IB增长战略"),
    ("/home/agentuser/Work-05_领导力修炼.pptx",                "Work-05 领导力修炼"),
]

OUTPUT = "/home/agentuser/Work全量合集.pptx"
TMPDIR = "/tmp/pptx_merge"
TARGET_SLIDE_COUNT = "ppt/slides/_rels/slideLayouts/_rels"

def opc_merge(ppt_files_with_titles):
    """Merge multiple PPTX files at OPC level. Returns total slide count."""
    # Clean tmp
    if os.path.exists(TMPDIR):
        shutil.rmtree(TMPDIR)
    os.makedirs(TMPDIR)

    slide_counter = 1
    all_rels = []  # list of (sld_rels_path, rels_xml_str)

    # Open each PPTX and extract slides
    for ppt_path, work_title in ppt_files_with_titles:
        print(f"\nProcessing: {work_title}")
        print(f"  File: {ppt_path}")

        if not os.path.exists(ppt_path):
            print(f"  [SKIP] Not found")
            continue

        with zipfile.ZipFile(ppt_path, 'r') as zin:
            # List slides in this pptx
            slide_names = sorted([n for n in zin.namelist() if re.match(r'ppt/slides/slide\d+\.xml', n)])
            print(f"  Slides found: {len(slide_names)}")

            for sld_name in slide_names:
                # Read slide XML
                sld_xml = zin.read(sld_name)

                # Read slide rels
                sld_rels_path = sld_name + "._rels"
                if sld_rels_path in zin.namelist():
                    sld_rels_xml = zin.read(sld_rels_path)
                else:
                    sld_rels_xml = b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>'

                # New slide name
                new_sld_name = f"ppt/slides/slide{slide_counter}.xml"
                new_sld_rels_path = f"ppt/slides/_rels/slide{slide_counter}.xml._rels"

                # Write to tmp dir
                out_sld = os.path.join(TMPDIR, f"slide{slide_counter}.xml")
                with open(out_sld, 'wb') as f:
                    f.write(sld_xml)

                out_sld_rels = os.path.join(TMPDIR, f"slide{slide_counter}.xml._rels")
                with open(out_sld_rels, 'wb') as f:
                    f.write(sld_rels_xml)

                all_rels.append((new_sld_rels_path, sld_rels_xml))
                slide_counter += 1

    return slide_counter - 1, all_rels

def build_merged_pptx(total_slides, all_rels):
    """Build merged PPTX from first PPT as base."""
    base_path = PPTS[0][0]

    # Copy base to tmp output
    out_tmp = "/tmp/pptx_merge_out"
    if os.path.exists(out_tmp):
        shutil.rmtree(out_tmp)
    shutil.copytree(TMPDIR, out_tmp)

    # Copy base pptx content (except slides)
    with zipfile.ZipFile(base_path, 'r') as zin:
        for item in zin.namelist():
            if re.match(r'ppt/slides/slide\d+\.xml', item):
                continue
            if re.match(r'ppt/slides/_rels/slide\d+\.xml\._rels', item):
                continue
            out_item = os.path.join(out_tmp, item)
            os.makedirs(os.path.dirname(out_item), exist_ok=True)
            with open(out_item, 'wb') as f:
                f.write(zin.read(item))

    # Write merged [Content_Types].xml
    ct_path = os.path.join(out_tmp, "[Content_Types].xml")
    ct_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
'''
    for i in range(1, total_slides + 1):
        ct_xml += f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
    ct_xml += '</Types>'
    with open(ct_path, 'w', encoding='utf-8') as f:
        f.write(ct_xml)

    # Write merged _rels/.rels
    rels_path = os.path.join(out_tmp, "_rels", ".rels")
    os.makedirs(os.path.dirname(rels_path), exist_ok=True)
    rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''
    with open(rels_path, 'w', encoding='utf-8') as f:
        f.write(rels_xml)

    # Write merged ppt/_rels/presentation.xml.rels
    pres_rels_dir = os.path.join(out_tmp, "ppt", "_rels")
    os.makedirs(pres_rels_dir, exist_ok=True)
    pres_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="presentation.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="slideLayouts/slideLayout1.xml"/>
'''
    for i in range(1, total_slides + 1):
        pres_rels += f'<Relationship Id="rId{i+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
    pres_rels += '</Relationships>'
    pres_rels_path = os.path.join(pres_rels_dir, "presentation.xml.rels")
    with open(pres_rels_path, 'w', encoding='utf-8') as f:
        f.write(pres_rels)

    # Write merged ppt/presentation.xml — update slide list
    pres_xml_path = os.path.join(out_tmp, "ppt", "presentation.xml")
    pres_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
  saveSubsetFonts="1">
<p:sldSz cx="12192000" cy="6858000"/>
<p:sldIdLst>
'''
    for i in range(1, total_slides + 1):
        pres_xml += f'<p:sldId id="256+i" r:id="rId{i+3}"/>\n'.replace("256+i", str(256 + i))
    pres_xml += '''</p:sldIdLst>
<p:sldMasterIdLst><p:sldMasterId r:id="rId2"/></p:sldMasterIdLst>
</p:presentation>'''
    with open(pres_xml_path, 'w', encoding='utf-8') as f:
        f.write(pres_xml)

    # Write merged ppt/slideLayouts/slideLayout1.xml from base
    with zipfile.ZipFile(base_path, 'r') as zin:
        layout_names = [n for n in zin.namelist() if 'slideLayouts/slideLayout' in n and n.endswith('.xml')]
        for ln in layout_names:
            out_ln = os.path.join(out_tmp, ln)
            os.makedirs(os.path.dirname(out_ln), exist_ok=True)
            with open(out_ln, 'wb') as f:
                f.write(zin.read(ln))
        # Also copy slideMasters
        master_names = [n for n in zin.namelist() if 'slideMasters/' in n and n.endswith('.xml')]
        for mn in master_names:
            out_mn = os.path.join(out_tmp, mn)
            os.makedirs(os.path.dirname(out_mn), exist_ok=True)
            with open(out_mn, 'wb') as f:
                f.write(zin.read(mn))
        # Copy theme
        theme_names = [n for n in zin.namelist() if 'theme/' in n and n.endswith('.xml')]
        for tn in theme_names:
            out_tn = os.path.join(out_tmp, tn)
            os.makedirs(os.path.dirname(out_tn), exist_ok=True)
            with open(out_tn, 'wb') as f:
                f.write(zin.read(tn))

    # Write new Content_Types
    ct = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
'''
    for i in range(1, total_slides + 1):
        ct += f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
    ct += '</Types>'
    with open(os.path.join(out_tmp, "[Content_Types].xml"), 'w') as f:
        f.write(ct)

    # Build final zip
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)
    with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(out_tmp):
            for file in files:
                fp = os.path.join(root, file)
                arcname = os.path.relpath(fp, out_tmp)
                zout.write(fp, arcname)

    return OUTPUT

def main():
    print("=== OPC-Level PPTX Merge ===")
    total, all_rels = opc_merge(PPTS)
    print(f"\nTotal slides extracted: {total}")

    out = build_merged_pptx(total, all_rels)
    size = os.path.getsize(out)
    print(f"\nSaved: {out}")
    print(f"Size: {size/1024:.1f} KB")

if __name__ == "__main__":
    main()
