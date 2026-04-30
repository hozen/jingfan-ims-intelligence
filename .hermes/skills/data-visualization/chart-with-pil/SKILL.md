---
name: chart-with-pil
description: "Create bar charts, mekko charts, and simple data visualizations using Python PIL (Pillow) when matplotlib is unavailable. Use for PPT-ready charts with CJK font support. Python 3.11 venv at /home/agentuser/.hermes/pptx-env/ has PIL pre-installed."
---

# Chart Creation with PIL (Pillow) — No matplotlib Required

## When to Use

- Need to create bar charts, mekko charts, or simple data visualizations
- matplotlib is not available in the current Python environment
- Chart must support CJK (Chinese) text labels
- Output needs to be clean and PPT-ready (960×560px or similar)

## Python Environment

**Pre-installed venv (no download needed):**
```
/home/agentuser/.hermes/pptx-env/bin/python3.11
```
Has PIL (Pillow) pre-installed, plus python-pptx. Does NOT have matplotlib, numpy.

## CJK Font for Chinese Labels

System CJK font location (available on this system):
```
/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
```

**IMPORTANT:** DejaVuSans.ttf does NOT render Chinese characters — use WQY ZenHei for any CJK text.

```python
from PIL import Image, ImageDraw, ImageFont

def font(size, bold=False):
    try:
        return ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', size)
    except:
        # fallback to DejaVu for ASCII
        p = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        try:
            return ImageFont.truetype(p, size)
        except:
            return ImageFont.load_default()
```

## Mekko Chart Template

```python
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 560
img = Image.new('RGB', (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

# Data
segments = ['Diagnostics', 'Life Sciences', 'Biotechnology']
revenues  = [9.941, 7.334, 7.293]  # $B
growth    = [-1.5, 3.5, 11.5]       # % (positive = bar goes up, negative = down)
colors    = [(168, 200, 216), (0, 121, 179), (0, 63, 108)]  # light→dark blue

# Layout
LEFT=90; RIGHT=40; TOP=70; BOT=100
CW   = W-LEFT-RIGHT
CH   = H-TOP-BOT
BASE = H-BOT
SCALE = CH / 20.0  # 20% = full chart height

def yp(g):
    return int(BASE - g * SCALE)

# Compute bar widths (proportional to revenue)
xs = []
x = LEFT
for r in revenues:
    bw = r / sum(revenues) * CW
    xs.append((int(x), int(bw)))
    x += bw

# Grid lines
for g in range(-10, 25, 5):
    y = yp(g)
    if TOP <= y <= BASE + 30:
        draw.line([(LEFT, y), (W-RIGHT, y)], fill=(220,220,220), width=1)
        draw.text((LEFT-8, y-5), f'{g:+.0f}%' if g!=0 else '0%',
                  fill=(77,77,77), font=font(10), anchor='rt')

# Baseline
draw.line([(LEFT, yp(0)), (W-RIGHT, yp(0))], fill=(30,30,30), width=2)

# Bars
for i, ((x0, bw), g, c) in enumerate(zip(xs, growth, colors)):
    xl, xr = x0+2, x0+bw-2
    if g >= 0:
        yt = yp(g)
        draw.rectangle([xl, yt, xr, BASE], fill=c)
        draw.text(((xl+xr)//2, yt+5), f'{g:+.1f}%', fill=(255,255,255), font=font(11, True), anchor='mm')
        draw.rectangle([xl, yt, xr, yt+3], fill=(255,255,255))
    else:
        yb = yp(g)
        draw.rectangle([xl, BASE, xr, yb], fill=c)
        draw.text(((xl+xr)//2, yb-5), f'{g:+.1f}%', fill=(77,77,77), font=font(11, True), anchor='mb')
        draw.rectangle([xl, yb-3, xr, yb], fill=(255,255,255))

# Segment labels
for i, ((x0, bw), seg) in enumerate(zip(xs, segments)):
    cx = x0 + bw//2
    draw.text((cx, BASE+10), seg, fill=(30,30,30), font=font(11, True), anchor='mt')
    draw.text((cx, BASE+27), f'${revenues[i]:.1f}B', fill=(153,153,153), font=font(10), anchor='mt')

# Title (CJK)
draw.text((W//2, 18), 'Danaher 产品线：规模 vs. 增速', fill=(30,30,30), font=font(15, True), anchor='mm')

# Legend
lx = W-RIGHT-5; ly = TOP+5
for j, (col, lbl) in enumerate([(colors[0],'Diagnostics'),(colors[1],'Life Sciences'),(colors[2],'Biotechnology')]):
    draw.rectangle([lx-10, ly+j*18, lx, ly+j*18+10], fill=col)
    draw.text((lx+4, ly+j*18+1), f'{lbl}  ${revenues[j]:.1f}B', fill=(77,77,77), font=font(10), anchor='lt')

img.save('/tmp/dhr_mekko.png')
```

## matplotlib Availability (for future reference)

matplotlib CAN be installed via `uv run --with matplotlib python3`, but:
- Takes ~60-90 seconds to download (large package)
- The download is NOT cached locally
- If speed matters, use PIL instead
- When matplotlib IS available:

```python
import matplotlib
matplotlib.use('Agg')  # NON-GUI backend — critical!
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Mekko via matplotlib.patches.Rectangle:
rect = mpatches.Rectangle((x, y), width, height, facecolor='color')
ax.add_patch(rect)
```

## Key Pitfalls

1. **CJK font missing**: Always use `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc` for Chinese text. Without it, Chinese characters render as empty boxes.
2. **PIL ImageDraw.line() requires int coordinates**: Always cast to `int()` — float raises `TypeError: 'float' object cannot be interpreted as an integer`.
3. **Anchor values**: PIL anchor strings are `mm` (middle-middle), `mt` (middle-top), `mb` (middle-bottom), `lt` (left-top), `rt` (right-top).
4. **Y-axis flip**: PIL draws top-down (y=0 at top), but charts usually have y=0 at baseline. Compute: `y_pixel = H - baseline_y_px + offset`.
5. **SEC blocking**: For SEC filings, do NOT use browser tools — use direct urllib HTTP calls with a proper User-Agent header.

## Output Format

- Save as PNG: `img.save('/tmp/output.png')` — PIL lossless, fast
- Recommended resolution: 960×560px at 150 DPI = good for PPT insertion
- Font sizes: title=15-16, labels=11, axis=9-10
