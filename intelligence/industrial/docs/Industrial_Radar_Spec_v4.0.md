# iMS Industrial Radar — Spec v4.0
# 2026-09-12 用户明确确认的输出与方向修正（强制，优先级最高）

## 背景
用户反馈：以前纠正过的问题没有带入新一天的任务执行。
根因：修正只存在于散落的规范文件中（v3.0 在旧会话目录），job 的 message 从未更新引用，导致每次执行读不到。
本 v4.0 规范已同步写入定时任务（job_1594ac48）的 message，成为强制规则。

## 修正 1：不生成 PDF，只输出 MD
- 取消全部 PDF 输出要求（weekly_reports/ 目录、reportlab、WeasyPrint、手机版PDF、PDF命名 一律取消）。
- 每次运行在对话中直接输出完整 MD 报告，并保存到 {工作目录}/ims_industrial_radar/IND_Radar_Daily_YYYYMMDD.md，用 file_export 声明交付。

## 修正 2：JSON 只生成当天文件
- 只生成 {工作目录}/ims_industrial_radar/daily_YYYY-MM-DD.json。
- 不再生成 latest.json，不再覆盖 GitHub 上的 intelligence/industrial/latest.json。
- GitHub 推送：只推送 intelligence/industrial/daily/YYYY-MM-DD.json（当天文件）。

## 修正 3：Stage 1/2/3 完整执行
每次运行必须完整执行并输出三个 Stage：
- Stage 1 Discovery：Engine A + Engine B + Engine C 扫描
- Stage 2 Qualification：PULL Demand Qualification + PASS/WATCH/REJECT + Qualification Card + Influence Window
- Stage 3 输出与下游交接：每条正式信号输出下游 Stakeholder 线索（业主/设计院/EPC/仪表集成商/集团关系）+ owner 角色 + missing_roles + next_validation_action（stage3_handoff 字段），保持 Lead ID 与 Stage 3 Enrichment 接口兼容。

## 修正 4：Early Signal 优先，拒绝"招标搜索器"（v3.0 核心，正式纳入）
Radar 的价值不是"比销售早几天看到招标"，而是"在客户需求已出现、技术规格尚未冻结之前发现机会"。

### Engine C — Early Signal / 前置信号雷达（与 Engine A/B 并列）
专门寻找尚未进入正式采购、但已出现商业 Trigger 的账户：
- Project Trigger：项目备案/立项/可研/环评第一次公示/节能审查/土地审批/重大项目清单/扩建计划/技改计划/产能规划
- Customer Problem：环保整改/行政处罚/在线监测异常/水质事故/排放异常/仪表运维问题/数据质量问题/环保督察/设备老化/运维外包/人员不足
- Digitalization Trigger：智慧工厂/智慧电厂/数字化转型/设备管理/预测性维护/少人值守/无人值守/集中控制/远程运维/AI运维/环保数字化/数据平台
- Organization/Investment Trigger：新工厂/新产线/大规模扩产/新厂区/集团统一管理/多厂整合/公辅系统升级/环保系统升级

### 招标类来源降级
- 招标公告/EPC招标/设备采购/中标公告 = Tender Monitoring（补充信息），不得占据首页 Top List。
- 已正式发布招标通常判断 LATE（除非技术规格仍可影响）。

### Influence Window（每条线索必填）
回答"Hach/iMS 现在还能影响什么？"
- HIGH：方案架构/水处理概念/监测策略/仪表规格/数字化需求/供应商名单/iMS需求 仍可影响
- MEDIUM：仪表选型/品牌选择/包件规格/EPC供应商推荐 仍可影响
- LOW：只能参与已形成采购/争取品牌替换/通过EPC进入
- NONE：方案、规格、供应商基本已定

### Entry Timing（每条线索必填）
EARLY / GOOD / LATE / CLOSED —— 按"技术规格是否仍可影响"判断，不是距开标天数。

### 首页结构
①今日 Early Opportunities（Early Signal + High/Medium Influence，3-5条，最重要）
②今日 iMS Opportunities（客户问题是什么；无则明确写 0）
③Tender Monitoring（小区域，仅 Sales heads-up）
④Market Insight

### Search Bias Check（每次日报完成前）
计算 Early Signal % / Pre-Tender % / Tender % / Awarded %；
若 Tender + Awarded > 50%，触发 Search Bias Warning 并补一轮 Early Signal 搜索。

### Quality Gate
每条准备进入 Top Opportunities 的线索，发布前问："如果销售今天知道这条，他还能影响什么？"
- 只能"赶紧投标" → Tender Monitoring
- 可以"找到 Owner/设计院/EPC，在方案和规格形成前影响需求" → Radar Opportunity

## 其他保持不变
两个原有 Engine（A Compliance / B CapEx）、PULL Qualification v1、信号验证规则 v2.1、证据纪律、优先行业（半导体/新能源/石化/食品饮料/制药）、机会分级、Priority 三维度、Water System Ownership、与 Municipal 区分、持续性规则。

## North Star（v4.0 重申）
- Radar 的价值不是提前看到招标，而是在客户需求已出现、技术规格尚未冻结的时候发现机会。
- Early Signal > Tender Signal
- Customer Problem > Product Keyword
- Influence Window > Days Before Bid
- Installed Base Pain + Operational Trigger 与 New CapEx 同等重要