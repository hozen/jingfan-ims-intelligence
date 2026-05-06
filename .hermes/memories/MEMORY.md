Hach中国IMS，商业情报收集定位。wiki偏好topics/项目名结构。本地MD文件需纳入git管理。
§
Camoufox browser: `Camoufox(headless=True).start()` — NOT `.launch()`, NOT with `browser={}` arg. Fixed pattern: `from camoufox.sync_api import Camoufox; browser = Camoufox(headless=True).start(); page = browser.new_page()`. Python venv at `~/.camoufox-venv/bin/python3` — use this executable specifically, NOT system python3 when running camoufox scripts.
§
Wiki UI已从MkDocs/material切换到自定义Python静态生成器（2026-05-01）。输出在~/wiki-mdbook/book/，服务在port 8000。mdbook CLI因网络不通未安装，改用Python+markdown库生成。核心修复：链接需.mkd后缀→.html，导航目录（实体/概念/对比）需无index.html时用trailing slash。
§
GitHub push可行（exit28是curl超时，非host不可达）。公网IP 175.24.134.225。云安全组屏蔽非标准端口。file.io/transfer.sh/tmpfiles.org均不可用。PyPI/GitHub/Ubuntu镜像/外网下载均超时——此服务器访问外网严重受限，仅HTTP GET偶尔通，HTTPS/curl/wget大文件下载全部超时。
§
丹纳赫中国微信公众号账号：主号"丹纳赫" + "丹纳赫招聘"。定期抓取文章/视频内容存档分析，存入wiki项目work-08-danaher/raw/
§
9个work每周2次邮件动态更新（周中+周末）。邮件发送待修复。

汇报节奏：每6小时综合报告，同时发巴菲特(hozenshi@hotmail.com)和李录(69870728@qq.com)。Work看板：300次对话=100%可交付基准。01经~20轮修改才达交付标准——有PPT只是第一步。01+02已合并为"ie-expo + cuwa"。

协作工作流：遇到专业问题主动找李录(财务/公司分析)和乔布斯(营销框架)请求review。
§
邮件汇报规范（用户明确反馈）：每6小时合并成1封综合报告（不是碎片化多封），标题即结论，不要新建thread要回复已有邮件。发送巴菲特(hozenshi@hotmail.com)和李录(69870728@qq.com)。自驱动工作流：每15分钟邮件检查，不等用户指派。
§
Gateway config.yaml的model/provider字段被gateway自动重置——直接patch config.yaml会在下次交互时还原。若需切换模型，用hermes restart gateway，而非编辑config。团队：巴菲特(hozenshi@hotmail.com)、李录(69870728@qq.com)、乔布斯(279235@qq.com)、我hozen@163.com。
§
当对方没有发邮件时，主动发消息给对方（不等，先把自己该做的做好）；如果对方没回复，主动跟进（发邮件询问进度、提醒）；主动推进事情向前（不只配合，要推动）。运营工作包括：1）jobs-research项目配合乔布斯 2）丹纳赫公众号定期抓取 3）wiki-mdbook项目(work-01到work-09) 4）Git仓库状态维护。
§
研究信息验证规范：找到联系人后必须在记录中标注来源（LinkedIn/官网/搜索结果等），避免编造未验证信息。
§
团队角色（巴菲特确认）：巴菲特是老板(hozenshi@hotmail.com)，我向他汇报。李录(69870728@qq.com)是高级PM，协调项目，强财务+公司分析。乔布斯(279235@qq.com)做Jobs网站，我辅助；擅长营销框架，成果是研究输入。我向乔布斯学习营销框架，主动应用。

Cron每15分钟检查邮箱+自驱动工作。协作触发条件（wiki:/projects/collaboration.html）：review→李录，技术/开发→乔布斯，财务分析→李录，营销框架→引用乔布斯成果，决策→巴菲特。主动保持与乔布斯、李录通信畅通。
§
邮件书写规范（用户明确反馈）：不要新建邮件——要回复已有邮件thread；不要碎片化多封——内容合并成1封；标题即结论；每6小时一次综合报告。IMAP搜索前必须先select INBOX。
§
work-02（铁路货运经济观察）数据源优先级：大秦铁路(601006)月度公告 > 神华(601088)年报含朔黄线参股数据 > 西部创业(000557)季报 > 国家铁路局月度数据。用户指出的方法论：A股铁路上市公司年报/季报是最快最新的数据源。