#!/usr/bin/env python3
"""
Rebuild merged PPT by re-creating each slide from source PPT content.
python-pptx can't directly clone slides across presentations with different layouts,
so we copy text/shapes by reading XML and re-adding them.
"""
import os
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from copy import deepcopy
import zipfile
from lxml import etree

PPTS = [
    ("/home/agentuser/环博会市场观察_完整版_v19.pptx",          "Work-01 环博会市场观察"),
    ("/home/agentuser/Work-02_中国水协2026年会.pptx",           "Work-02 中国水协2026年会"),
    ("/home/agentuser/wiki/projects/work-03-hongmeng/briefing.pptx", "Work-03 华为鸿蒙水质仪表"),
    ("/home/agentuser/wiki/projects/work-04-ims/ims-ib-PSP研究_v1.pptx", "Work-04 IMS IB增长战略"),
    ("/home/agentuser/Work-05_领导力修炼.pptx",                "Work-05 领导力修炼"),
]

BLUE = RGBColor(0, 126, 181)
DARK_GRAY = RGBColor(77, 77, 77)

def get_slide_texts(pptx_path):
    """Extract all text from each slide in a pptx."""
    texts_by_slide = []
    with zipfile.ZipFile(pptx_path, 'r') as z:
        slide_files = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)])
        for sld_file in slide_files:
            xml = z.read(sld_file)
            root = etree.fromstring(xml)
            # Extract all text
            ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            text_elements = root.findall('.//a:t', ns)
            texts = [t.text or '' for t in text_elements]
            texts_by_slide.append('\n'.join(texts))
    return texts_by_slide

def check_all_sources():
    """Verify all PPTs are readable and have content."""
    for path, title in PPTS:
        if not os.path.exists(path):
            print(f"[MISSING] {title}: {path}")
            continue
        texts = get_slide_texts(path)
        print(f"[OK] {title}: {len(texts)} slides")
        for i, t in enumerate(texts):
            preview = t[:60].replace('\n', ' | ')
            print(f"     [{i+1}] {preview}")

def main():
    print("=== Checking all source PPTs ===\n")
    check_all_sources()

if __name__ == "__main__":
    main()
