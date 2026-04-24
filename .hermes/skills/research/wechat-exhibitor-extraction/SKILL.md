---
name: wechat-exhibitor-extraction
description: Extract exhibitor data from WeChat public account article images using tesseract OCR when vision_analyze fails
---

# WeChat Exhibitor List Extraction

## Problem
Extract exhibitor names and booth numbers from WeChat public account article images (环保圈公众号 about 2026 Environmental Expo). The vision_analyze tool consistently refuses to process local files.

## Environment
- **tesseract OCR**: `/usr/bin/tesseract` (v5.3.4, leptonica-1.82.0)
- **Chinese language data**: `tesseract-ocr-chi-sim` already installed
- **Python venv with pytesseract**: `/tmp/ocr_env/bin/python`
- **Camoufox browser**: `/home/agentuser/.cache/camoufox/camoufox` (Firefox binary)
- **WeChat article images**: Use mmbiz.qpic.cn URLs, download via `curl -L -H "User-Agent: Mozilla/5.0" -H "Referer: https://mp.weixin.qq.com/"`

## Workflow

### Step 1: Get WeChat Article Images
```bash
# Fetch WeChat article HTML
curl -s -L --max-time 30 \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
  -H 'Referer: https://mp.weixin.qq.com/' \
  'https://mp.weixin.qq.com/s/ARTICLE_ID' > article.html

# Extract image URLs from HTML
grep -oP 'https://mmbiz\.qpic\.cn/[^"'\''>\s]+' article.html | sort -u

# Download images (sz_mmbiz_jpg domain works, mmbiz_jpg may return 0 bytes)
curl -s -L --max-time 30 -o image.jpg \
  -H 'User-Agent: Mozilla/5.0' \
  -H 'Referer: https://mp.weixin.qq.com/' \
  'https://mmbiz.qpic.cn/sz_mmbiz_jpg/IMAGE_ID/1280?wx_fmt=jpeg'
```

### Step 2: OCR with tesseract (RECOMMENDED)
```bash
# Direct tesseract - FASTER than Python wrapper
# Use chi_sim+eng (not just chi_sim) to also catch English booth codes like E1-A01
tesseract /path/to/image.jpg stdout -l chi_sim+eng 2>/dev/null

# PSM flag not needed for clean exhibition list images; omit for simplicity
# No preprocessing required for clean JPEG photos from WeChat (tested: 1.8MB JPEG worked directly)
```

# Or with Python venv
source /tmp/ocr_env/bin/activate
python -c "
from PIL import Image
import pytesseract
img = Image.open('/path/to/image.jpg')
text = pytesseract.image_to_string(img, lang='chi_sim', config='--psm 6')
print(text)
"
```

### Step 3: Parse Exhibitor Data
Extract company name + booth number pairs using regex:
```python
import re
lines = text.split('\n')
for line in lines:
    booth_match = re.search(r'(E\d)[- ]([A-Z0-9]+(?:\/[A-Z0-9]+)?)', line)
    if booth_match:
        hall = booth_match.group(1)
        booth = booth_match.group(2)
        name = line[:booth_match.start()].strip()
        # Clean name...
```

## Key Findings
- **vision_analyze REFUSES all local files** - even when given absolute paths to /home/agentuser/.hermes/image_cache/, it says "I don't see the image". Use tesseract instead.
- **tesseract is pre-installed system-wide** at `/usr/bin/tesseract` (v5.3.4). No Python wrapper needed.
- **Use `chi_sim+eng` not `chi_sim`** - exhibition lists contain both Chinese company names and English booth codes (e.g. E1-A01, E3-C12); `chi_sim` alone misses the English parts.
- **No preprocessing needed** - clean WeChat JPEG photos (even 1.8MB) work directly with tesseract. PSM flags usually unnecessary.
- **OCR speed**: ~77 exhibitors in under 3 seconds.
- **WeChat image downloads**: sz_mmbiz_jpg domain works, plain mmbiz_jpg often fails (0 bytes).

## WeChat Article Sources for 2026环博会
- 环保圈公众号文章 (public account: 环保圈, article about exhibitor lists)
- Article URL: `https://mp.weixin.qq.com/s/S5pOYhc94nIzEy1I4Et0Zw`
- Article contains E1-E6 hall maps and exhibitor lists as embedded images

## Fallback
If tesseract fails, try:
1. Resize image: `convert input.jpg -resize 800x -quality 75 output.jpg`
2. Increase contrast: `convert input.jpg -normalize -contrast-stretch 2x2 output.jpg`
3. Use `--psm 4` or `--psm 6` for different layout modes
