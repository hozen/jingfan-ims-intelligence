iMS Industrial Radar — Incremental Upgrade

Demand-First / PULL Qualification v1

这是对现有 iMS Industrial Radar Stage 1 + Stage 2 周期任务的增量升级。

不要重构现有任务。

保持现有：

* Stage 1 Discovery
* Stage 2 Qualification
* 线索编号体系
* PASS / WATCH / REJECT
* 每条线索 1–3 页的详细输出
* Qualification 高亮
* PDF 输出结构
* 与 Stage 3 Enrichment 的数据接口/输出位置

全部不变。

本次只升级一个核心问题：

不再从"iMS 能做什么"反推"客户需要什么"。

新的 Qualification 必须：

Demand First.

⸻

1. 为什么升级

过去的软件产品实践带来一个重要 lesson：

技术上能够实现、数据上能够分析、甚至模型预测得很准确，并不代表存在真实 Demand。

一个典型失败模式：

我们拥有数据
→ 我们能够分析/预测
→ 我们开发 Feature
→ 我们寻找客户使用场景。

这种 Supply-driven Innovation 很容易产生：

Technically Interesting, Commercially Weak

的产品。

工业 Radar 必须主动避免重复这个错误。

⸻

2. Stage 1 与 Stage 2 的边界保持不变

Stage 1 — Discovery

继续寻找真实外部信号，例如：

* 招标
* 中标候选人
* 环评
* 扩建
* 技改
* 新产线
* 自动化升级
* 环保整改
* 数字化项目
* 设备更新
* 事故
* 合规要求
* 降本项目
* 人员变化
* 运维变化

Stage 1 的目标仍然是：

找到可能值得 Qualification 的真实 Project / Change / Trigger。

⸻

3. Stage 2 Qualification：新增 PULL

每条候选线索在判断 iMS Fit 之前，必须先完成：

PULL Demand Qualification

⸻

P — Project

回答：

客户到底正在试图完成什么事情？

不要写：

* 客户可能需要数字化；
* 客户可能需要设备管理；
* 客户可能需要预测性维护；
* 客户可能需要 iMS。

这些都是 Solution-side 推断。

应该尽可能描述真实 Project：

例如：

* 新建某生产线；
* 污水站无人化改造；
* 降低某项运行成本；
* 满足新的排放要求；
* 减少人工巡检；
* 解决频繁设备故障；
* 提高某工艺稳定性；
* 新建中央控制中心；
* 替换老旧在线仪表；
* 解决某次事故暴露的问题。

必须引用 Evidence。

如果无法确认：

P Confidence = LOW

⸻

U — Unavoidable

回答：

为什么客户必须做？为什么是现在？

寻找真正的 forcing function：

* Regulation
* Compliance
* Safety
* Production requirement
* Quality requirement
* Customer requirement
* Cost reduction
* Labor shortage
* Capacity expansion
* Equipment obsolescence
* Accident
* Audit finding
* Corporate KPI
* Sustainability target
* Budget already approved
* Deadline
* Mandatory upgrade

区分：

Must-have

不解决会产生明确后果。

Should-have

有明显价值，但可以延期。

Nice-to-have

改善体验，但没有明确 urgency。

如果找不到 Unavoidable：

不要因为 iMS Fit 很高就直接 PASS。

⸻

4. L — Limitations

回答：

客户今天怎么解决这个问题？为什么现有办法不够？

这是 Qualification 中必须新增的重点。

寻找：

* Manual inspection
* Excel
* Paper record
* DCS / SCADA
* Existing software
* Instrument local display
* Service engineer
* Distributor service
* Preventive maintenance
* Reactive maintenance
* Laboratory testing
* Existing automation system
* Third-party platform
* Other workaround

然后判断：

Existing workaround 到底有什么 Limitation？

例如：

* 太慢；
* 太贵；
* 太依赖人工；
* 数据孤岛；
* 无法跨设备；
* 无法形成 action；
* 无法提前发现；
* 无法满足 compliance；
* 无法形成闭环；
* 无法远程管理；
* 数据质量不足；
* 没有设备层信息；
* 缺乏专业 know-how。

如果不知道客户目前如何解决：

明确写：

Current workaround unknown — requires validation.

禁止自行想象。

⸻

5. L — Leverage

最后才允许问：

iMS + Instrument 能带来什么现有方法做不到，或者明显做得更好的结果？

不要只写 Feature：

* Dashboard
* Alarm
* Trend
* Remote monitoring
* Equipment management
* Predictive maintenance

必须继续往后推：

Data → Insight → Decision → Action → Outcome

例如：

仪表状态数据
→ 发现异常趋势
→ 判断需要维护
→ 提前安排 service
→ 避免非计划停机

才是完整价值链。

如果只能写到：

Data → Dashboard / Insight

而无法回答：

"So what? 客户接下来会做什么？"

则降低 Qualification Score。

⸻

6. 新增硬规则：No Action, No Feature

以后所有 iMS Fit 判断执行：

No Action, No Feature.

如果一个 iMS Feature 无法明确连接：

Customer Problem
→ Decision
→ Action
→ Measurable Outcome

不得因为"技术上可以做"而作为强 Qualification Evidence。

⸻

7. Evidence 与 Assumption 必须分开

PULL 四项分别标注：

FACT — 有明确来源支持。

INFERENCE — 基于事实合理推断。

UNKNOWN — 当前没有证据。

严禁把 INFERENCE 写成 FACT。

特别禁止：

"该客户有大量仪表，因此一定存在设备管理需求。"

或者：

"该项目涉及数字化，因此适合 iMS。"

这属于 Supply-driven inference。

⸻

8. 新增 PULL Score

每条线索增加一个轻量评分：

Dimension	Score
Project clarity	0–5
Unavoidable / urgency	0–5
Existing solution limitation	0–5
iMS leverage	0–5

PULL Score = /20

建议解释：

16–20	Strong Demand Evidence
11–15	Promising, but requires validation
6–10	Weak Demand Evidence
0–5	Mostly Supply-side speculation

PULL Score 不替代现有 Qualification Score。

它是一个新的 Demand Quality Gate。

⸻

9. PASS / WATCH / REJECT 升级

PASS

不仅需要 iMS Fit。

还必须存在：

Real Project + Meaningful Unavoidable + Evidence of Limitation + Credible iMS Leverage

⸻

WATCH

特别适用于：

iMS 看起来很适合，但 Demand Evidence 不够。

这种线索不要为了提高 PASS 数量而升级。

WATCH 应明确写：

下一步需要验证什么？

例如：

* 客户现在如何巡检？
* 是否已有 SCADA？
* 当前 downtime 是否造成真实损失？
* 是否存在总部 KPI？
* 谁拥有这个问题？
* 有没有预算？
* 为什么今年必须解决？

这些问题未来可以直接进入 Stage 3 / Sales VOC。

⸻

REJECT

包括：

* 只有行业相关性；
* 只有设备相关性；
* 只有"数字化"概念；
* 只有 iMS Feature Match；
* 没有 Project；
* 没有 Pain；
* 没有任何 forcing function；
* iMS 不会改变客户 Decision / Action / Outcome。

⸻

10. 每条线索新增一个 PULL Box

在现有 Stage 2 Qualification 高亮区域增加：

DEMAND / PULL

P — Project
客户正在做什么？

U — Unavoidable
为什么必须做？为什么现在？

L — Limitations
现在怎么做？为什么不够？

L — Leverage
iMS + Instrument 如何改变 Decision / Action / Outcome？

PULL Score: XX / 20

Evidence Quality: HIGH / MEDIUM / LOW

Key Unknown:
最重要的一个未知问题。

Next Validation Question:
如果 Sales 只能问客户一个问题，应该问什么？

⸻

11. 特别关注工业场景中的 Repeatable Demand

工业 Radar 不仅寻找单个 Opportunity。

开始识别：

Repeatable PULL Pattern

如果不同客户反复出现相同：

Project
+
Unavoidable
+
Limitation
+
Leverage

必须标记：

REPEATABLE DEMAND SIGNAL

例如：

如果连续多个客户因为相似的：

* 人员减少；
* 运维成本；
* 合规；
* 仪表维护；
* 生产稳定性；
* 水处理成本；
* 数据孤岛；

而产生类似需求，则进入 Weekly Review。

不要急于形成结论。

先积累 Evidence。

⸻

12. 与 Bundle Pricing 的关系

特别观察：

Instrument + iMS Bundle 是否正在对应某种 Repeatable Demand。

不要因为 Bundle 已经产生订单就假设 Product-Market Fit 已成立。

对于发现的相关机会，尝试判断：

客户购买 Bundle 是因为：

A. Software creates independent value
客户明确需要 iMS。

B. Software increases hardware value
iMS 让仪表整体方案更有价值。

C. Pricing incentive
主要因为 Bundle Pricing / Promotion。

D. Sales push
主要由销售推动，客户 Demand 较弱。

E. Unknown

这是未来判断 Bundle GTM 是否真正成立的重要 Evidence。

⸻

13. Weekly Learning Interface

工业 Radar 每次运行除了发现 Opportunity，还承担：

Demand Learning

在报告结尾增加一个简短部分：

What Did We Learn About Demand Today?

只回答：

1. 今天是否发现新的 Strong PULL？
2. 是否出现以前见过的 Repeatable PULL Pattern？
3. 有没有过去认为适合 iMS、但今天因为 Demand Evidence 不足而降级的线索？
4. 今天有没有信息应该改变我们的 iMS Product / GTM 假设？

如果没有：

明确写：

No meaningful new demand learning today.

不要为了填报告制造 Insight。

⸻

14. North Star

Industrial Radar 的目标不是：

找到最多"可能使用 iMS"的工业客户。

而是：

找到正在面对一个重要、真实、必须解决的问题，而且现有方法存在明显不足的客户，再判断 iMS + Instrument 是否能够显著改善其 Decision / Action / Outcome。

永远遵守：

Demand → Product → Solution

而不是：

Product → Solution → Search for Demand

以及：

Never infer demand from what iMS can do.

最终判断一个 Radar 是否越来越聪明，不只是看：

How many leads did we find?

还要看：

What did we learn about why customers buy?
