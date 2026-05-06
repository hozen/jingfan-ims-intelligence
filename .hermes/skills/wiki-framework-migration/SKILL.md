---
name: wiki-framework-migration
description: Migrate Wiki from heavy JS framework (MkDocs/Docsify) to lightweight static HTML
tags: []
---

# Wiki Framework Migration Pattern

## Problem
Migrate Wiki from heavy JS framework (MkDocs/Docsify) to lightweight static HTML.

## Key Learnings

### 1. mdBook Install Failure → Python Fallback
Network blocks GitHub downloads (`curl`/`wget`/`cargo` all timeout).
**Fallback**: Python static site generator using `markdown` + `jinja2`.

```python
# Minimal build script pattern
import markdown
from pathlib import Path
CSS = "/* User-preferred styling */"
HTML = "<!DOCTYPE html>..."
md = markdown.Markdown(extensions=['toc', 'tables'])

for md_file in src.rglob("*.md"):
    html = HTML.replace("{{content}}", md.convert(md_file.read_text()))
    (out / md_file.with_suffix(".html")).write_text(html)
```

### 2. Link Path Conversion (.md → .html)
MD files reference `.md` links but HTML outputs are `.html`. Links break (404).
**Fix**: Convert all links before building.

```python
import re
content = re.sub(r'href="(.*)\.md"', r'href="\\1.html"', content)
content = re.sub(r'\.md(#.*)?\)', r'.html\1)', content)
```

**Directory-style URL choice**: If using `/entities/` instead of `/entities/index.html`, strip `/index.html` from links:
```python
content = content.replace('href="/index.html"', 'href="/"')
content = re.sub(r'href="(.*)/index.html"', r'href="\\1/"', content)
```

### 3. Directory-Style URLs (Preferred over /index.html)
Modern static sites prefer clean URLs: `/entities/` over `/entities/index.html`.
**Pros**: Cleaner, more maintainable, works with trailing slash conventions.
**Cons**: Requires the web server to serve index.html for bare directories.
**Fix**: For Python http.server, bare directory URLs work automatically. For nginx, need `try_files $uri $uri/ =404`.

### 4. Source File Path Prefix Bug (CRITICAL — Found Through Trial)
When copying MD files, path references inside the files may have duplicate prefixes.
Example: `src/entities/companies/entities/companies/hach.md` — the path segments are doubled inside the MD content itself.
**Symptom**: Generated HTML has URLs like `/entities/entities/companies/`.
**Fix**: Edit source MD files directly. Find `entities/companies/` inside content, replace with `companies/` if already under that path.
**Detection**: Search MD source for repeated path segments (entities/entities, concepts/concepts).

### 5. Camoufox Verification Command (Specific to This Server)
The camoufox venv is at `~/.camoufox-venv/bin/python3` — use this executable, NOT system python3.
```python
from camoufox.sync_api import Camoufox
browser = Camoufox(headless=True).start()
page = browser.new_page()
page.goto("http://175.24.134.225:8000/entities/")
# ... test clicks and navigation
browser.close()
```

### 6. Rebuild + Restart Server Pattern
After modifying source and rebuilding, always restart the server:
```bash
# Kill old server
pkill -f "http.server 8000" || true
# Rebuild
cd ~/wiki-mdbook && python3 build.py
# Restart
cd ~/wiki-mdbook/book && python3 -m http.server 8000 &
```

### 7. mdBook Sidebar Layout CSS
mdBook-style layout: fixed left sidebar (240px) + scrollable main content area with top breadcrumb bar.
```css
#sidebar {position:fixed; width:240px; height:100vh; overflow-y:auto; border-right:1px solid #ddd; padding:16px;}
#content {margin-left:240px; padding:0 24px;}
#topbar {position:sticky; top:0; background:#fff; border-bottom:1px solid #ddd; padding:12px 24px;}
```

### 8. Mobile Responsive Design (Hamburger Menu)
User reported "mobile view broken" — sidebar fixed at 260px overflows on small screens.
**Fix**: Add hamburger menu with JS toggle + media queries.

```html
<nav class="main">
<span class="menu-toggle" onclick="toggleMenu()">☰</span>
<span style="color:#fff;font-weight:600">IMS Wiki</span>
<div class="main-links">
<a href="/index.html">首页</a>
<a href="/projects/index.html">项目</a>
<!-- ... -->
</div>
</nav>
<script>
function toggleMenu(){document.querySelector('.main-links').classList.toggle('open')}
</script>
```

```css
nav.main{background:var(--blue);padding:12px 20px;display:flex;justify-content:space-between}
nav.main .menu-toggle{display:none;font-size:24px;cursor:pointer;color:#fff}
@media (max-width:600px){
  nav.main .menu-toggle{display:block}
  nav.main-links{display:none;position:absolute;top:50px;left:0;right:0;background:var(--blue);padding:15px}
  nav.main-links.open{display:block}
}
```

**Testing**: Use camoufox with mobile viewport (390x844) or Playwright MCP browser_resize.

### 9. Image/PPT Support in Static Generator
User wanted "图文并茂" - wiki pages with images.
**Fix**: Add image copy + CSS to build.py.

```python
import shutil

# Copy images from src to book
def copy_assets(src_dir, out_dir, subdirs):
    for subdir in subdirs:
        src = src_dir / subdir
        if src.exists():
            for img in src.rglob('*.png'):
                rel = img.relative_to(src)
                dst = out_dir / subdir / rel.parent
                dst.mkdir(parents=True, exist_ok=True)
                shutil.copy2(img, dst / rel.name)
            for img in src.rglob('*.jpg'):
                # ... same pattern
            for pptx in src.rglob('*.pptx'):
                # ... same pattern
    
copy_assets(SRC, OUT, ['projects'])
```

Add image CSS:
```css
img{max-width:100%;height:auto;border-radius:4px;margin:10px 0}
figure{margin:15px 0}
figcaption{color:var(--light);font-size:13px;text-align:center}
```

Then in MD files: `![描述](archive/image.png)`

### 10. Git Post-Commit Hook for Auto-Build
User wanted: "git push后自动build" - automate wiki rebuild on commit.
**Setup**:
```bash
cd ~/wiki-mdbook
git init
git config user.email "agent@local"
git config user.name "IMS Agent"
```

Create `.git/hooks/post-commit`:
```bash
#!/bin/bash
cd "$(git rev-parse --show-toplevel)"
python3 build.py

# Auto-commit generated files
git add -A
if [[ -n $(git status --porcelain) ]]; then
    git commit -m "Auto-build: $(date '+%Y-%m-%d %H:%M')" --no-verify
fi
```

**Workflow**: `git add -A && git commit -m "更新"` → auto-build → page updates.

### 11. Project README.md Required
work-02-cuwa not showing - missing `README.md` in project directory.
Every project needs README.md to appear in wiki index.
**Check**: `ls projects/*/README.md` should show all projects.
Source file `wanlang-group.md` but link points to `wan-lang-group.html` → 404.
**Fix**: Verify all links match actual filenames. Use camoufox crawl to exhaustively find broken links.

```python
# Crawl all pages to find 404s
def crawl(url, depth=0):
    page.goto(url)
    if page.title() == 'Error response':
        errors.append(url)
    for link in page.eval_on_selector_all('a[href]'):
        crawl(link, depth+1)
```

### 5. Missing index.md → Create Manually
**Fix**: Create index.md manually for each subdirectory.

### 6. Model Split
| Phase | Model | Task |
|-------|-------|------|
| Analysis | expensive | Understand structure, plan migration |
| Installation | cheap | Simple installs, file ops |
| Configuration | expensive | Config decisions |
| Build | cheap | Batch generation |
| Verification | expensive | Quality check |

### 7. User Preferences (CSS)
User prefers: 白底无背景, 三色(蓝#007ab5/深灰#4d4d4d/浅灰#999), 微软雅黑字体.

```css
:root{--blue:#007ab5;--dark:#4d4d4d;--light:#999}
body{font:'Microsoft YaHei',sans-serif}
```

## Workflow
1. Analyze source structure (`docs/` = MD, `site/` = output)
2. Create `book.toml` config (even if mdBook won't install, it documents structure)
3. Copy content to `src/`
4. Create missing `index.md` files
5. Check for duplicate path segments in MD source (search for `entities/entities/`, `concepts/concepts/`)
6. Fix link paths (.md → .html, decide on directory-style vs /index.html)
7. Build static HTML with Python script
8. Verify all pages return 200 (use camoufox crawl — check from root, then spot-check subdirectories)
9. Deploy: `cd output_dir && python3 -m http.server 8000`
10. **After any rebuild: kill old server, rebuild, restart server**
11. Final visual check with browser_vision on key pages