---
name: wechat-article-extract
description: Extract full article content from WeChat Official Accounts article pages (mp.weixin.qq.com). Handles client-side rendered content with obfuscated JS encoding.
triggers:
  - "WeChat article"
  - "微信公众号"
  - "mp.weixin.qq.com"
  - "WeChat content extraction"
  - "微信文章提取"
---

# WeChat Article Extraction

从微信公众号文章页面提取正文内容的技能。适用于无法用浏览器渲染但需要获取文章完整文字的场景（如竞争情报收集）。

## 背景

微信公众号文章使用**客户端渲染**（非SSR）。直接`curl`只能拿到HTML框架，正文内容通过JavaScript动态写入DOM。HTML中正文以**混淆编码**形式藏在某个`<script>`标签的全局变量里。

## 两种方法

### 方法1：Python脚本（推荐，用于研究/情报场景）

直接从HTML中解析出混淆内容并解码。

```python
import re

with open('/tmp/wechat_article.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 找到 cgiDataNew 所在的 script 块
pattern = r'var\s+cgiDataNew\s*=\s*\{.*?\};'
match = re.search(pattern, html, re.DOTALL)
if not match:
    # 也可能是其他变量名，如 cgiData, bizData 等
    match = re.search(r'var\s+\w+Data\w*\s*=\s*\{', html)

print(match.group(0)[:500])
```

**实际有效方法（已验证）**：正文内容在 `id="js_content"` 的div里。直接正则提取即可：

```python
import re

with open('/tmp/wechat_article.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 方法1：直接提取 js_content div（成功率最高）
m = re.search(r'id="js_content"[^>]*>(.*?)(?=<div[^>]*id="js_preview"|$)', html, re.DOTALL)
if m:
    content = re.sub(r'<[^>]+>', ' ', m.group(1))
    content = re.sub(r'\s+', ' ', content).strip()
    print(f"Content length: {len(content)}")

# 方法2：如果方法1失败，尝试 rich_media_content
if not m or len(content) < 1000:
    m = re.search(r'class="rich_media_content"[^>]*>(.*?)(?=<script|\Z)', html, re.DOTALL)

# 方法3：最后尝试 img-content
if not m or len(content) < 1000:
    m = re.search(r'id="img-content"[^>]*>(.*?)(?=<script|\Z)', html, re.DOTALL)
```

**验证**：提取后搜索关键词（如"设备订单"）确认内容存在。

### 方法2：浏览器截图（用于视觉验证）

当解析失败时，用 `browser_vision` 截图是最可靠的方式：

```python
from camoufox.sync_api import Camoufox

browser = Camoufox(headless=True).start()
page = browser.new_page()
page.goto('https://mp.weixin.qq.com/s/xxxx')
page.wait_for_timeout(3000)  # 等待JS渲染
screenshot = page.screenshot()
browser.close()
```

## 已知陷阱

1. **WeChat CDN图片无法直接获取** — 公众号图片有referrer限制，curl会被拦截
2. **发布时间/作者信息在文章外部** — 单独从文章正文提取会丢失，需从页面meta或标题区获取
3. **长文章分页** — 有些文章有分页，需处理
4. **特殊字符** — 编码可能包含`\uXXXX`形式的unicode转义
5. **中文Windows文件名的curl下载** — 使用`--output`指定输出路径，避免编码问题

## 验证步骤

1. 提取后检查是否包含中文（确认不是纯HTML框架）
2. 检查文章长度是否合理（太短说明提取失败）
3. 对比标题和首段是否匹配

## 应用场景

- 竞品情报：竞品公众号文章 → 提取内容 → 存档分析
- 行业研究：展会/论坛发布的微信文章
- 市场观察：竞品市场活动报道

## 相关工具路径

- Camoufox venv: `~/.camoufox-venv/bin/python3`
- 临时脚本目录: `/tmp/`
