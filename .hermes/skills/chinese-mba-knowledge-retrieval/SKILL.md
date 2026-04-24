---
name: chinese-mba-knowledge-retrieval
description: Search authoritative Chinese business/management knowledge sites for frameworks, theories, and models instead of relying on search engines.
category: research
---

# Chinese MBA Knowledge Retrieval

## When to Use
- Searching for well-documented business/management frameworks in Chinese
- Management theories, leadership models, strategic frameworks
- First confirmed source: MBA智库百科 (wiki.mbalib.com)

## Approach
**DO**: Go directly to authoritative Chinese knowledge sites instead of relying on search engines.
**DON'T**: Trust Bing/Google search results for Chinese management terminology — results are often polluted or empty.

## Confirmed Sources
- `https://wiki.mbalib.com/wiki/[Chinese_term]` — MBA智库百科, reliable for management frameworks

## HTML Parsing Pattern (Python)
```python
import requests, re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}
url = 'https://wiki.mbalib.com/wiki/[term]'
r = requests.get(url, headers=headers, timeout=15)
r.encoding = 'utf-8'

# Extract text from <p> tags — most reliable for MBA智库 article body
paras = re.findall(r'<p[^>]*>(.*?)</p>', r.text, re.DOTALL | re.IGNORECASE)
for p in paras:
    p_clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(p_clean) > 50:
        print(p_clean[:300])
        print('---')
```

**Known noise**: MBA智库页面有时包含站点级的"编辑评论"（如重复的"第一阶段"修正注释），表现为与文章内容无关的段落混在其中。特征是重复出现且内容自相矛盾。过滤方法：保留长度>50字、与主题关键词相关的段落；剔除明显矛盾或重复的条目。

## Topics Already Researched
- 情景领导力 / Situational Leadership (Hersey & Blanchard) — 2026-04-21，完整R1-R4/S1-S4框架+批评+案例

## Notes
- Bing search for Chinese management terms often returns noise (unrelated content, Baidu知道, etc.)
- MBA智库百科 is authoritative and well-indexed — direct URL access works reliably
- Regex on `<p>` tags extracts article body content more cleanly than full-page text extraction
