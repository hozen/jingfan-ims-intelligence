#!/usr/bin/env /home/agentuser/.camoufox-venv/bin/python3
"""
中国水协2026年会信息追踪脚本
每6小时执行一次，持续一周
"""
import sys
sys.path.insert(0, '/home/agentuser/.camoufox-venv/lib/python3.12/site-packages')

from camoufox.sync_api import Camoufox
import os

WIKI_DIR = "/home/agentuser/wiki/projects/cuwa-2026-annual-meeting/raw"
os.makedirs(WIKI_DIR, exist_ok=True)
LOGFILE = os.path.join(WIKI_DIR, "watch_log.txt")

from datetime import datetime

with open(LOGFILE, "a", encoding="utf-8") as f:
    f.write(f"\n=== {datetime.now().strftime('%Y-%m-%d %H:%M')} 搜索 ===\n")

browser = Camoufox(headless=True).start()
page = browser.new_page()

queries = [
    "中国水协2026年会 深圳",
    "水业圈 2026年会",
    "中国城镇供水排水协会 2026 技术交流",
    "深圳环境水务集团 2026 年会参观",
    "中国水协 2026 十五五 水务规划"
]

output_lines = []

for q in queries:
    try:
        page.goto(f"https://www.baidu.com/s?wd={q}", timeout=15000)
        page.wait_for_timeout(2000)
        text = page.inner_text("body")
        lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 10]
        results = [l for l in lines if any(k in l for k in ["年会","水协","深圳","水务","供水","排水","十五五","AI","智能","综合大会","技术交流"])]
        if results:
            output_lines.append(f"\n## {q}")
            for r in results[:15]:
                output_lines.append(r)
    except Exception as e:
        output_lines.append(f"ERROR {q}: {e}")

browser.close()

with open(LOGFILE, "a", encoding="utf-8") as f:
    f.write("\n".join(output_lines))
    f.write("\n---\n")

print("Log written to:", LOGFILE)
print("\n".join(output_lines))
