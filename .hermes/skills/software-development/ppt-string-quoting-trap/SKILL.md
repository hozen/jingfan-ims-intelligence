---
name: ppt-string-quoting-trap
description: Python string quoting trap in PPT generation scripts — Chinese text with ASCII double quotes causes premature string termination
---

# Python字符串引号陷阱（PPT生成专用）

## 问题现象
中文文本含ASCII双引号`"`（U+0022）会导致Python字符串在双引号字符串内提前关闭。
症状：SyntaxError报在某个完全不相关的行，实际根因在该行之前某处的中文引号。

错误信息示例：
```
SyntaxError: closing parenthesis ']' does not form a valid tuple
```
但实际是字符串内的 `"` 导致Python认为字符串结束了。

## 根因验证
用 `xxd` 查看文件原始字节：
- 正常关闭：`...67 22` = `g" `（字符串以 `"` 正确关闭）
- 异常结尾：`...27 5D 2C` = `' ],`（字符串以 `'` 结尾，不是 `"`）

用 `grep -n '"' file.py` 查找含中文引号的行。

## 另一种陷阱：Unicode Smart/ Curly Quotes

**症状**：Python报告 `SyntaxError: invalid character '，' (U+FF0C)` 或 `SyntaxError: invalid character '。' (U+3002)`，
但这些是正常中文字符，不应在Python语法中出现。

**根因**：文件中的中文弯引号 `"` `"` (U+201C/U+201D) 或全角标点混入Python字符串边界引号内，
Python解释器把它们当作字符串内容的一部分，导致行末的闭合引号被误解。

**实测案例**（work-06 PPT生成）：
```
text=""工具在变，判断力和提问力是你自己的--而这两样东西，恰恰需要真实的行业经验才能建立。""
                   ↑ U+201C left double quote              ↑ U+201D right double quote
```
Python看到：开始引号 `"` → 字符串内容 → 遇到 U+201D 被误认为字符串结束 → 后面内容变成语法错误。

**字节级诊断**：
```bash
python3 -c "
with open('script.py','rb') as f:
    lines = f.readlines()
line = lines[557]  # 报错的行号
for i,b in enumerate(line):
    if b > 127: print(f'pos {i}: 0x{b:02x}')
"
```

**修复方法**：
1. **最可靠**：重写脚本时全程避免Unicode引号，用ASCII单引号 `'` 包裹含中文的字符串
2. **批量替换**：生成脚本后用以下Python代码清理
```python
with open('script.py', 'rb') as f:
    data = f.read()
# 替换Unicode引号为ASCII近似字符
replacements = {
    b'\xe2\x80\x9c': b"'",
    b'\xe2\x80\x9d': b"'",
    b'\xe2\x80\x98': b"'",
    b'\xe2\x80\x99': b"'",
    b'\xe2\x80\x94': b'--',
    b'\xef\xbc\x8c': b',',   # 全角逗号
    b'\xef\xbc\x81': b'!',   # 全角感叹号
    b'\xef\xbc\x9f': b'?',   # 全角问号
    b'\xe3\x80\x82': b'.',   # 句号
}
for old, new in replacements.items():
    data = data.replace(old, new)
with open('script.py', 'wb') as f:
    f.write(data)
```

**预防**：写PPT生成脚本时，中文文本内容一律用单引号 `'...'` 包裹，不用双引号。

## 修复方法

### 方法1：整行重写（推荐）
将整行重写，用单引号包裹字符串：
```python
# 错误：
text = "他说："你好"，然后离开"

# 修复：
text = '他说："你好"，然后离开'
```

### 方法2：替换中文引号为Corner brackets
```python
text = "他说：「你好」，然后离开"  # 使用「」替代""
```

### 方法3：转义
```python
text = "他说：\"你好\"，然后离开"
```

## 涉及脚本
- `/home/agentuser/create_work02_ppt.py`
- `/home/agentuser/create_work05_ppt.py`
- `/home/agentuser/create_work06_ppt.py` ← Unicode smart quotes变体
- `/home/agentuser/wiki/projects/work-01-cnep/ie-expo-research/create_ppt.py`

## 验证方法
生成前用Python语法检查：
```bash
/tmp/ocr_env/bin/python -m py_compile /home/agentuser/create_work02_ppt.py
```
无输出=语法正确。

## 预防
写中文文本时，一律用单引号 `'...'` 作为Python字符串边界，不用双引号。
