---
name: baidu-api-research-workflow
description: Research workflow using Baidu Cloud APIs for web search and document extraction. Covers bce-v3 authentication, Qianfan API endpoints, DNS resolution quirks, and ClawHub skill installation.
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [baidu, api, search, bce-v3, china, research]
---

# Baidu API Research Workflow

Use this when doing web research on Chinese sources, especially when Baidu search API access is available.

## 1. Available Tools & When to Use Each

| Tool | Use When | Limitation |
|------|----------|------------|
| **browser_navigate → cn.bing.com** | Quick web search | Results may be empty/unreliable |
| **browser_navigate → ie-expo.cn** | Official expo/event data | Often requires login for full data |
| **baidu-search skill (ClawHub)** | Live web search via Qianfan API | Requires valid Qianfan API key |
| **vision_analyze** | Image OCR/text extraction | Unreliable for dense Chinese text |
| **pymupdf** | Text extraction from PDFs | Cannot OCR images |
| **curl + BCE v3 auth** | Direct Baidu Cloud API calls | Complex signature, often fails |

## 2. Baidu Search Skill Installation (ClawHub)

```bash
# 1. Download from ClawHub
curl -s 'https://wry-manatee-359.convex.site/api/v1/download?slug=baidu-search' -o /tmp/baidu-search.zip
unzip -q /tmp/baidu-search.zip -d /tmp/baidu-search

# 2. Copy to skills directory
cp -r /tmp/baidu-search ~/.hermes/skills/baidu-search

# 3. Install dependencies
uv pip install requests --python /tmp/ocr_env/bin/python
```

**Usage:**
```bash
BAIDU_API_KEY=<your-key> /tmp/ocr_env/bin/python ~/.hermes/skills/baidu-search/scripts/search.py '{"query":"搜索内容","count":5}'
```

## 3. BCE v3 API Key Format

The key format is: `bce-v3/{AK}/{signature}`
- AK = Access Key (e.g., `ALTAK-2PWQsNGDWclsFwZxkQKI1`)
- SK = Secret Key (separate from AK)
- **IMPORTANT**: This format is for Baidu Cloud BCE authentication, NOT for direct Bearer token use

### Qianfan API Endpoints (confirmed working)
- `qianfan.baidubce.com` — resolves correctly ✅
- `search.bce.baidu.com` — does NOT resolve ❌
- `aip.baidubce.com` — resolves correctly ✅ (for OCR/token)

### Getting Access Token
```bash
# ❌ This fails with bce-v3 format keys
curl -X POST 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={AK}&client_secret={SK}'

# Error: {"error":"invalid_client"} — key format not accepted
```

### BCE v3 Signature Authentication (for Qianfan)
```python
import hmac, hashlib, datetime, json

def bce_sign_v3(ak, sk, method, host, uri, body):
    now = datetime.datetime.utcnow()
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    headers_part = f"host:{host}\ntimestamp:{timestamp}\n"
    content_len = f"content-length:{len(body)}\n"
    body_hash = hashlib.sha256(body.encode()).hexdigest()
    sts = f"bce-auth-v1/{ak}/timestamp\n{hashlib.sha256((headers_part + content_len + body_hash).encode()).hexdigest()}"
    sig = hmac.new(sk.encode(), sts.encode(), hashlib.sha256).hexdigest()
    return f"bce-auth-v1/{ak}/timestamp/{sig}", timestamp
```

**Known issue**: Qianfan API signature validation often fails with externally-provisioned bce-v3 keys. The API may require keys generated from the Qianfan console specifically.

## 4. Official Expo/Event Research Methodology

When researching Chinese trade shows (环博会, industrial expos):

1. **Official website** is primary source — often at `ie-expo.cn` or similar
   - `ie-expo.cn` = official organizer (Messe Muenchen Zhongmao 中贸慕尼黑)
   - Official exhibitor directory: `cloud.ie-expo.cn/trade-web-site3/` (may require login)
   - Official closing reports often have verified stats published 1-2 days after event

2. **Official social media** (WeChat public accounts) is main promotion channel in China
   - Search WeChat for event name + "公众号"

3. **Third-party lists** (like 828i.com/展超网, 中华会展网) are often PREDICTIONS based on previous years, NOT confirmed exhibitors
   - **ALWAYS verify**: User confirmed 828i.com had some real data but also predictions

4. **Sohu/163 articles** often publish exhibitor lists as IMAGES (not text), making OCR necessary
   - Image URLs from these articles: `q4.itc.cn` CDN

5. **HBZhan.com (环保在线)** has expo coverage but may block access

## 5. Image OCR for Chinese Exhibitor Lists

Options (in order of preference):

1. **vision_analyze** — Works for small/clear images, unreliable for dense Chinese text
2. **marker-pdf** — Best quality but requires 3-5GB (PyTorch + models)
3. **pymupdf** — Works for text-based PDFs only, NOT for images
4. **Tesseract OCR** — Not installed, requires root access to `apt-get install tesseract-ocr tesseract-ocr-chi-sim`

```bash
# Install pymupdf in venv (fast, ~25MB)
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple pymupdf --python /tmp/ocr_env/bin/python
```

## 6. Network Restrictions to Know

- **Image upload services blocked**: imgbox, file.io, uploadcare, tmpfiles — all fail
- **Baodu.com triggers CAPTCHA** in browser — use Bing or Qianfan instead
- **search.bce.baidu.com** doesn't resolve — use `qianfan.baidubce.com`
- **PyPI downloads** are very slow — always use Tsinghua mirror (`pypi.tuna.tsinghua.edu.cn`)
- **pip install timeout** at 120s — use uv with longer timeout or venv approach

## 7. Key Files & Paths

- Baidu search skill: `~/.hermes/skills/baidu-search/`
- OCR venv: `/tmp/ocr_env/bin/python`
- Downloaded images: `/tmp/exhibitor_*.jpg`
- Hermite browser: `~/.cache/camoufox/`
