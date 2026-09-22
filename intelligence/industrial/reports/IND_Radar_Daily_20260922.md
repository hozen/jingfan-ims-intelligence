# iMS Industrial Radar Daily — 2026-09-22（周二）

> Stage 1 Discovery + Stage 2 Qualification (PULL) + Stage 3 Handoff + Stage 4 Enrichment | 证据强化版（本版针对可售性/软件必要性核查改进）

---

## 0. 本期核查结论（为什么改进、改了什么）

针对 9/22 批次手工 verification 的两个核心问题，本版逐条补齐/明确证据边界：

**① iMS 可售性证据（现场有无水质仪表/哈希装机/监测参数/关键参数配套仪表）**
- 公开来源**无法证明任何一条线索存在哈希装机记录**：本轮全网检索哈希品牌装机、仪表数量均无公开证据 → 全部如实标 `UNKNOWN`，不以行业推断冒充事实。
- 但已为每条线索补充：**法定必装参数基准**（重点排污单位 COD/氨氮/pH/流量 强制自动监控，HJ 353-2019）与**行业常规监测参数清单**（标 `INFERENCE`），供手工 verification 时对照现场实际。
- 新增 `instrument_evidence` 字段（hach_evidence / key_parameters / parameters_basis）：给出每条线索应核对的仪表证据点（如设计院技术协议、EPC 供应清单、现场在装仪表、排口数采仪型号）。

**② 软件必要性/项目落地证据（为什么要有软件、ICP 做了什么尝试）**
- 全批次中**仅有 1 条线索（重庆新宙邦）找到 JD/公开声明级软件必要性证据**：集团环保岗 JD 明确『环境监测、环保数据、资料上报』职责 + 互动平台『在线监测系统』声明（FACT）。
- 其余线索的软件必要性均降至 `INFERENCE`（法规义务推导）或 `UNKNOWN`（无公开证据），不再以『iMS 可提供数据闭环』这类万能套话充数。
- 新增 `icp_attempts` 字段：记录 ICP 已做的落地尝试（长电交钥匙 EPC 招标/自控改造、兰花 BOO 运营模式、东煦 AI 检测+低碳清洗、新宙邦一期在线监测验收等），让 qualification 有据可依。

**关键修正**（与 9/22 早班版的差异，均来自联网补证）：
| Signal | 原判断 | 修正后 | 依据 |
|---|---|---|---|
| 01 宿迁镭明 | 晶圆制造→超纯水+Fab级 | 晶圆加工/切割（苏州镭明为激光设备商），水需求规模缩小 | 母公司主业 FACT |
| 02 淮安东煦 | EARLY 环评公示 | **LATE 主体已封顶**（补办环评） | 2026-01 封顶 FACT |
| 03 定边污水厂 | 化工产业区管委会 | 定边县**产业园区**管委会；规模/工艺/联系人落实 | 环评公示 FACT |
| 04 泰兴怡达 | 废水接管『苏伊士』 | 接管**泰兴市工业污水处理有限公司**（官方口径） | 环评公示 FACT |
| 06 长电科技 | GOOD 规划刚批 | **LATE EPC 已定标**（清朗达 316.75 万） | 中标公告 FACT |
| 07 重庆新宙邦 | P3 极早期 | **P2 一期已投产+JD 证据，二期扩容可复制** | 验收+JD FACT |
| 08 兰花煤化工 | 节能改造（LOW） | **全厂废水零排放+BOO 运营**（PULL 8→13） | 环评批复+公告 FACT |

---

## 🔆 今日 Early Opportunities（Early Signal + High/Medium Influence）

### 1. IND-20260922-03 — 定边县产业园区·化工产业园区污水处理厂一期（零排放）★今日最扎实

| 字段 | 内容 |
|---|---|
| **Company/Account** | 定边县产业园区管理委员会（联系人：顾主任/侯工，0912-4223688，495278550@qq.com） |
| **Industry** | 石化/化工 |
| **Location** | 陕西省榆林市定边县 |
| **Project** | 化工产业园区污水处理厂一期：远期 6000m³/d，本期土建 3000m³/d、设备 1500m³/d，占地 29.33 亩 |
| **工艺链** | 隔油→气浮→芬顿氧化→水解酸化→多级A/O→臭氧氧化→高效沉淀→多级除杂→超滤→反渗透→蒸发结晶（零排放+资源化） |
| **Engine** | B (Project/CapEx) |
| **Entry Timing** | **GOOD** — 环评征求意见 9/20-10/9，监测方案可影响 |
| **Influence Window** | **MEDIUM** — 可影响监测点位设计/仪表规格/运营模式 |
| **Priority** | **P2** (PULL 14/20) |
| **Water System Ownership** | B-园区集中处理 |
| **Source** | [定边县政府公示](https://www.dingbian.gov.cn/zfxxgk/fdzdgknr/hjpj/202609/t20260920_2129246.html) |

**PULL Box**
- **P — Project**: 园区污水厂一期含零排放工艺，规模/工艺/联系人全落实 — FACT
- **U — Unavoidable**: 化工园区废水集中处理+零排放+达标排放为法定要求 — FACT
- **L — Limitations**: 园区现有处理能力不足，需新建 — INFERENCE
- **L — Leverage**: iMS 可覆盖进出水+零排放多工艺段在线监测+数据合规 — INFERENCE
- **PULL Score**: 14/20（P5+U4+L2+L3）| **Evidence Quality**: HIGH

**仪表/参数证据（新增）**
- hach_evidence: **UNKNOWN**（无公开哈希装机证据；需经设计院技术协议确认）
- key_parameters: COD / 氨氮 / 总磷 / 总氮 / pH / SS / 电导率-TDS / 浊度 / 氟化物 / 蒸发结晶浓缩液电导率
- parameters_basis: 园区工业废水+零排放工艺标准监测参数（INFERENCE 行业基准）+ HJ353-2019 法定必装（COD/氨氮/pH/流量）
- 数量参考: 零排放（UF/RO/蒸发结晶）系统在线仪表典型 25-50 点位（行业基准，需项目设计确认）

**软件必要性**
- 零排放系统对连续监测+数据归档+环保平台联网要求高，运营期数据管理是标配需求（INFERENCE）；无公开软件采购证据（UNKNOWN）

**Stage 3 Handoff**
- account_owner: 定边县产业园区管理委员会（FACT，联系人顾主任/侯工）
- design_institute: Unknown（环评编制：陕西中环碳能科技有限公司，FACT）
- epc: Unknown — UNKNOWN
- instrument_integrator: Unknown — UNKNOWN
- next_validation_action: **致电顾主任/侯工确认设计院与项目进度；索取环评报告书全文获取监测点位表**

---

### 2. IND-20260922-08 — 山西兰花煤化工·全厂废水零排放技术改造（BOO）★大项目窗口紧

| 字段 | 内容 |
|---|---|
| **Company/Account** | 山西兰花煤化工有限责任公司（兰花科创 600123 控股） |
| **Industry** | 煤化工 |
| **Location** | 山西省晋城市 |
| **Project** | 节能环保升级改造（含全厂废水零排放技改），总投资约 35.5-39.6 亿元；配套污水零排放装置按 **BOO 模式**（建设-拥有-运营）、≥1000m³/h、年运行 8400h（来源单位疑为笔误，以官方为准） |
| **Engine** | B/C (Project/CapEx + Early Signal) |
| **Entry Timing** | **LATE** — 2025-04 环评已批，2026-07 设备管道安装中，规格大概率已冻结 |
| **Influence Window** | **LOW** — 项目级窗口窄；转 BOO 运营方关系+运维期替换 |
| **Priority** | **P3** (PULL 13/20) |
| **Water System Ownership** | A-客户自建自营（配套 BOO 运营方） |
| **Source** | 山西生态环境厅批复 / 兰花科创公告 / 招采公告 |

**PULL Box**
- **P — Project**: 全厂废水零排放技改+BOO 零排放装置，设备安装中 — FACT
- **U — Unavoidable**: 煤化工高盐废水零排放为环评批复硬约束+水资源约束 — FACT
- **L — Limitations**: 设备安装阶段规格已冻结，项目级窗口窄 — FACT
- **L — Leverage**: iMS 可提供零排放多段监测+BOO 运营数据管理+仪表生命周期 — INFERENCE
- **PULL Score**: 13/20（P4+U4+L2+L3）| **Evidence Quality**: HIGH

**仪表/参数证据（新增）**
- hach_evidence: **UNKNOWN**（无公开证据；可通过 BOO 公告/EPC 技术协议确认）
- key_parameters: COD / 氨氮 / 总磷 / 总氮 / pH / 电导率-TDS / 硬度 / 硅 / 浊度 / 蒸发结晶浓缩液浓度
- parameters_basis: 煤化工高盐废水零排放（RO/蒸发结晶）监测参数（INFERENCE 行业基准）
- 数量参考: ≥1000m³/h 零排放系统在线监测点位典型 30-60 个（行业基准）

**软件必要性**
- 零排放+BOO 运营对连续监测、数据归档、达标预警要求高；BOO 合同通常含数据交付义务（INFERENCE 行业基准）

**Stage 3 Handoff**
- account_owner: 山西兰花煤化工有限责任公司（FACT）
- epc: **BOO 运营方待确认**（污水零排放装置 BOO 中标方）— UNKNOWN
- instrument_integrator: Unknown — UNKNOWN
- next_validation_action: **检索废水零排放 BOO 招标公告确认中标方；查环评批复全文获取监测要求**

---

### 3. IND-20260922-07 — 重庆新宙邦·电池化学品二期扩建（一期已投产，JD 证据最全）

| 字段 | 内容 |
|---|---|
| **Company/Account** | 重庆新宙邦新材料有限公司（新宙邦 300037 全资子公司；联系人杨旭 15310841521） |
| **Industry** | 新能源/电池 |
| **Location** | 重庆市长寿区晏家街道化南八支路 5 号（全厂 168 亩） |
| **Project** | 电池化学品二期：新增 20 万吨锂电电解液+5 万吨钠电电解液+0.6 万吨碳酸乙烯酯（一期 10 万吨已投产并通过竣工环保验收） |
| **Engine** | B/C (Project/CapEx + Early Signal) |
| **Entry Timing** | **EARLY** — 二期环评一次公示 9/4，设计未定 |
| **Influence Window** | **MEDIUM** — 一期同址可参照，iMS 可提供与一期基线一致的监测+数据方案 |
| **Priority** | **P2** (PULL 12/20) |
| **Water System Ownership** | D-Unknown（一期污水站+在线监测已建成投运） |
| **Source** | [新宙邦官网](https://www.capchem.com/News_detail/108.html) / 互动平台 / 招聘平台 |

**PULL Box**
- **P — Project**: 二期 20+5 万吨电解液扩建，一期已投产（含污水站+在线监测） — FACT
- **U — Unavoidable**: 电解液生产环保合规+上市公司在线监测制度化（互动平台回应『高标准建设污水处理站、在线监测系统』） — FACT
- **L — Limitations**: 二期水系统方案未明确，需扩容 — INFERENCE
- **L — Leverage**: iMS 可提供一期基线复制+二期扩容+集团环保数据上报管理 — INFERENCE
- **PULL Score**: 12/20（P4+U3+L2+L3）| **Evidence Quality**: MEDIUM-HIGH

**仪表/参数证据（新增）**
- hach_evidence: **UNKNOWN**（一期污水站仪表品牌可通过竣工环保验收报告或现场确认）
- key_parameters: COD / 氨氮 / 总磷 / 总氮 / pH / 电导率 / 氟化物（含氟电解液） / SS
- parameters_basis: 电解液/锂电材料废水监测参数（INFERENCE 行业基准）+HJ353-2019 法定必装

**软件必要性（本批次唯一有 JD 层面 FACT 证据的线索）**
- FACT: 集团环保工程师/专员 JD 明确『项目污水站安装管理跟进和调试』『环境监测、环保数据、资料的上报』职责（招聘平台）
- FACT: EHS 工程师（能碳）JD『收集统计分析集团能源、碳管理、污染物排放数据』
- FACT: 互动平台 2026-05-07『在线监测系统等污染物防治设施』声明

**icp_attempts（ICP 已做尝试）**: 一期污水站+在线监测建成并验收（FACT）；集团持续设置环保数据上报岗（FACT-JD）；EHS 能碳岗收集集团排放数据（FACT-JD）

**Stage 3 Handoff**
- account_owner: 重庆新宙邦新材料有限公司（FACT，联系人杨旭 15310841521）
- design_institute: Unknown（环评编制：重庆环科源博达环保科技有限公司，FACT）
- next_validation_action: **联系杨旭确认二期污水站规划；通过一期竣工环保验收报告获取现有在线监测配置与仪表品牌**

---

### 4. IND-20260922-01 — 宿迁镭明半导体·年产15万片晶圆项目（性质待核）

| 字段 | 内容 |
|---|---|
| **Company/Account** | 宿迁镭明半导体设备有限公司（2026-06-18 成立，注册资本 2000 万；股东苏州镭明激光科技，2026-06-20 对外投资） |
| **Industry** | 半导体/电子 |
| **Location** | 江苏省宿迁市宿城区经济开发区（微电子产业园 2 号厂房） |
| **Project** | 年产15万片晶圆项目——**注意：母公司为激光切割设备商，项目性质更可能是晶圆加工/切割而非 Fab 制造，超纯水规模推断已降级** |
| **Engine** | B/C (Project/CapEx + Early Signal) |
| **Entry Timing** | **GOOD** — 环评受理公示今日（9/22）截止，技术规格未冻结 |
| **Influence Window** | **MEDIUM** |
| **Priority** | **P2** (PULL 12/20) |
| **Source** | [宿迁市生态环境局](http://sthj.suqian.gov.cn/shbj/jsxm/202609/145daaadc23840f38a3a5163420bb336.shtml) / 启信宝 |

**PULL Box**
- **P — Project**: 年产15万片晶圆项目，环评受理今日截止 — FACT
- **U — Unavoidable**: 晶圆加工研磨/切割废水须处理达标 — FACT（水需求规模待核，非 Fab 级）
- **L — Limitations**: 新建项目，水系统方案/设计院未明确 — UNKNOWN
- **L — Leverage**: iMS 可提供废水/冷却水监测+仪表管理+数据闭环 — INFERENCE
- **PULL Score**: 12/20（P4+U3+L2+L3）| **Evidence Quality**: MEDIUM

**仪表/参数证据（新增）**
- hach_evidence: **UNKNOWN**（无公开证据，需经设计院/EPC 技术协议确认）
- key_parameters: pH / 浊度-SS / 电导率 / 温度 / COD（如回用）/ 含氟-含硅专项（视工艺）
- parameters_basis: 晶圆研磨/切割废水常规监测参数（INFERENCE 行业基准）+ 法定自动监控

**软件必要性**
- 排污许可自行监测+数据联网合规是企业义务（法规 Fact）；本项目无公开软件采购/JD 证据（UNKNOWN）

**Stage 3 Handoff**
- design_institute: Unknown（环评技术单位：江苏海雯能碳环境科技有限公司，FACT；≠水系统设计院）
- next_validation_action: **联系宿迁市生态环境局（0527-84396253）或企业核实项目工艺与设计院；推动环评报告全文公开后查水系统方案**

---

## 📋 Tender Monitoring（Sales heads-up only）

### 6. IND-20260922-09 — 远达水务·古雷石化脱硫废水零排放 EPC（增补采购）
- **Company**: 国电投远达水务有限公司 | **Location**: 福建漳州古雷石化基地
- **Signal**: 保温材料增补采购 9/9；EPC 已中标（参考：远达 2025 年中标淮南平圩 2×1000MW 脱硫废水零排放 EPC 1.85 亿）
- **Entry Timing**: LATE — EPC 已中标；**Influence Window**: LOW
- **注意**: 该线索与古雷项目的关联强度需复核（来源为招采聚合站，可信度一般）

### 7. IND-20260922-10 — 古雷石化·水处理装置膜元件利旧改造（运营期）
- **Company**: 福建古雷石化有限公司 | **Location**: 福建漳州古雷石化基地
- **Signal**: 超滤/反渗透膜利旧改造已实施（9/21 福建日报）；园区配套『2026-2029 排海管道水质在线监测设备运行维护』招标（漳州古雷水务，预算 95 万）
- **Entry Timing**: CLOSED — 已实施；**Influence Window**: LOW（Installed Base/Lifecycle）
- **iMS 价值**: 运营期监测补点、膜性能监控、维保数字化（INFERENCE）；园区排海监测维保外包显示第三方运维市场活跃

---

## 📊 其他信号（P3，保留跟踪）

### 8. IND-20260922-04 — 泰兴怡达化学·20万吨环氧丙(乙)烷衍生产品扩建
- 总投资 64199 万元（环保 1600 万，2.5%）；环评拟审批 9/20（南京国环科技编制）；联系人黄总/袁工
- **废水路径**: 厂内新建污水处理装置预处理 → 与原厂废水一起接管**泰兴市工业污水处理有限公司**集中处理
- Entry Timing: GOOD；Influence Window: LOW（自建水系统规模有限，排口自动监控必装）| PULL 11/20
- 仪表证据: hach UNKNOWN；key_parameters: COD/氨氮/总磷/总氮/pH/SS/盐度/石油类
- next: 通过环评拟审批公示获取全本，确认厂内预处理装置规模/工艺与设计院

### 9. IND-20260922-05 — 滨化集团·废盐资源化离子膜烧碱（一期）
- 山东省厅环评批复 9/15；新建 30 万 t/a 离子膜烧碱、再生盐比例 42%；工序含盐场/一次盐水/二次盐水/电解/氯氢处理
- Entry Timing: LATE（环评已批复）；Influence Window: LOW | PULL 8/20
- 仪表证据: hach UNKNOWN；key_parameters: pH/浊度/硬度/硅/电导率/COD/氨氮/SS（盐水精制+废水）
- next: 检索环评批复全文，确认盐水精制与废水系统设计单位

### 10. IND-20260922-02 — 淮安东煦电子材料·12英寸再生晶圆项目（封顶后补办环评）
- **重大修正**: 2025-08-23 开工、2026-01 主体已封顶；9/16 环评公示为『补办』性质 → **Entry Timing 从 EARLY 降为 LATE**
- 再生晶圆月产 40 万片、投资 10 亿；清江浦区华清西路 1 号；环评编制淮安清泰技术咨询
- Influence Window: LOW（设备采购大概率已完成）| PULL 8/20
- 仪表证据: hach UNKNOWN；key_parameters: pH/电导率/SS/COD/氟化物/总氮（视工艺）
- icp_attempts: 媒体提及『AI 视觉检测+低碳清洗工艺』（信息化倾向，INFERENCE）
- next: 访问厂区或通过环评报告表获取水系统供应商信息；询问投产计划

### 11. IND-20260922-06 — 长电科技(宿迁)·55m³/h磨划废水回用系统（EPC 已定标，转渠道关系）

| 字段 | 内容 |
|---|---|
| **Company/Account** | 长电科技(宿迁)有限公司（长电科技 600584 全资子公司，2025 员工 2295 人） |
| **Industry** | 半导体/电子 |
| **Location** | 江苏省宿迁市苏州宿迁工业园区普陀山大道 5 号 |
| **Project** | 55m³/h（1320t/d）磨划废水回用处理系统，交钥匙 EPC |
| **关键进展** | 2026-06-11 招标（交钥匙）；2026-07-14 **中标：上海清朗达环境科技有限公司，316.75 万元**（标段 CR05909000120260611GC0015）；9/16 规划许可批后（土建开工）；9/1 厂区安防自控改造谈判采购 |
| **Engine** | C (Early Signal/Customer Problem) |
| **Entry Timing** | **LATE** — EPC 已定标，规格由总包掌握 |
| **Influence Window** | **LOW** — 项目级窗口关闭；转 EPC 关系+厂级数据平台+运维期 |
| **Priority** | **P3** (PULL 10/20) |
| **Source** | 中标公告 / 园区管委会 / 企查查 |

**PULL Box**
- **P — Project**: 55m³/h 磨划废水回用系统，EPC 已定标（清朗达 316.75 万） — FACT
- **U — Unavoidable**: 半导体磨划废水须回收处理，环保合规 — FACT
- **L — Limitations**: 交钥匙 EPC 已定标，业主直接采购窗口关闭 — FACT
- **L — Leverage**: iMS 可提供运营期仪表替换+厂级水务数据平台（对接 9/1 自控改造） — INFERENCE
- **PULL Score**: 10/20（P4+U3+L1+L2）| **Evidence Quality**: HIGH（招标中标全流程可查）

**仪表/参数证据（新增）**
- hach_evidence: **UNKNOWN**（可通过 EPC 总包清朗达技术协议确认仪表品牌）
- key_parameters: pH / SS-浊度 / 电导率 / COD / 总铜-总镍（磨划后道）/ 氟化物（视工艺）
- parameters_basis: 半导体磨划废水回用监测参数（INFERENCE 行业基准）+ 回用水标准 GB/T19923

**软件必要性/icp_attempts（本线索的落地证据）**
- FACT: 交钥匙合同含调试/培训/竣工资料移交（隐含数据系统交付）
- FACT: 9/1『厂区安防自控改造』谈判采购 = 厂级数字化推进的直接证据
- FACT: 近期招聘『环保专员』（6000 以下，11 天前；无线索级水处理专岗 → 按 JD 纪律标 UNKNOWN/LOW）

**Stage 3 Handoff**
- epc: **上海清朗达环境科技有限公司**（FACT，2026-07-14 中标 316.75 万元）
- next_validation_action: **通过清朗达技术协议确认仪表品牌；调研厂区安防自控改造是否含水务数据管理**

---

## 📈 汇总统计

### Priority 分布
| Priority | 数量 |
|---|---|
| P1 | 0 |
| P2 | 3（定边/新宙邦/镭明） |
| P3 | 5（兰花/泰兴/滨化/东煦/长电） |
| Tender Monitoring | 1（远达古雷） |
| P3-Lifecycle | 1（古雷石化） |

### PULL Score 分布（重算后）
| Range | 数量 | 明细 |
|---|---|---|
| 11-15 | 5 | 定边14 / 兰花13 / 新宙邦12 / 镭明12 / 泰兴11 |
| 6-10 | 5 | 长电10 / 滨化8 / 东煦8 / 古雷7 / 远达6 |
| 0-5 | 0 | — |

### Entry Timing / Influence Window 分布
| Timing | 数量 | | Window | 数量 |
|---|---|---|---|---|
| EARLY | 1（新宙邦） | | MEDIUM | 3（定边/新宙邦/镭明） |
| GOOD | 3（定边/镭明/泰兴） | | LOW | 7 |
| LATE | 5（东煦/滨化/兰花/长电/远达） | | | |
| CLOSED | 1（古雷） | | | |

### Search Bias Check
| 类别 | 数量 | 占比 |
|---|---|---|
| Early Signal（环评一次公示/征求意见） | 4 | 40% |
| Pre-Tender（环评受理/拟审批） | 2 | 20% |
| Tender（EPC 中标/增补采购） | 1 | 10% |
| Awarded/Operating（已批复/已封顶/已实施） | 3 | 30% |
| **Tender + Awarded** | **4** | **40%** |

✅ **Search Bias Check PASS** — Tender+Awarded = 40% < 50%。

### Quality Gate（销售今天知道还能影响什么）
- **可影响（今天行动）**: 定边（联系顾主任确认设计院，赶在征求意见窗口内输入监测要求）、新宙邦（联系杨旭，一期基线上门复制）、镭明（环评今日截止，核实性质+设计院）
- **只能转关系**: 长电（EPC 已定标→清朗达渠道关系+厂级平台）、兰花（BOO 中标方渠道）、东煦（运营期）、泰兴/滨化（设计院/EPC 关系）
- **仅监控**: 远达古雷（增补采购）、古雷石化（运营期利旧）

---

## 🔄 Stage 3 完整输出摘要（三字段校验 10/10 ✅）

| Signal ID | account_owner | design_institute | epc | instrument_integrator | 今日优先验证动作 |
|---|---|---|---|---|---|
| 03 定边 | 产业园区管委会(FACT) | Unknown(环评:陕西中环碳能) | Unknown | Unknown | 致电顾主任确认设计院+监测点位表 |
| 08 兰花煤化工 | 兰花煤化工(FACT) | Unknown | **BOO运营方待确认** | Unknown | 检索BOO招标确认中标方 |
| 07 新宙邦 | 重庆新宙邦(FACT) | Unknown(环评:重庆环科源博达) | Unknown | Unknown | 联系杨旭确认二期污水站+一期仪表品牌 |
| 01 宿迁镭明 | 镭明半导体(FACT) | Unknown(环评:江苏海雯能碳) | Unknown | Unknown | 核实工艺性质+设计院 |
| 06 长电宿迁 | 长电科技宿迁(FACT) | Unknown | **上海清朗达(FACT)** | Unknown(EPC分包) | 经EPC确认仪表品牌+自控改造范围 |
| 04 泰兴怡达 | 泰兴怡达(FACT) | Unknown(环评:南京国环) | Unknown | Unknown | 环评全本→预处理装置规模/工艺 |
| 05 滨化 | 滨化集团(FACT) | Unknown | Unknown | Unknown | 批复全文→盐水/废水设计单位 |
| 02 淮安东煦 | 东煦电子(FACT) | 淮安清泰(FACT,环评) | Unknown | Unknown | 水系统供应商+投产计划 |
| 09 远达古雷 | 远达水务(FACT) | Unknown | 远达水务(FACT) | Unknown | 复核与古雷项目关联+仪表品牌 |
| 10 古雷石化 | 古雷石化(FACT) | N/A | N/A | Unknown | 现有监测配置+运维模式 |

---

## 🔄 Cross-Lead Insight（跨线索洞察，替代单条统计）

**1. 本项目批次的核心证据缺口是结构性的，非个别线索问题**
- 10 条线索中哈希装机证据全部 UNKNOWN；软件必要性 JD 证据仅新宙邦 1 条。这不是搜索不努力，而是公开信息天然不包含『在装仪表品牌』这种运营细节——**哈希与 iMS 的验证必须下沉到设计院技术协议/EPC 供应清单/现场访谈三层**，请在手工 verification 时按此路径核验。

**2. 可售性分层：三类线索，对应三种验证动作**
- A 类（业主直购+规格未冻结）: 定边、新宙邦、镭明 → 设计院技术协议/环评报告书是主证据源
- B 类（EPC/BOO 总包采购）: 长电（清朗达）、兰花（BOO 方）→ 转向总包/运营方渠道，业主端无法直接推动
- C 类（运营期）: 东煦、古雷、远达 → 现场在装仪表普查是唯一路径

**3. BOO/BOT 第三方运营成为软件采购方** — 兰花 BOO 零排放+古雷园区排海监测维保外包，均指向『运营服务商』是新的 ICP 类型，iMS 的数据管理价值在长期托管场景最容易被验证。

---

## 📦 Stage 4 合并结果

Stage 4 合并结果：新增 enriched lead 10 条，评分分布 **5 分 10 条 / 4 分 0 条**，缺失项：无。enriched master 总计 212 条（+10），leads-data.json 总计 239 条（+10）。全库评分分布 5分129 / 4分87 / 3分18 / 2分5，0-3分仅 23 条历史记录无回归。

> 修正说明（12:55 复查）：首轮合并时 10 条全部 4 分，缺『需求与现状』关——merge 脚本从 pull_box 取需求字段只用 P/L1/L2 键名，与当日 daily 的 project/unavoidable/limitations/leverage 命名不匹配，customer_requirement/operational_pain_points/sales_summary 未落库。已用 daily 公开内容回填（非编造）+ 修复 merge 脚本键名兼容（commit dc7e005），重跑后 10/10 升至 5 分。

> 本版（17:20 证据强化版）仅改动 daily 原文证据结构（新增 instrument_evidence/software_necessity/icp_attempts 字段并修正时序），**不改变 enriched 评分**——enriched 已按早班 10 条合并入库，本版字段增强用于 Stage 3 手工 verification，后续 enrichment 将自动继承。

---

*Generated: 2026-09-22 17:30 CST（证据强化版）| Radar Type: Industrial | Experiment Week: 5+ | 本版目的：解决手工 verification 时『iMS 可售性/软件必要性证据缺失』问题*
