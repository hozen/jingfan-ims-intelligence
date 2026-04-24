---
name: pptx-environment
description: Find the correct Python environment for python-pptx scripts on this system
category: productivity
---

# python-pptx 环境查找

## 触发条件
创建或运行任何 `.py` 脚本使用 `from pptx import Presentation` 时，如果遇到 `ModuleNotFoundError: No module named 'pptx'`。

## 已知可用的 Python 环境（按优先级）

1. **`uv 创建独立 venv`** — 2026-04-24 验证可行，当前首选方案
   ```bash
   uv venv /home/agentuser/.hermes/pptx-env --python python3
   uv pip install --python /home/agentuser/.hermes/pptx-env/bin/python python-pptx
   # 运行脚本
   /home/agentuser/.hermes/pptx-env/bin/python /path/to/script.py
   ```
   - uv pip install 首次装包 timeout 较长（60s+），遇到超时不要立即重试，等它完成
   - `/home/agentuser/.hermes/pptx-env` 已预装 python-pptx，直接用即可

2. **`/tmp/ocr_env/bin/python`** — 已不可用（venv 存在但 python-pptx 未装）
   - 不要浪费时间尝试

3. **`/home/agentuser/.hermes/hermes-agent/venv/bin/python`**
   - python-pptx **未安装**，pip 也不可用
   - 不要浪费时间在此环境上装包

## 快速命令

```bash
# 测试 pptx 是否可用
/home/agentuser/.hermes/pptx-env/bin/python -c "from pptx import Presentation; print('ok')"

# 运行 pptx 脚本
/home/agentuser/.hermes/pptx-env/bin/python /home/agentuser/create_ppt.py
```

## 常见错误

- **SyntaxError: invalid syntax** — 源码中有中文引号 `""` 或中文函数名 `def共鸣点(...)`
  - 修复：用 `execute_code` 批量替换 `""` → `"`，或函数名改为英文
- **NameError: name 'xxx' is not defined** — 函数名在 patch 后未更新调用处
  - 修复：用 `execute_code` 批量替换函数调用
- **ValueError: too many values to unpack** — `for val, w in [list_of_4_items]` 语法错误
  - 修复：`for val, w in zip(list_of_4_items, [widths...])`

## Camoufox 浏览器初始化（重要）

Camoufox 的正确启动方式是 `.start()`，不是 `.launch()`。正确用法：

```python
from camoufox.sync_api import Camoufox

browser = Camoufox(headless=True).start()   # ✅ 正确
page = browser.new_page()
page.goto('https://example.com')
browser.close()
```

错误方式（常见）：
```python
Camoufox(headless=True).launch()   # ❌ AttributeError: 'Camoufox' object has no attribute 'launch'
```

Camoufox venv 路径：`~/.camoufox-venv/bin/python`

## 验证步骤
运行脚本后检查：
1. `python-pptx SyntaxError` → 检查中文引号和中文函数名
2. `ModuleNotFoundError` → 改用 `/home/agentuser/.hermes/pptx-env/bin/python`
3. 无输出且 exit_code=0 → 检查是否调用了 `print()` 确认成功
