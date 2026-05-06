---
name: pdf-text-extraction
description: Extract text from PDF files when common tools (pdftotext, ghostscript, ImageMagick, pymupdf) are unavailable on this server.
version: 1.0.0
author: Hermes
tags: [pdf, extraction, python]
metadata:
  hermes:
    tags: [pdf, text-extraction]
prerequisites:
  python_modules: [pypdf]
---

# PDF Text Extraction

Extract text from PDF files when common tools (pdftotext, ghostscript, ImageMagick, pymupdf) are unavailable.

## Environment

This server has **pypdf** available. Use it first.

```python
from pypdf import PdfReader

reader = PdfReader("/path/to/file.pdf")
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text and text.strip():
        print(f"=== Page {i+1} ===")
        print(text[:3000])
```

## What Doesn't Work Here

| Tool | Status |
|------|--------|
| `pdftotext` | Not installed |
| `ghostscript` | Not installed |
| `ImageMagick convert` | Not installed |
| `pymupdf` (fitz) | Not installed |
| `pdfminer` | Not installed |
| `tesseract` | Installed but for OCR, not text extraction |
| `pypdf` | ✅ Available |

## If pypdf Fails

Try installing via pip (may timeout on this server):
```bash
pip install --break-system-packages pymupdf
```

Or try browser screenshot + OCR as last resort.

## PDF vs PPTX

If a file is named `.pdf` but is actually a PPTX (renamed), try:
```python
import zipfile
with open(path, 'rb') as f:
    magic = f.read(8)
print(magic.hex())  # PDF starts with 255044462d312e37 (i.e. %PDF-)
print(magic.startswith(b'%PDF'))

import zipfile
with zipfile.ZipFile(path, 'r') as z:
    print(z.namelist()[:10])
```

## PDF Generation from HTML

Use Chrome headless to convert HTML to PDF:
```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=/tmp/output.pdf --print-to-pdf-no-header /tmp/input.html
```
