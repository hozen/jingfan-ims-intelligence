---
name: image-ocr-workflow
description: Real-world photo/video OCR workflow when browser_vision is broken — uses Camoufox + Tesseract
triggers:
  - 用户发送展会照片要求识别文字
  - 图片OCR质量差，需要增强
  - browser_vision工具报错
---

# Image OCR Workflow for Real-World Photos

## Context
当需要从展会现场拍摄的照片/视频中提取文字信息时，Hermes内置`browser_vision`工具可能损坏（报错"Expecting value: line 1 column 1 (char 0)"），需要备用方案。

## 工具链

### Tesseract OCR（基础）
```bash
# 基本用法 - chi_sim=简体中文，eng=英文
tesseract /path/to/image.jpg stdout -l chi_sim --psm 6

# PSM模式说明：
#   --psm 3  Fully automatic page segmentation（自动，最通用）
#   --psm 6  Assume single uniform block of text
# 实测：展会照片用PSM 3效果通常优于PSM 6
tesseract /path/to/image.jpg stdout -l chi_sim --psm 3
```

### Camoufox + Tesseract（针对低质量照片）
当直接OCR效果差时，用Camoufox截图再OCR可以绕过图片角度/格式问题：
```python
from camoufox.sync_api import Camoufox

images = [
    ("01", "/path/to/img1.jpg"),
    ("02", "/path/to/img2.jpg"),
]

browser = Camoufox(headless=True).start()
page = browser.new_page()

for key, path in images:
    page.goto(f"file://{path}")
    page.wait_for_timeout(1500)
    page.screenshot(path=f"/tmp/snap_{key}.png", full_page=True)

browser.close()
```
注意：`images=` 参数不是Camoufox的合法参数，会报错。用headless=True即可。

### ffmpeg 视频抽帧
```bash
# 从视频中均匀抽取N帧
ffmpeg -i video.mp4 -vf 'fps=1' -frames:v 3 '/tmp/frame_%03d.jpg' -y

# 查看视频信息
ffprobe -v quiet -show_format -show_streams 'video.mp4'
```

## 图片存储位置（WeChat发送）
- 图片：`/home/agentuser/.hermes/image_cache/img_[hash].jpg`
- 视频：`/home/agentuser/.hermes/cache/documents/doc_[hash]_video.mp4`

## 验证步骤
```bash
# 1. 确认图片存在
file /path/to/image.jpg

# 2. 快速OCR测试
tesseract /path/to/image.jpg stdout -l chi_sim --psm 3 | head -20

# 3. Camoufox截图测试
~/.camoufox-venv/bin/python3 -c "from camoufox.sync_api import Camoufox; browser = Camoufox(headless=True).start(); page = browser.new_page(); page.goto('file:///path'); page.screenshot(path='/tmp/test.png'); browser.close()"
```

## 已知问题
1. **browser_vision工具损坏**：所有browser_navigate调用返回"Expecting value: line 1 column 1 (char 0)"，无法用内置浏览器分析图片
2. **Camoufox venv**：`~/.camoufox-venv/bin/python3`，不是系统python3
3. **Tesseract对展会现场照片OCR效果差**：角度、光线、复杂背景导致识别率低
4. **视频字幕OCR**：展会演讲视频OCR效果极差

## 备用方案：当 browser_vision 工具损坏时

Hermes `browser_vision` 工具可能完全失效（报错"Expecting value"），但 Camoufox 本身正常。此时：

1. **写Python脚本**用Camoufox直接截取图片（绕过Hermes工具层）
2. **启动本地HTTP服务**提供图片：`cd /image_dir && python3 -m http.server 8000 --bind 0.0.0.0`
3. **公司名核实**：用Camoufox打开百度搜索截图 → Tesseract OCR验证

```python
# 完整工作流：截取本地图片 + OCR + 网络核实
from camoufox.sync_api import Camoufox
import subprocess, time

IMGS = {
    "01": "/home/agentuser/.hermes/image_cache/img_xxx.jpg",
    "02": "/home/agentuser/.hermes/image_cache/img_yyy.jpg",
}
browser = Camoufox(headless=True).start()
page = browser.new_page()
for key, path in IMGS.items():
    page.goto(f"file://{path}")
    page.wait_for_timeout(1500)
    page.screenshot(path=f"/tmp/snap_{key}.png", full_page=True)
    print(f"Saved snap_{key}.png")
browser.close()

# OCR
for key in IMGS:
    r = subprocess.run(
        ["tesseract", f"/tmp/snap_{key}.png", "stdout", "-l", "chi_sim", "--psm", "6"],
        capture_output=True, text=True
    )
    print(r.stdout[:500])
```

## 图片存储位置（WeChat发送）
```bash
# 1. 确认图片存在
file /path/to/image.jpg

# 2. 快速OCR测试
tesseract /path/to/image.jpg stdout -l chi_sim --psm 3 | head -20

# 3. Camoufox截图测试
~/.camoufox-venv/bin/python3 -c "from camoufox.sync_api import Camoufox; browser = Camoufox(headless=True).start(); page = browser.new_page(); page.goto('file:///path'); page.screenshot(path='/tmp/test.png'); browser.close()"
```
