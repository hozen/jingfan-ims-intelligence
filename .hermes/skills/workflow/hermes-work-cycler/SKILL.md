---
name: hermes-work-cycler
description: Hermes姐姐自驱动work轮循状态管理 — 当多个状态文件不一致时，以cron执行报告(.md文件)为最终真相来源
category: workflow
---

# Hermes Work Cycler — 状态管理技能

## 核心问题

cron job维护两个可能不一致的状态文件：
- `work_progress.json` — 当前work、最后完成、备注
- `work_state.json` — 上次执行的work名

当两者不一致时（如本次：`work_state.json`说last_work=work-06，但`work_progress.json`说current_work=work-03），需要确定哪个是真相。

## 解决原则

**以cron执行报告（.md文件）为最终真相来源**。

cron每次执行后生成报告存于：
```
/home/agentuser/.hermes/cron/output/<session_id>/<timestamp>.md
```

这些report文件是不可篡改的执行记录，包含：
- 本次执行了哪个work
- 下次轮循哪个work
- 状态更新指令

## 正确的工作顺序

循环：work-01 → work-02 → work-03 → work-04 → work-05 → work-06 → work-07 → work-08 → work-09 → 循环

| Work | 主题 |
|------|------|
| work-01 | IE Expo环博会市场观察 |
| work-02 | CUWA 2026中国水协年会 |
| work-03 | 华为鸿蒙接入 |
| work-04 | IMS Moat竞争力研究 |
| work-05 | Leadership 情景领导力 |
| work-06 | 经济护城河概念研究 |
| work-07 | IMS架构/边缘AI Agent |
| work-08 | Danaher研究 |
| work-09 | 闻泰科技研究 |

## 状态文件更新（Python）

```python
import json
from datetime import datetime

# 实际使用的文件路径（在/tmp/）
STATE_FILE = '/tmp/hermes_work_state.json'
PROGRESS_FILE = '/tmp/work_status.json'

# 更新hermes_work_state.json
state = {
    "current_work": "work-07",
    "last_update": datetime.now().isoformat(),
    "last_action": "work-06经济护城河研究完成"
}
with open(STATE_FILE, 'w') as f:
    json.dump(state, f, ensure_ascii=False)

# 更新work_status.json
progress = {
    "current": "work-07",
    "last_reported": "work-06",
    "last_report_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "note": "Completed work-06 economic moat research. Next: work-07"
}
with open(PROGRESS_FILE, 'w') as f:
    json.dump(progress, f, ensure_ascii=False)
```

## 流程

1. **扫描邮箱**（如无新邮件）
2. **读取状态文件**确定当前work → 推进到下一个work
3. **研究** → **写wiki** → **发邮件给巴菲特**
4. **更新两个状态文件**（保持一致）
5. **更新wiki log.md**记录本次工作

## 文件路径

| 用途 | 路径 |
|------|------|
| Cron输出目录 | `/home/agentuser/.hermes/cron/output/` |
| Cron执行报告 | `/home/agentuser/.hermes/cron/output/eea7425d6c16/<timestamp>.md` |
| Work状态 | `/home/agentuser/.hermes/cron/output/work-cycler-state.json` |
| 状态文件(备用) | `/home/agentuser/.hermes/cron/output/work-cycle-state.json` |
| last_work | `/home/agentuser/.hermes/cron/output/last_work.txt` |
| Processed邮件 | `/home/agentuser/.hermes/cron/output/processed_emails.json` |
| Wiki projects | `/home/agentuser/wiki/docs/projects/` |
| Wiki log | `/home/agentuser/wiki/docs/log.md` |

## 邮件回复规范

⚠️ **重要**：回复巴菲特邮件必须：
1. 在原邮件基础上Reply，不能新开线程
2. 使用 `In-Reply-To` 和 `References` 头
3. UID格式：`<{uid}@163.com>`

```python
msg['In-Reply-To'] = f'<{original_uid}@163.com>'
msg['References'] = f'<{original_uid}@163.com>'
```

## 状态文件详解

实际环境中存在多个状态文件，分两类：

**Primary指针（可信）：**
- `work_cycle.txt` — 纯文本，下一个要执行的work编号，如 `work-01`
- `work_index.txt` — 纯文本，当前轮循到的数字索引，如 `9`

**Secondary JSON（可能滞后）：**
- `work-cycler-state.json` — current_work字段仅供参考（只在上一次cron执行后更新）
- `work-cycle-state.json` — 同上，备用
- `work_progress.json` — 同上
- `work_state.json` — 同上

## 状态冲突解决规则（重要经验）

**2026-05-06发现：JSON文件经常与实际轮循状态不同步。**

实际验证结果：
- `work_cycle.txt` 内容：`work-01`
- `work_index.txt` 内容：`9`
- `work-cycler-state.json` 内容：`current_work: "work-09"`

**解决原则：以 `work_cycle.txt` 为准。**

步骤：
1. 读取 `work_cycle.txt` → 得到下一个要执行的work
2. 同步 `work_index.txt` 到对应数字
3. 更新 `work-cycler-state.json` 的 `current_work` 字段为该work
4. 完成后推进 `work_cycle.txt` 到下一个work

```bash
# 读取当前work
cat /home/agentuser/.hermes/cron/output/work_cycle.txt

# 读取当前索引
cat /home/agentuser/.hermes/cron/output/work_index.txt
```

**为什么JSON会滞后：**
- JSON只在cron执行后更新
- 手动操作不会更新JSON
- 所以JSON的 `current_work` 永远是"上次cron执行时的值"，不是"当前轮循指针"

**验证：用cron报告确认**
如仍有疑惑，找最新cron报告：
```bash
ls -t /home/agentuser/.hermes/cron/output/eea7425d6c16/*.md 2>/dev/null | head -1 | xargs cat
```

## 轮循顺序

```
work-01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 循环回01
```

**推进逻辑（示例）：**
- 当前 `work_cycle.txt` = `work-09` → 本次执行work-09 → 写 `work-01` 回文件
- 当前 `work_cycle.txt` = `work-01` → 本次执行work-01 → 写 `work-02` 回文件
