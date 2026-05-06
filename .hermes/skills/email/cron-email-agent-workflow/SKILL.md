---
name: cron-email-agent-workflow
description: Hermes姐姐 daily cron job - check 163.com email via POP3, process Jobs tasks, continue MQL research, report to log
---

# Cron Email Agent Workflow

## Purpose
Hermes姐姐's daily cron job pattern: check for new emails from a specific contact (Jobs), process tasks, continue own work (MQL leads, research), report status to log.

## Trigger
Scheduled cron job runs autonomously with no user present.

## Workflow

### Step 1: Check 163.com Email via POP3
Since himalaya CLI is often unavailable, use Python poplib directly:

```python
import poplib
import email
from email.parser import Parser

server = poplib.POP3_SSL('pop.163.com', 995)
server.user('hozen@163.com')
# Get password from environment or keyring
resp, lines, octets = server.list()
```

Parse emails:
```python
parser = Parser()
for i in range(len(lines), 0, -1):
    resp, msg_bytes, octets = server.retr(i)
    msg = parser.parsestr('\n'.join([b.decode() for b in msg_bytes]))
    # Extract subject, from, date
    subject = msg.get('subject', '')
    sender = msg.get('from', '')
    date = msg.get('date', '')
    # Check for Jobs emails (279235@qq.com)
```

### Step 2: Check for New Tasks from Jobs
- Jobs email: 279235@qq.com
- If new emails found → process tasks per RACI
- If no new emails → continue own pending tasks

### Step 3: MQL Lead Search (Own Work)
Key sources:
- 深圳环水集团: https://cg.sz-water.com.cn/hyzbgg/ (招标公告) + /hfcggg/ (非招标采购)
- 威海水务: similar patterns
- Keywords: HACH, 哈希, 试剂, 耗材, 水质监测

Update `/tmp/mql-leads-2026.md` with findings.

### Step 4: Update Work Board
After processing, update `~/.hermes/work-board.txt`:
- Increment the 对话 count for any work discussed/advanced
- Recalculate 完成度 = 对话轮次 / 300 × 100%
- Mark status if changed

Example update:
```
| 02 | railway-freight | 15 | 5% | 专项研究中：大秦铁路+中欧班列数据 |
```

### Step 5: Report to Log
Write status to `/tmp/hermes-to-jobs.log`:
```
=== Cron Run: YYYY-MM-DD HH:MM ===

[邮箱检查]
- 乔布斯新邮件: N封

[MQL线索跟踪]
- 今日更新内容
- 临近截止提醒

[jobs-research状态]
- Phase 1: 状态
- Phase 2: 状态

[下次待办]
1. ...
```

## Key Contacts (RACI)
- 乔布斯 (279235@qq.com): A+R for jobs-research, Advisory for MQL
- Mr. Buffett (HozenShi@hotmail.com): I (Informed, 6h auto-report)
- Hermes姐姐: R+A for MQL, R+C for jobs-research

## Work Board
- File: `~/.hermes/work-board.txt`
- 基准：300轮对话 = 100%完成
- 每次cron或对话后更新各work的对话轮次和完成度
- 状态说明要简洁（不超过10字）
