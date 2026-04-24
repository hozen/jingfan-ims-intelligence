---
name: pptx-from-corporate-template
description: Create branded PPTX reports by extracting colors/layout from a corporate .pptx template, then rebuilding slides with python-pptx. Includes WeChat delivery and Chinese curly-quote pitfall.
category: productivity
tags: [pptx, python, hach, template, wechat]
---

# Creating PPTX Reports from Corporate Templates

## When to Use
Creating a branded PowerPoint report where the user provides a `.pptx` template and wants content filled in.

## Workflow

### Step 1: Extract Template Colors and Structure

```bash
# Unzip the PPTX
unzip -o 'template.pptx' -d template_extracted

# Extract color values from theme XML
cat template_extracted/ppt/theme/theme1.xml | python3 -c "
import sys, re
data = sys.stdin.read()
colors = re.findall(r'val=\"([0-9A-Fa-f]{6})\"', data)
print('Colors:', colors[:20])
"
```

### Step 2: Analyze Slide Layouts

```python
from pptx import Presentation

prs = Presentation('template.pptx')
print(f"Slide count: {len(prs.slides)}")
print(f"Slide size: {prs.slide_width.inches:.2f} x {prs.slide_height.inches:.2f}")

for i, slide in enumerate(prs.slides):
    print(f"\n=== Slide {i+1} ===")
    for shape in slide.shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text[:80].replace('\n', ' ')
            if text.strip():
                print(f"  [{shape.shape_type}] {text}")
```

### Step 3: Rebuild Slides with Content

Key functions needed:
- `clear_slide(slide)` — remove all shapes from a slide
- `add_filled_shape(slide, left, top, width, height, fill_color)` — add colored rectangle
- `add_text_box(slide, left, top, width, height, text, font_size, bold, color)` — add text

### Step 4: Python String Pitfall — Chinese Curly Quotes

**Problem**: Chinese/Unicode curly quotes `"` `"` (U+201C/U+201D) inside Python string literals cause `SyntaxError`.

**Wrong**:
```python
"含"云/平台"关键词展商"  # SyntaxError
```

**Correct**:
```python
"含数字化关键词展商（云/平台）"  # use regular quotes inside
# OR
'含"云/平台"关键词展商'  # use single quotes outside
```

Always grep for `"` or `"` in your script before running:
```bash
grep -n '"' script.py | head -20  # find curly quotes
```

### Step 5: Send via WeChat

```python
# Use MEDIA: absolute path format
send_message(target="weixin:chat_id", message="MEDIA:/path/to/file.pptx")
```

## Hach Template Specific Colors (2026)
- `44546A` — dark blue-gray (primary text/title)
- `4874CB` — bright blue (accent)
- `EE822F` — orange (accent)
- `F2BA02` — yellow (accent)
- `75BD42` — green (accent)
- `30C0B4` — teal (accent)
- `E54C5E` — red (accent/warning)
- `E7E6E6` — light gray (background)
- `FFFFFF` — white

## Template Structure (Hach 6-slide template)
- Slide 1: Instructions/cover
- Slide 2: Title slide ("此处输入幻灯片标题")
- Slide 3: Agenda/contents
- Slide 4: Section header
- Slide 5: Content page
- Slide 6: Thank you

To add more slides, clone an existing slide:
```python
from copy import deepcopy
xml = deepcopy(prs.slides._sldIdLst[-1]._element)
prs.slides._sldIdLst.append(deepcopy(xml))
```
