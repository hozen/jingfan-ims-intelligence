---
name: hermes-cron-management
description: Manage Hermes scheduled cron jobs - create, update, merge, and troubleshoot. Includes team emails and lessons learned.
---

# Hermes Cron Job Management

## Key Lessons Learned

### 1. Updating vs Recreating
- **Don't use `update`** when changing core settings (schedule, model) - often fails silently
- **Remove and recreate** for major changes instead

### 2. Schedule Format
- Use `30m` format, NOT `*/30 * * * *` - latter causes parsing errors
- For cron expression: `*/30 * * * *` works but model may not persist

### 3. Merging Similar Tasks
When multiple jobs do similar work, merge them:
- **Before**: email-check (10min) + 9work-dynamic (12h) + daily-research (7am) = 3 jobs
- **After**: One combined job running every 30min checking email + self-driven work

### 4. Combined Task Pattern
```
每30分钟运行:
1. 检查邮箱 (POP3) → 有新邮件则处理
2. 无新邮件 → 轮循研究1个work → 存wiki → 发邮件汇报巴菲特
```

### 5. Model Persistence Issue

- This is a display bug - the model is usually applied at runtime

### 6. Troubleshooting Status
- Status showing "error" doesn't always mean failure - check actual output files
- Look in `~/.hermes/cron/output/<job_id>/` for execution results

## Current Active Jobs (as of 2026-05-04)

| Job ID | Name | Frequency | Status |
|--------|------|-----------|--------|
| b1871e3c3125 | Work 6小时更新 | 6h | ok |
| 4c4555f67855 | Hermes姐姐-主任务 | 30min | active |
| f1c5fea04637 | hermes-to-jobs-monitor | paused |

## Team Emails (MUST remember)
- 巴菲特 (Mr. Buffett): hozenshi@hotmail.com
- 李录 (LiLu / 高级项目经理): 69870728@qq.com
- 乔布斯 (Steve Jobs): 279235@qq.com
- Hermes姐姐 (我): hozen@163.com
- Hermes妹妹: 李录的助手

## Command Reference

### List Jobs
```
cronjob(action='list')
```

### Create New Job (correct pattern)
```
cronjob(
  action='create',

  name='任务名',
  prompt='详细的prompt',
  repeat=9999,
  schedule='30m'
)
```

### Run Immediately
```
cronjob(action='run', job_id='xxx')
```

### Pause/Remove
```
cronjob(action='pause', job_id='xxx')
cronjob(action='remove', job_id='xxx')
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| '<=' not supported | schedule format wrong | Use '30m' not '*/30' |
| model null | UI display bug | Check actual output files |
| status error | may still work | Check output directory |