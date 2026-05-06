---
name: wiki-static-generator
description: Build and serve a local wiki from markdown files using Python static generator - mdBook-style, 0 JS
---
# Wiki Static Generator
## Setup (2026-05-01)
- Source: `~/wiki-mdbook/src/`
- Output: `~/wiki-mdbook/book/`
- Serve: `cd ~/wiki-mdbook/book/ && python3 -m http.server 8XXX` (MUST cd to book/ subdirectory, NOT root)
- Build: `cd ~/wiki-mdbook && python3 build.py` (from ROOT, NOT src/ — the build script lives at `wiki-mdbook/build.py`, NOT `wiki-mdbook/src/build.py`)
## Adding New Project = 3 Steps
1. Create `src/projects/work-XX/`
2. Add entry to BOTH `src/index.md` AND `src/projects/index.md`
3. Run build.py

## Important: build.py Changes Do NOT Auto-Regenerate Existing HTML
When build.py template changes, must ALSO manually fix existing HTML files AND update src markdown.
## Key Learnings (2026-05-01)
- Network is limited on this server. Cannot install rust mdbook via `cargo install` or `curl` downloads. Use Python markdown library.
- Absolute path links (`/index.html`) are REQUIRED for subdir navigation to work. Relative links break across directory boundaries.
- Run the generator after any MD file changes.