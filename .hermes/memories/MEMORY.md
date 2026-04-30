Hach中国IMS，商业情报收集定位。wiki偏好topic-based结构（topics/<name>/下各自entities/concepts/comparisons/raw），而非llm-wiki原生flat type分类。本地MD文件（如IMS竞争分析_环博会后行动方案.md）也需纳入git管理。
§
Chinese curly quotes "" in Python string literals also cause SyntaxError — replace with regular quotes. grep for '"' or '"' before running Python scripts that contain Chinese text.
§
Baidu API key (bce-v3/...) is for BCE v3 auth, NOT direct Bearer token. search.bce.baidu.com DNS fails; use qianfan.baidubce.com. Baidu search skill from ClawHub needs Qianfan console API key.
§
Camoufox browser tools — FIXED Apr 2026: venv was corrupted (no python3 binary, .py source files missing). Fixed by: `python3 -m venv /home/agentuser/.camoufox-venv` then `/home/agentuser/.camoufox-venv/bin/pip install camoufox`. Works as of fix date. Python venv at `/home/agentuser/.camoufox-venv/bin/python3`.
§
Chinese search "哈希" → hash value results, NOT Hach company. Search "哈希公司" or English "Hach" or add contextual keywords like "哈希 水质监测"
§
展会研究关键方法论: (1) 官方组织渠道 - IFAT China/IE expo官网是 www.ie-expo.com, 主办方是中贸慕尼黑 (Messe Muenchen Zhongmao) (2) 官方参展商目录(需登录): https://cloud.ie-expo.cn/trade-web-site3/?p=13540&l=en (3) 官方联系邮箱: ieexpo@mm-zm.com (4) 中国展会主要通过微信公众号推广,主办方可能有公众号 (5) 展会结束3天内搜索引擎索引少,应找官方渠道 (6) 社交媒体: LinkedIn(@ie-expo), Facebook, Instagram (7) 微信展商名单文章获取：打开公众号文章图片→长按→文字识别→复制→粘贴（用户验证有效）；展位号比公司名更可靠（OCR对中文竖排文字+水印识别差，展位号往往准确）
§
Camoufox browser: `Camoufox(headless=True).start()` — NOT `.launch()`, NOT with `browser={}` arg. Fixed pattern: `from camoufox.sync_api import Camoufox; browser = Camoufox(headless=True).start(); page = browser.new_page()`. Python venv at `~/.camoufox-venv/bin/python3` — use this executable specifically, NOT system python3 when running camoufox scripts.
§
GitHub仓库: 本地git在/home/agentuser/，已commit（9b48e08，21文件），wiki/ + gen_v16.js + .gitignore。remote待配置，用户要求上传wiki + Hermes核心配置（SOUL.md/MEMORY.md/USER.md）+ 本地研究MD文件。E1馆资料未收集（用户说"把一三馆的资料准备一下"，E3已完成，E1未开始），收齐后再做PPT。
§
公网IP 175.24.134.225，但云安全组屏蔽非标准端口（8080可bind但外网不可达）。file.io上传返回301重定向（需-L跟随），transfer.sh连接被拒，tmpfiles.org超时(28)。GitHub push可行（exit28是curl超时，非host不可达）。