#!/usr/bin/env python3
"""Merge all 5 Work PPTs into one presentation in order."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from copy import deepcopy

PYTHON = "/tmp/ocr_env/bin/python"

PPTS = [
    ("/home/agentuser/环博会市场观察_完整版_v19.pptx", "Work-01 环博会市场观察"),
    ("/home/agentuser/Work-02_中国水协2026年会.pptx", "Work-02 中国水协2026年会"),
    ("/home/agentuser/wiki/projects/work-03-hongmeng/briefing.pptx", "Work-03 华为鸿蒙水质仪表"),
    ("/home/agentuser/wiki/projects/work-04-ims/ims-ib-PSP研究_v1.pptx", "Work-04 IMS IB增长战略"),
    ("/home/agentuser/Work-05_领导力修炼.pptx", "Work-05 领导力修炼"),
]

BLUE = RGBColor(0, 126, 181)
DARK_GRAY = RGBColor(77, 77, 77)

def add_divider_slide(prs, work_title, slide_num):
    """Add a section divider slide between works."""
    slide_layout = prs.slide_layouts[0]  # Only layout available
    slide = prs.slides.add_slide(slide_layout)
    w = prs.slide_width
    h = prs.slide_height

    # Blue top bar
    from pptx.shapes.autoshape import Shape
    bar = slide.shapes.add_shape(1, 0, 0, w, Inches(0.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    # Work number
    label_num = work_title.split(" ")[0].replace("Work-", "")
    ts = slide.shapes.add_textbox(Inches(0.6), Inches(2.6), Inches(3), Inches(1))
    tf = ts.text_frame
    tf.paragraphs[0].text = label_num
    tf.paragraphs[0].font.size = Pt(80)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = BLUE
    tf.paragraphs[0].font.name = "Microsoft YaHei"

    # Work title
    title_text = " ".join(work_title.split(" ")[1:])
    ts2 = slide.shapes.add_textbox(Inches(0.6), Inches(3.7), Inches(12), Inches(1.2))
    tf2 = ts2.text_frame
    tf2.paragraphs[0].text = title_text
    tf2.paragraphs[0].font.size = Pt(36)
    tf2.paragraphs[0].font.color.rgb = DARK_GRAY
    tf2.paragraphs[0].font.name = "Microsoft YaHei"

    return slide

def clone_slide(prs, src_slide):
    """Clone src_slide into prs using XML deepcopy + rId remapping."""
    # Get source XML
    src_xml = src_slide._element
    # Deep copy XML tree
    new_xml = deepcopy(src_xml)

    # Add to slide list
    prs.slides._sldIdLst.append(new_xml)
    return prs.slides[-1]

def main():
    output_path = "/home/agentuser/Work全量合集.pptx"

    # Use first PPT as base
    base_path = PPTS[0][0]
    prs = Presentation(base_path)
    print(f"Base: {base_path} ({len(prs.slides)} slides, layouts={len(prs.slide_layouts)})")

    total = len(prs.slides)

    for i, (ppt_path, work_title) in enumerate(PPTS[1:], start=1):
        if not os.path.exists(ppt_path):
            print(f"[SKIP] Not found: {ppt_path}")
            continue

        src_prs = Presentation(ppt_path)
        print(f"\n+ {work_title}: {len(src_prs.slides)} slides from {os.path.basename(ppt_path)}")

        # Add divider
        add_divider_slide(prs, work_title, total)
        total += 1
        print(f"  + divider slide (total now: {total})")

        # Clone all slides
        for j, src_slide in enumerate(src_prs.slides):
            clone_slide(prs, src_slide)
            total += 1
        print(f"  + {len(src_prs.slides)} content slides (total now: {total})")

    print(f"\n=== Total slides: {len(prs.slides)} ===")
    prs.save(output_path)
    size = os.path.getsize(output_path)
    print(f"Saved: {output_path} ({size/1024:.1f} KB)")

if __name__ == "__main__":
    main()
