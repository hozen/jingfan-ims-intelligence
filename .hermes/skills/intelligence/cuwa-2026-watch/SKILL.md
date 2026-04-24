---
name: cuwa-2026-watch
description: Cron job skill for monitoring 中国城镇供水排水协会2026年会 — runs every 6h, detects new content, sends email to leshi@hach.com with IMS cross-validation.
version: 1.0.0
author: hermes
license: internal
metadata:
  hermes:
    tags: [monitoring, water-industry, china, intelligence]
    created: 2026-04-19
---

# CUWA 2026 Annual Meeting Watch

## Purpose
Monitor 中国城镇供水排水协会2026年会 for new exhibitor info, product announcements, policy signals, and AI/tech trends. Deliver intelligence reports via email to leshi@hach.com, with an IMS cross-validation section.

## Architecture

```
cuwa-2026-watch.sh          ← Bash search script (百度+微信搜索)
cuwa_watch_prev.txt         ← Previous run content (for diff detection)
send_email.py               ← Email sender (163 SMTP SSL 465)
~/.hermes/scripts/          ← All scripts live here
wiki/projects/cuwa-2026-annual-meeting/  ← Wiki archive
```

## Critical Findings (Trial & Error)

### 163 SMTP: Port 465 SSL Only
- 163邮箱SMTP **不支持** STARTTLS 587
- **正确方式**: `smtplib.SMTP_SSL('smtp.163.com', 465, context=ssl.create_default_context())`
- 错误方式: `smtplib.SMTP('smtp.163.com', 587)` → Timeout
- 授权码: `SDmxwwnLJdYCXHyn` (hozen@163.com)

### ⚠️ send_email.py Auth Code Drift陷阱
- **症状**: `SMTPAuthenticationError: (535, b'Error: authentication failed')`
- **根因**: 脚本文件中的auth code（`DVTFHXXPNLBVLDKB`）与skill中记录的正确答案（`SDmxwwnLJdYCXHyn`）不一致 — 脚本被人为修改或覆盖后未同步
- **排查**: 先用 `session_search("SDmxwwnLJdYCXHyn")` 在历史记录中检索正确auth code
- **修复**: 确认 `~/.hermes/scripts/send_email.py` 中 `SMTP_PASS = "SDmxwwnLJdYCXHyn"` 与skill一致
- **教训**: skill中记录正确值，但脚本文件可能已过期；两者必须交叉验证

### Content Diff Detection
- Compare current search output against `~/.hermes/scripts/cuwa_watch_prev.txt`
- Only trigger email + wiki update when new content detected
- Silent if no new content (no empty emails)

## IMS Cross-Validation Section (Required in Every Email)

Every email must include this section with three sub-dimensions:

1. **竞争相关性** — 此展商/产品是否和Hach IMS直接竞争？落在哪个产品线？
2. **产品缺口预警** — 对方能做到、我们还没覆盖的功能或场景
3. **甲方需求信号** — 水务集团在关注什么→可能传导到对仪表/监测的需求变化

## Known Exhibitors (to date)

| Company | Key Products/Theme | IMS Relevance |
|---------|-------------------|---------------|
| 深圳环水集团 | "环水智检"机器人+AI水质检测 | 核心竞争：AI在线监测 |
| 舜禹股份 | 智慧水务全链条 | 竞争：中游SCADA/DAS |
| 三川智慧 (300066) | AI+物联网水表 | 竞争：智能表计 |
| 万朗集团 | AI+智慧水务全流程 | 竞争：智慧水务平台 |
| 汉威科技 | 传感器+物联网 | 潜在竞争：传感器 |
| 开发科技 | 水计量全自主知识产权（住宅/商业端） | 参考：住宅计量自主可控趋势 |
| 聚光/谱育 | 在线水质监测 | 核心竞争：COD/氨氮 |

## Key Dates
- 年会: 2026-04-15~19, 深圳国际会展中心（宝安）
- 《供水条例》施行: 2026-06-01
- Cron job: every 360min × 28 iterations

## ⚠️ Bash Script Shebang Bug (Found 2026-04-23)

The shebang line and the first comment **must be on separate lines**:

```bash
# ← blank line required after shebang
# 中国水协2026年会信息追踪脚本
```

Putting the comment on the same line as `#!/bin/bash` (i.e. `#!/bin/bash# comment`) makes the shebang invalid, causing the kernel to ignore it and the cron runner to fall back to `python3`, which then fails on line 7 (`TIMESTAMP=$(date ...)`) with `SyntaxError: invalid syntax`.

Current broken script header (line 1):
```
#!/bin/bash|# 中国水协2026年会信息追踪脚本
```

Correct header:
```
#!/bin/bash
# 中国水协2026年会信息追踪脚本
```

## Cron Setup
**⚠️ Bash scripts must be invoked with `bash` explicitly** — the cron runner defaults to `python3`, which parses bash `$()` substitutions as Python syntax and throws `SyntaxError`. See `cron-bash-script-syntaxerror` skill.

```python
cronjob(action='create',
        prompt='''Run: bash /home/agentuser/.hermes/scripts/cuwa-2026-watch.sh 2>&1
Then compare against ~/.hermes/scripts/cuwa_watch_prev.txt — if new content found, save to wiki, send email via send_email.py, update prev file, and git commit.''',
        schedule='every 360m',
        repeat=28,
        name='cuwa-2026-watch',
        script='cuwa-2026-watch.sh')
```

**Important**: In the prompt, always say `bash /home/agentuser/.hermes/scripts/cuwa-2026-watch.sh` — never just `./cuwa-2026-watch.sh` or `python3 cuwa-2026-watch.sh`.

## Wiki Structure
```
wiki/projects/cuwa-2026-annual-meeting/
  PROJECT.md          # Project overview
  SESSION-*.md        # Session logs
  log.md              # Change log
  index.md            # Directory index
  raw/
    media-coverage-2026.md
    watch-log-*.md    # Watch results
    watch_log.txt     # Previous run baseline
  concepts/
    ai-water-management.md
    resilient-city-drainage.md
    water-pricing-mechanism.md
  entities/
    (company entities)
```

## Git Repo
- Name: `hach-ims-intelligence`
- Platform: Bitbucket
- SSH key: ED25519 generated at `~/.ssh/id_ed25519.pub`
- Remote: `git@bitbucket.org:hach-ims/hach-ims-intelligence.git`
