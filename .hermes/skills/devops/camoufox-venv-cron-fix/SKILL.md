---
name: camoufox-venv-cron-fix
description: Fix camoufox venv Python path resolution failure in cron jobs
category: devops
---

# Camoufox Venv Cron 故障排查与修复

## 触发条件
cron job 调用 camoufox 脚本失败，报 `ModuleNotFoundError: No module named 'camoufox'`

## 根因
脚本 shebang 写的是：
```bash
#!/usr/bin/env /home/agentuser/.camoufox-venv/bin/python3
```
`/usr/bin/env` 会从 `$PATH` 查找可执行文件，而非直接执行给定路径。系统 python3（3.12）位于 `$PATH` 前，venv 的 python3.11 被绕过。

## 正确调用方式
```bash
/home/agentuser/.camoufox-venv/bin/python3 /home/agentuser/.hermes/scripts/cuwa-2026-watch.sh
```
直接调用 venv 的 python 解释器，**不经过** `env` / shebang。

## 验证步骤
```bash
# 确认 camoufox 在 venv 中
/home/agentuser/.camoufox-venv/bin/python3 -c "import camoufox; print('ok')"

# 确认 shebang 问题（会失败）
/usr/bin/env /home/agentuser/.camoufox-venv/bin/python3 -c "import camoufox"  # → ModuleNotFoundError
```

## 相关路径
- venv 根: `/home/agentuser/.camoufox-venv/`
- venv python: `/home/agentuser/.camoufox-venv/bin/python3` → 指向 python3.11
- watch 脚本: `/home/agentuser/.hermes/scripts/cuwa-2026-watch.sh`
- 状态文件: `/home/agentuser/.hermes/scripts/cuwa_watch_prev.txt`

## 其他可用工具
- camoufox-venv python 路径稳定，勿依赖系统 python3
- 如需其他 venv 包，先 `pip install --target=/home/agentuser/.camoufox-venv/lib/python3.12/site-packages`
