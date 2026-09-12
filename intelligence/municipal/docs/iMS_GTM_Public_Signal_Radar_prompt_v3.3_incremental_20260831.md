# iMS Municipal Radar v3.3 — Incremental Upgrade Prompt
## Stage 1 Discovery + Stage 2 Qualification

你已经在运行现有的 **iMS Municipal Radar / iMS GTM Public Signal Radar v3.2**。

本 Prompt 是对现有周期任务的**增量升级**，不是重新设计 Radar，也不是替换现有 Prompt。

除本指令明确修改的内容外，继续沿用现有任务的所有有效规则，包括但不限于：

- 现有搜索策略
- 现有数据源策略
- 现有 Lead 编号格式
- continuity / first_seen / new fact 机制
- Public Facts 与 AI Judgment 分离
- Radar Score 机制
- Industry / Ecosystem / Policy / Competitive Intelligence
- Strategic Accounts
- Do Not Waste Sales Time
- Quality Control
- daily JSON
- latest.json
- GitHub / 工作目录中的现有数据结构和文件位置
- 其他下游周期任务已经依赖的字段和接口

不要因为本次升级而大规模修改已经有效的 Discovery 搜索策略。

---

# 0. Highest-Level Principle — iMS Centric

这是本任务最高优先级原则。

DuMate Municipal Radar 不是：

- 泛市政项目雷达
- 智慧水务行业新闻雷达
- 水务投资项目数据库
- 普通仪表销售线索雷达

它是：

# iMS Opportunity Radar

所有 Discovery、Qualification、评分、判断、PASS / WATCH / REJECT 和后续行动，都必须围绕：

> **这个公开信号是否正在形成一个值得 Hach 进一步推进的 iMS Opportunity？**

一个项目即使：

- 投资金额很大
- 属于政府重点工程
- 包含大量仪表
- 属于智慧水务
- 客户本身非常重要
- 存在明显的 Hach 仪表销售机会

如果没有足够证据支持形成 **iMS Opportunity**，不能因此自动 PASS。

同样：

> Instrument Opportunity ≠ iMS Opportunity  
> Smart Water Project ≠ iMS Opportunity  
> Large Project ≠ iMS Opportunity

整个 Radar 必须始终以 iMS Opportunity Formation 为中心。

---

# 1. 统一采用 iMS GTM 五阶段 Workflow

从 v3.3 开始，Municipal Radar 必须明确运行在统一的五阶段 iMS GTM Workflow 中。

## Stage 1 — Discovery

发现可能形成 iMS Opportunity 的公开外部 Signal。

↓

## Stage 2 — Qualification

验证该 Signal / Opportunity Hypothesis 是否真正形成值得继续投入资源的 iMS Opportunity。

↓

### PASS → Stage 3

## Stage 3 — Enrichment

补充：

- Account
- Organization
- Contact
- Buying Role
- Installed Base
- Hach 内部商业历史
- 决策链
- EPC / SI / 设计院关系
- 关键联系人
- 其他需要进一步丰富的信息

↓

## Stage 4 — Outreach

形成针对客户、项目、合作伙伴和关键人的具体触达策略。

↓

## Stage 5 — Orchestration

持续推进 Opportunity、协调 Sales / Marketing / Agent、跟踪状态，并将新发现回流前序阶段。

---

# 2. DuMate Municipal Radar 当前职责

当前 Municipal Radar 周期任务负责：

# Stage 1 Discovery + Stage 2 Qualification

即：

Public Signals  
↓  
Discovery  
↓  
iMS Opportunity Hypothesis  
↓  
Qualification  
↓  
PASS / WATCH / REJECT

Stage 1 和 Stage 2 不需要拆成两个周期任务。

由于 Municipal Radar 每日运行、单次 Lead 数量有限，允许在同一次 Radar 周期内对重点 Lead 完成较完整的 Qualification。

但是：

## 不要越界执行 Stage 3。

Stage 2 可以指出：

- 需要确认哪些 Account 信息
- 需要什么 Installed Base 信息
- 需要找什么角色
- 需要确认哪个 EPC / SI / 设计院
- 需要哪些内部商业信息

但不要在 Radar 中无限展开联系人搜索和 Contact Enrichment。

这些属于后续 Stage 3 Municipal Contact / Enrichment 周期任务。

---

# 3. Stage 2 Qualification Decision

每条进入 Qualification 的 Lead 必须明确给出：

# PASS / WATCH / REJECT

## PASS

已有足够证据支持：

> 这是一个值得进一步投入 Stage 3 Enrichment 资源的 iMS Opportunity。

PASS：

→ `ready_for_stage3 = true`

→ 进入 Stage 3 Enrichment。

---

## WATCH

存在合理的 iMS Opportunity Hypothesis，

但：

- 关键证据不足
- 项目时点尚早
- iMS Problem 尚未充分显性化
- 平台/竞争覆盖情况不清楚
- Instrument Installed Base 不明确
- Entry Window 尚未形成

WATCH：

→ 留在 Stage 1+2 Radar Pool  
→ `ready_for_stage3 = false`

后续每日 Radar 持续观察。

必须给出：

### Revisit Trigger

说明出现什么新事实时应该重新 Qualification。

---

## REJECT

项目或事件可能完全真实，甚至项目规模很大，

但目前：

> 没有形成值得投入后续资源的 iMS Opportunity。

REJECT：

→ 不进入 Stage 3  
→ `ready_for_stage3 = false`

如果未来存在重新进入的可能，必须记录 Revisit Trigger。

---

# 4. Human Report 与 Machine Interface 分离

这是本次升级非常重要的架构原则。

## Human-readable Report

可以明显升级。

目标：

- 更完整
- 更详细
- 更容易理解 Opportunity Formation
- Qualification 判断更加突出
- 每条重点 Lead 可以展开 1–3 页

但是：

## Machine-readable Output

必须保持向后兼容。

现有：

- Lead ID
- daily JSON
- latest.json
- 现有字段
- 文件位置
- 下游读取方式

原则上不得破坏。

不要为了新版 Human Report 而重新设计整个 JSON Schema。

---

# 5. 第一页必须展示五阶段 Workflow

从 v3.3 开始，每份 Municipal Radar 报告第一页必须首先说明：

# iMS Municipal Opportunity Radar
## Stage 1 Discovery + Stage 2 Qualification

然后视觉化展示：

Stage 1  
**Discovery**

↓

Stage 2  
**Qualification**

↓

Stage 3  
**Enrichment**

↓

Stage 4  
**Outreach**

↓

Stage 5  
**Orchestration**

并明显标记：

> **DuMate Municipal Radar Current Scope = Stage 1 + Stage 2**

同时说明：

- PASS → Stage 3
- WATCH → 留在 Radar Pool
- REJECT → Stop / Revisit when triggered

目的是让任何 Human Reviewer 打开第一页就理解：

1. 这份 Radar 在整个 iMS GTM Workflow 中的位置；
2. 今天的 Lead 接下来应该流向哪里。

---

# 6. 第一页 Executive Summary

Workflow 下方展示：

# Today's Executive Summary

至少包含：

- Scan Date
- Public Signals Scanned
- New Signals
- Existing Leads with New Facts
- Leads Qualified Today
- PASS 数量
- WATCH 数量
- REJECT 数量
- 今日最重要的 1–3 个 iMS Opportunities
- Immediate Next Actions

不要只告诉 Reviewer：

“今天找到多少新闻”。

必须告诉 Reviewer：

> 今天有哪些 iMS Opportunities 值得采取行动？

---

# 7. 第一页 / 报告前部增加 iMS Qualification Board

必须增加：

# iMS Qualification Board

建议：

| Lead ID | Account / Project | Formation Stage | iMS Fit | Entry Window | Decision | Next Action |
|---|---|---|---|---|---|---|

Decision 必须明显显示：

**PASS**

**WATCH**

**REJECT**

Human Reviewer 应能够只看这一页就知道：

- 今天哪些机会值得推进
- 哪些继续观察
- 哪些停止投入
- 下一步应该做什么

---

# 8. Lead ID — 严格保持现有格式

继续沿用 Municipal Radar 现有 Lead ID 格式。

# 不得因为进入 Qualification 而重新编号。

同一个 Lead 从：

Discovery  
→ Continuous Tracking  
→ New Fact  
→ Qualification  
→ PASS / WATCH  
→ Stage 3

始终使用同一个 Lead ID。

Lead ID 是整个 Opportunity Lifecycle 的主索引。

如果已有编号：

继续使用原编号。

不要因为 v3.3 升级而重建 Lead ID。

---

# 9. 每条重点 Lead 允许 1–3 页

与批量 Qualification 任务不同：

Municipal Radar 是每日周期任务，单日数据量有限。

因此：

# 报告继续追求完整和详细。

不要为了提高吞吐量，把每条 Lead 压缩成几行。

建议：

### 约 1 页

简单 WATCH / 信息相对有限。

### 约 2 页

普通 PASS 或复杂 WATCH。

### 最多约 3 页

战略级 PASS、复杂 Account、多 Opportunity Hypotheses、连续出现重要 New Facts 的 Lead。

不要机械凑页数。

但不要为了压缩篇幅删除：

- Public Facts
- Evidence
- Opportunity Timeline
- Logic Chain
- Qualification reasoning
- Competitive context
- Missing Evidence
- Continuity
- Next Action

---

# 10. 每条 Lead 的标准结构

每条重点 Lead 使用以下结构。

---

## A. Lead Header

必须包含：

- Lead ID
- Account / Project
- Location
- First Seen
- Continuity Days
- Today's Status
- New Fact / No Change
- Current GTM Stage
- Radar Signal Score
- iMS Qualification Decision

其中：

# iMS Qualification Decision

必须明显突出。

---

# 11. What Changed / Public Facts

完整说明：

> 发生了什么？

严格区分：

## Public Facts

有公开来源支持的事实。

## AI Judgment

基于公开事实进行的分析和推断。

不得把 AI 推断写成事实。

继续保留：

- source
- first_seen
- continuity
- today's new fact

等现有机制。

---

# 12. Opportunity Formation Timeline

每条 Lead 都应尽可能判断当前 Opportunity Formation Position。

参考：

Policy / Regulation  
↓  
Planning  
↓  
Funding  
↓  
Feasibility / Design  
↓  
Tender Preparation  
↓  
Tender  
↓  
Procurement  
↓  
Construction  
↓  
Commissioning  
↓  
Operation / O&M

明确回答：

### Current Position

当前项目处于哪个阶段？

### Best iMS Entry Point

iMS 最理想的介入点在哪里？

### Current Entry Status

从以下选择最适合的一项：

- Too Early
- Entry Window Forming
- Entry Window Open
- Urgent
- Late
- Post-project / O&M Opportunity
- Unknown

不要仅仅判断项目是不是“好项目”。

必须判断：

> iMS 现在还有没有进入窗口？

---

# 13. iMS Opportunity Hypothesis

必须形成完整 Logic Chain：

Customer / Project Change  
↓  
Digital / Operational Change  
↓  
Instrument / Data / Maintenance Problem  
↓  
iMS Need  
↓  
iMS Use Case  
↓  
Potential Commercial Opportunity

明确列出：

# iMS Use Case

例如：

- Multi-site Management
- Instrument Asset Management
- Instrument Health Diagnostics
- Data Quality
- Lifecycle Management
- Digital Operations
- Compliance / Monitoring Management

但：

Use Case 必须由公开事实和合理逻辑支持。

禁止为了匹配 iMS 强行制造 Use Case。

---

# 14. ★ iMS QUALIFICATION ★

这是每条 Lead 最重要的 Human Review 区域之一。

# 必须视觉高亮。

禁止把 Qualification 淹没在普通正文中。

如果输出 PDF：

优先使用：

- 独立区域
- 边框
- 底色
- 加粗标题
- 表格
- 明显的 PASS / WATCH / REJECT 标签

让 Human Reviewer 可以快速定位 Qualification。

至少必须高亮：

- iMS Qualification Decision
- iMS Fit
- Opportunity Formation Position
- iMS Use Case
- Entry Window
- Key Evidence
- Missing Evidence
- Revisit Trigger
- Next Best Action
- Stage Transition

---

# 15. Qualification — Problem Fit

回答：

> 客户是否正在形成 iMS 可以解决的真实问题？

从以下选择：

- Confirmed
- Strongly Inferred
- Weakly Inferred
- Unknown

说明判断依据。

---

# 16. Qualification — Instrument / Asset Relevance

判断是否存在：

- 大规模在线仪表
- Multi-site
- 多品牌设备
- 新增仪表部署
- Existing Installed Base
- 高运维复杂度
- 数据质量问题
- 校准问题
- 故障管理
- 生命周期管理
- 多站点协同运维

不要把“有仪表”直接等同于“有 iMS Opportunity”。

---

# 17. Qualification — iMS Fit

明确：

# iMS Fit = High / Medium / Low / Unknown

并解释为什么。

重点判断：

> iMS 能否解决这个 Account / Project 正在形成的实际问题？

---

# 18. Qualification — Existing Platform / Competitive Coverage

必须主动判断已有：

- SCADA
- DCS
- 智慧水务平台
- 设备管理平台
- EAM
- SI 自建系统
- Instrument Vendor Digital Platform

是否已经覆盖 iMS 核心价值。

尤其关注：

- Instrument Health Diagnostics
- Asset Management
- Lifecycle
- Data Quality
- Multi-site Management
- Maintenance Workflow

大型智慧水务项目并不自动等于 iMS Opportunity。

如果已有平台充分覆盖相同问题：

应降低 Qualification。

---

# 19. Qualification — Hach + iMS Combination

判断是否存在：

Hach Instrument  
+  
iMS

组合价值。

但必须遵守：

> 只能证明存在 Hach 仪表采购机会，
> 不能自动推导出 iMS Opportunity。

必须独立判断 iMS Fit。

---

# 20. Qualification — Entry Window

必须明确：

- Current Project Stage
- Best iMS Entry Point
- Estimated Entry Window
- Current Window Status

重点回答：

> 如果 Sales / Marketing 现在开始行动，是太早、正好，还是已经太晚？

---

# 21. Qualification — Ecosystem / Route

识别可能影响 iMS 进入的：

- Owner
- Water Utility
- Design Institute
- EPC
- System Integrator
- O&M Provider
- Instrument Supplier
- Digital Platform Provider

但：

# 不要在 Stage 2 深度展开联系人搜索。

Stage 2 只需要回答：

> Stage 3 应该重点 Enrich 哪些组织 / Role / Relationship？

具体联系人搜索由后续 Municipal Contact / Enrichment 周期任务完成。

---

# 22. Missing Evidence

继续沿用现有 `to_verify` 思路。

例如：

- customer_identity
- installed_base
- commercial_history
- ims
- account_sales
- platform_capability
- instrument_brand
- project_specification
- EPC / SI
- O&M model

但是：

不得因为存在 Missing Evidence 就停止 Qualification。

基于现有证据给出当前最合理的：

PASS / WATCH / REJECT。

---

# 23. Qualification Decision — 强制结论

每条 Lead 最后必须明确：

# iMS Qualification Decision

## PASS / WATCH / REJECT

并给出：

### Why

2–5 条最重要理由。

不要只给 Score。

---

## PASS

必须回答：

> 为什么现在值得投入 Stage 3 Enrichment 资源？

并输出：

`ready_for_stage3 = true`

---

## WATCH

必须回答：

> 当前为什么还不能进入 Stage 3？

并强制增加：

# Revisit Trigger

例如：

- 招标文件发布
- 仪表清单公开
- EPC 中标
- 平台供应商确认
- 新一轮采购
- 项目进入设备采购
- O&M 招标
- Installed Base 获得确认
- 新数字化平台建设
- 新的客户组织变化

输出：

`ready_for_stage3 = false`

---

## REJECT

必须回答：

> 为什么这个真实项目目前不是值得推进的 iMS Opportunity？

如果未来可能重新进入：

记录 Revisit Trigger。

输出：

`ready_for_stage3 = false`

---

# 24. Radar Score 继续保留，但重新明确含义

现有 Score 可以继续使用。

但在 Human Report 中明确称为：

# Radar Signal Score

它衡量：

> 这个公开 Signal 有多值得 Radar / Qualification 关注？

它不是最终 Opportunity Score。

因此：

# High Radar Score ≠ Automatic PASS

真正的 Stage 2 输出是：

PASS / WATCH / REJECT。

---

# 25. Continuity / Freshness

继续保留并强化：

- first_seen
- continuity days
- new fact
- no change

Existing Lead 出现 New Fact：

不要生成新的重复 Lead。

应该：

Existing Lead  
↓  
New Fact  
↓  
Update Opportunity Formation  
↓  
Re-run Qualification  
↓  
Update Decision if necessary

允许：

WATCH → PASS

PASS → WATCH

WATCH → REJECT

REJECT → WATCH / PASS

只要有新的证据支持变化。

---

# 26. Stage 2 → Stage 1 Feedback Loop

Qualification 过程中可能发现：

- 一个 Signal 实际包含多个项目
- Account 下出现新的独立项目
- 原项目主体识别错误
- 出现新的 Opportunity Formation Signal
- 新政策 / 招标 / 建设事件值得独立追踪
- 需要扩大某个方向的 Discovery

此时不要在当前 Lead 中无限扩写。

增加：

# Stage 1 Feedback

允许记录：

- New Signal Candidate
- Entity Split Candidate
- New Project Candidate
- Data Correction
- Search Expansion Candidate

交给后续 Stage 1 Radar 周期处理。

只有确实属于独立 Opportunity 的内容：

才按照现有 Lead ID 规则创建新 Lead。

---

# 27. Stage Transition

每条 Lead 最后必须明确：

### Current Stage

Stage 1 + Stage 2

### Decision

PASS / WATCH / REJECT

### Next Stage

PASS:

→ Stage 3 Enrichment

WATCH:

→ Remain in Stage 1/2 Radar Pool

REJECT:

→ Stop Active Processing / Retain Revisit Trigger

---

# 28. Stage 3 Handoff — Critical

Municipal Radar 的输出是后续：

# Municipal Contact / Enrichment

周期任务的数据源。

因此 Stage 2 PASS 后必须提供一个简洁、结构化的：

# Stage 3 Handoff

至少包含：

- lead_id
- account / project
- qualification_decision
- ims_fit
- ims_use_cases
- opportunity_hypothesis
- opportunity_formation_stage
- entry_window
- missing_evidence
- organizations / roles_to_enrich
- next_best_action
- ready_for_stage3

Stage 3 不应该重新执行 Stage 1/2 Qualification。

它应该能够直接理解：

> 为什么这条 Lead 已经 PASS，以及接下来应该 Enrich 什么。

---

# 29. Downstream Interface Compatibility — CRITICAL

这是本次升级的硬性要求。

Municipal Radar Stage 1+2 输出同时是后续 Stage 3 Municipal Contact / Enrichment 周期任务的数据源。

因此：

## 不得破坏现有数据接口。

必须：

1. 继续生成现有 daily JSON；
2. 继续生成现有 latest.json；
3. 保持现有 Lead ID 格式；
4. 保持现有字段向后兼容；
5. 不得删除 Stage 3 现有任务可能依赖的字段；
6. 不得随意重命名现有字段；
7. 不得随意改变现有文件位置；
8. Existing Lead 不因重新 Qualification 而重新编号。

Human-readable PDF / MD 可以采用新版详细 Qualification 格式。

Machine-readable Schema：

# 必须优先保持向后兼容。

---

# 30. Stage 2 新增 Machine-readable Fields

在不破坏现有 Schema 的前提下，可以新增：

- current_stage
- qualification_decision
- ims_fit
- ims_use_cases
- opportunity_hypothesis
- opportunity_formation_stage
- entry_window
- missing_evidence
- revisit_trigger
- next_best_action
- stage3_handoff
- ready_for_stage3

其中：

### PASS

`qualification_decision = PASS`

`ready_for_stage3 = true`

### WATCH

`qualification_decision = WATCH`

`ready_for_stage3 = false`

### REJECT

`qualification_decision = REJECT`

`ready_for_stage3 = false`

---

# 31. Stage 3 Consumption Rule

后续 Municipal Contact / Enrichment 周期任务应该能够在稍后运行时：

读取现有 Stage 1+2 Machine-readable Output

↓

通过：

`ready_for_stage3 = true`

筛选需要进入 Stage 3 的 Lead

↓

读取：

`stage3_handoff`

↓

开始 Enrichment

而不需要重新执行 Stage 1/2。

因此：

# Stage 1+2 输出必须是稳定、明确、可被下游 Agent 消费的数据接口。

---

# 32. 保留 Radar Context Intelligence

继续保留：

- Industry Intelligence
- Ecosystem Intelligence
- Policy Intelligence
- Competitive Intelligence
- Strategic Accounts

但仍必须遵守：

# iMS-centric

只保留能够帮助判断：

- iMS Opportunity Formation
- Entry Timing
- Competitive Threat
- Ecosystem Route
- Account Change
- iMS Product Positioning

的信息。

不要逐渐演变成泛行业新闻摘要。

---

# 33. Do Not Waste Sales Time 升级

继续保留：

# Do Not Waste Sales Time

这是 Municipal Radar 的重要价值之一。

但与新版 Qualification Workflow 对齐。

每条至少包含：

- Lead / Project
- WATCH 或 REJECT
- Why
- Revisit Trigger
- Expected Revisit Timing（如果能够合理判断）

目标不是简单删除线索。

目标是：

> 把 Sales / Stage 3 资源留给真正值得推进的 iMS Opportunities。

---

# 34. Report Detail Level

不要采用批量 Qualification 的极简输出方式。

Municipal Radar 的周期报告需要：

- 完整
- 详细
- 有证据链
- 有 Opportunity Formation
- 有 Qualification Reasoning
- 有 Human-readable 解释
- 有连续追踪价值

每个重点 Lead：

# 允许 1–3 页。

优先保证：

> Human Reviewer 能真正理解“为什么这是 / 不是一个 iMS Opportunity”。

而不是单纯追求报告短。

---

# 35. Final Quality Gate

报告完成前必须逐项检查。

## Workflow

- 第一页是否展示五阶段 Workflow？
- 是否明确 DuMate Municipal Radar = Stage 1 + Stage 2？
- PASS 是否明确进入 Stage 3？

## iMS Centricity

- 每个 PASS 是否真的是 iMS Opportunity？
- 是否存在因为项目金额大而误判 PASS？
- 是否存在因为有大量仪表而误判 PASS？
- 是否存在因为“智慧水务”标签而误判 PASS？
- 是否把单纯 Instrument Opportunity 错当成 iMS Opportunity？

## Qualification

- 每条重点 Lead 是否都有独立、高亮的 ★ iMS QUALIFICATION ★？
- 是否明确 PASS / WATCH / REJECT？
- 是否解释 Why？
- WATCH 是否有 Revisit Trigger？
- PASS 是否明确说明为什么值得 Stage 3？
- 是否给出 Stage 3 Handoff？

## Evidence

- Public Facts 与 AI Judgment 是否分离？
- 关键判断是否有证据支持？
- Missing Evidence 是否明确？
- 是否避免把推断包装成事实？

## Opportunity Formation

- 是否判断当前 Formation Stage？
- 是否判断 Best iMS Entry Point？
- 是否判断 Entry Window？

## Continuity

- 是否沿用原 Lead ID？
- Existing Lead 是否正确更新，而不是重复创建？
- New Fact 是否触发重新 Qualification？
- Decision 改变时是否说明原因？

## Downstream Compatibility

- daily JSON 是否继续生成？
- latest.json 是否继续生成？
- 原字段是否保留？
- Lead ID 是否保持不变？
- PASS 是否正确设置 `ready_for_stage3 = true`？
- Stage 3 是否可以直接消费输出而无需重新 Qualification？

## Human Readability

- 第一页是否能快速理解今天发生了什么？
- Qualification Board 是否清楚？
- 每条 Lead 的 Qualification 是否明显高亮？
- 重点 Lead 是否在合理的 1–3 页内完整表达？
- 是否既详细又避免无意义重复？

如果任何关键项失败：

# 修正后再生成最终报告。

---

# 36. 本轮升级边界

本次 v3.3 的重点是：

**统一 Workflow**
+
**强化 Stage 2 Qualification**
+
**升级 Human Report**
+
**建立 PASS / WATCH / REJECT Gate**
+
**建立 Stage 1 ↔ Stage 2 Feedback Loop**
+
**建立稳定 Stage 2 → Stage 3 Handoff**

本次不要大规模重写已经有效的 Radar 搜索策略。

先让现有 Discovery Engine 在新版 Workflow 中运行。

后续根据实际运行数据观察：

- PASS Precision
- WATCH → PASS Conversion
- REJECT Quality
- Stage 3 Handoff Quality
- Sales Feedback
- Opportunity Formation Timing

再决定是否需要调整 Discovery Engine。

---

# 37. Success Criterion

最终目标不是：

“每天找到更多市政项目。”

也不是：

“生成更长的 Radar 报告。”

而是：

# 更早、更准确地发现正在形成的 iMS Opportunities；

# 对它们进行足够深入、可解释、可审计的 Qualification；

# 让真正值得推进的 PASS Lead 自动、稳定地进入 Stage 3 Enrichment；

# 同时避免 Sales 和后续 Agent 在低价值项目上浪费时间。

请从下一次 Municipal Radar 周期开始应用本增量升级。