---
name: wiki-internal-link-checker
description: Verify all internal links in a static wiki/mdbook site work correctly. Finds broken 404 links before deployment.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [wiki, static-site, link-checker, quality_assurance]
    related_skills: [systematic-debugging]
---

# Wiki Internal Link Checker

## Overview

Check all internal links in a static HTML site (like mdbook/wiki generated sites) to find broken links before deployment.

## The Problem

When generating static HTML from markdown, some links may become broken:
- Links to other markdown files (may not render or path changes)
- Relative vs absolute path issues
- Cross-references between project subdirectories

## The Key Insight

**Ambiguous request**: When user says "404", they may mean:
1. **Fallback 404 page** — create a custom "page not found" page
2. **Broken link check** — find and fix links in the site that return 404

**Always clarify** which one they want. The approach is completely different.

## How to Check

### Step 1: Build the site first

```bash
cd ~/wiki-mdbook && python3 build.py
```

### Step 2: Verify target files exist

Links in HTML use absolute paths from web root (like `/projects/index.html`), not relative.

```python
# From book/ directory, check if link target exists
for link in extracted_links:
    # Resolve: /projects/index.html -> book/projects/index.html
    target = "book" + link  # prefix to get actual file path
    if not exists(target):
        print(f"BROKEN: {source_file} -> {link}")
```

### Step 3: Common false positives

- `/index.html` → exists at `book/index.html`
- `/comparisons/index.html` → exists at `book/comparisons/index.html`
- `/projects/work-01-ie-expo/README.html` → exists at `book/projects/work-01-ie-expo/README.html`

The script must resolve paths correctly, not just check if file exists at exact string match.

## Example Verification

```python
import os
from pathlib import Path

book_dir = Path("book")

def check_links():
    broken = []
    for html_file in book_dir.rglob("*.html"):
        content = html_file.read_text()
        # Extract links like href="/path/file.html"
        for match in re.findall(r'href="([^"#]+)', content):
            if match.startswith(("http", "#", "mailto")):
                continue
            
            # Resolve path
            target = book_dir / match.lstrip("/")
            if not target.exists():
                # Don't report false positives
                if not target.with_suffix(".html").exists():
                    broken.append((html_file.name, match))
    return broken
```

## Common Issues Fixed

| Issue | Fix |
|-------|-----|
| `index.md` not building to `index.html` | Build process bug - check glob pattern |
| Links to `/keywords.html` broken | Keywords file not in root .md glob |
| Relative path doesn't resolve | Use absolute paths in HTML (start with /) |
| Cross-project references broken | Check link format in source markdown |

## Verification Checklist

- [ ] All index.html files in each subdirectory exist
- [ ] All project README links resolve
- [ ] All entity/concept/reference links resolve
- [ ] Cross-project references (like work-05→work-04) work
- [ ] Keywords/index page has all nav links

## Related

- systematic-debugging: For actual bugs found
- wiki-static-generator: For building the wiki