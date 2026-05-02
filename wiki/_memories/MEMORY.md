Hach中国IMS，商业情报收集定位。wiki偏好topics/项目名结构。本地MD文件需纳入git管理。
§
Chinese curly quotes "" in Python string literals also cause SyntaxError — replace with regular quotes. grep for '"' or '"' before running Python scripts that contain Chinese text.
§
Baidu API key (bce-v3/...) is for BCE v3 auth, NOT direct Bearer token. search.bce.baidu.com DNS fails; use qianfan.baidubce.com. Baidu search skill from ClawHub needs Qianfan console API key.
§
Camoufox venv已修复，用~/.camoufox-venv/bin/python3。GitHub push可行，公网IP 175.24.134.225，PyPI/GitHub/外网下载均超时——仅HTTP GET偶尔通。
§
展会研究关键方法论: (1) 官方组织渠道 - IFAT China/IE expo官网是 www.ie-expo.com, 主办方是中贸慕尼黑 (Messe Muenchen Zhongmao) (2) 官方参展商目录(需登录): https://cloud.ie-expo.cn/trade-web-site3/?p=13540&l=en (3) 官方联系邮箱: ieexpo@mm-zm.com (4) 中国展会主要通过微信公众号推广,主办方可能有公众号 (5) 展会结束3天内搜索引擎索引少,应找官方渠道 (6) 社交媒体: LinkedIn(@ie-expo), Facebook, Instagram (7) 微信展商名单文章获取：打开公众号文章图片→长按→文字识别→复制→粘贴（用户验证有效）；展位号比公司名更可靠（OCR对中文竖排文字+水印识别差，展位号往往准确）
§
Camoufox browser: `Camoufox(headless=True).start()` — NOT `.launch()`, NOT with `browser={}` arg. Fixed pattern: `from camoufox.sync_api import Camoufox; browser = Camoufox(headless=True).start(); page = browser.new_page()`. Python venv at `~/.camoufox-venv/bin/python3` — use this executable specifically, NOT system python3 when running camoufox scripts.
§
Wiki UI已从MkDocs/material切换到自定义Python静态生成器（2026-05-01）。输出在~/wiki-mdbook/book/，服务在port 8000。mdbook CLI因网络不通未安装，改用Python+markdown库生成。核心修复：链接需.mkd后缀→.html，导航目录（实体/概念/对比）需无index.html时用trailing slash。
§
GitHub push可行（exit28是curl超时，非host不可达）。公网IP 175.24.134.225。云安全组屏蔽非标准端口。file.io/transfer.sh/tmpfiles.org均不可用。PyPI/GitHub/Ubuntu镜像/外网下载均超时——此服务器访问外网严重受限，仅HTTP GET偶尔通，HTTPS/curl/wget大文件下载全部超时。
§
丹纳赫中国微信公众号账号：主号"丹纳赫" + "丹纳赫招聘"。定期抓取文章/视频内容存档分析，存入wiki项目work-08-danaher/raw/
§
任务拆分规则：复杂任务（5+工具调用）开始前先给框架，待用户确认后再深入，避免超时。
§
Wiki最终形态：导航=市场研究|关键词|实体（3入口）。实体页面(entities/)是公司/事件/政策索引，用户认为意义不大但暂未移除。首页=项目列表+最近更新。
§
双Agent协作(Hermes姐姐)：文件队列异步通信，queue-A→B/B→A.log，5min节拍。A管战略/拍板，B管执行/整理/检索。
§
我在双Agent系统中的名字：Alex (Agent-B)