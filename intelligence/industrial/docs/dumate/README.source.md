# iMS 工业雷达线索 Agent 复现包

> 用途：在另一个 Agent 环境中复现「IMS Industrial Opportunity Radar」任务的完整能力与产出标准。
> 提取自：DuMate 当前配置（调度任务 [DuMate task ID redacted]「IMS Industrial Opportunity Radar」，2026-09-28 版本）+ 长期记忆 + 靖帆仓库（hozen/jingfan-ims-intelligence）实际产物。
> 提取日期：2026-09-29

---

## 一、这个包是什么

当前 Agent 的工业雷达能力 = **调度任务 Prompt**（每日执行的完整指令）+ **规范文件**（迭代修正的沉淀）+ **记忆上下文**（长期背景知识）+ **仓库/脚本生态**（数据落库与质量 Gate）+ **输出样例**（格式基准）。本包把以上五部分按原样打包，任何具备"联网搜索 + Python + Git"能力的 Agent 环境按 README 配置后即可产出同等质量的结果。

## 二、包含内容与文件映射

| 目录/文件 | 内容 | 原始来源 |
| --- | --- | --- |
| `agent_prompt/main_prompt_v4.1.md` | **任务主 Prompt 完整原文**（逐字复制自调度任务消息） | 调度任务 job_1594ac48（2026-09-28 快照） |
| `specs/Industrial_Radar_Spec_v1.0.md` | 初版规范（任务消息会按需读取） | 仓库 intelligence/industrial/docs/ |
| `specs/Industrial_Radar_Spec_v2.0.md` | v2.0 规范 | 同上 |
| `specs/Industrial_Radar_Spec_v3.0.md` | v3.0 Early Signal 修正规范 | 同上 |
| `specs/Industrial_Radar_Spec_v4.0.md` | v4.0 输出修正（2026-09-12 用户确认，优先级最高） | 同上 |
| `specs/PULL_Qualification_v1.md` | PULL Demand-First 升级规范（必须执行） | 同上 |
| `specs/VM_Qualification_Rules_v1.md` | VM 10 条经验规则 + 落地 Gate | 同上 |
| `specs/Group_Software_Evidence_Check_v1.0.md` | 集团软件证据核查 v1.0（2026-09-27 强制，工业/市政共用） | 仓库 intelligence/docs/ |
| `scripts/merge_radar_daily_to_enriched.py` | Stage 4 合并脚本（幂等增量合并 + 评分分布输出） | 仓库 scripts/ |
| `scripts/build_industrial_pipeline_view.py` | 靖帆系统公开页构建脚本（被合并脚本调用） | 仓库 scripts/ |
| `memory_context/memory_context.md` | 提炼自 MEMORY.md 的与工业雷达相关的全部记忆条目（原文） | DuMate 长期记忆 MEMORY.md |
| `environment/system_config_notes.md` | 工具依赖、GitHub/SSH、调度、目录约定、运行速查 | DuMate 运行环境 + 任务消息 |
| `examples/daily_2026-09-26.json` | 最近一次运行的 daily JSON 输出（格式基准） | 仓库 intelligence/industrial/daily/ |
| `examples/daily_2026-09-12_fixed.json` | 任务消息指定的三字段修复参考样例 | 同上 |
| `examples/latest.json` | latest.json 聚合快照参考（2026-09-24，见「已知不一致」） | 仓库 intelligence/industrial/latest.json |
| `examples/IND_Radar_Daily_20260922.md` | 历史 MD 日报样例（版式/结构基准） | 仓库 intelligence/industrial/reports/ |

## 三、部署到新 Agent 环境的步骤

1. **创建任务工作目录**：在目标 Agent 的工作目录下建立 `ims_industrial_radar/`，把 `specs/` 下 7 个规范文件复制进去（任务消息按 `{工作目录}/ims_industrial_radar/` 读取）。
2. **安装主 Prompt**：把 `agent_prompt/main_prompt_v4.1.md` 全文作为任务的触发消息 / 系统指令。
3. **配置调度**：cron `0 8 * * 2,4,6`（周二/四/六 08:00，Asia/Shanghai），模型建议用与 glm-5 同档的模型，超时 ≥1800s。
4. **加载记忆上下文**：把 `memory_context/memory_context.md` 内容注入目标 Agent 的长期记忆/系统背景（若目标平台支持记忆文件机制，则放入其记忆存储；否则放在系统指令尾部）。
5. **准备仓库与密钥**：确保可访问 `git@github.com:hozen/jingfan-ims-intelligence.git`（目标环境放置 SSH 密钥后，按 system_config_notes.md §3 更新任务消息中的密钥路径，或改用平台自身的凭据机制）。
6. **放置脚本**：`scripts/` 两个脚本在仓库 clone 后可自动获得（推荐以仓库为准）；如目标环境无法 clone 仓库，可手动放入仓库对应路径。
7. **首轮试运行校验**：跑一次完整任务，对照 `examples/` 检查：
   - JSON 关键字段齐全（radar_type/market_segment/scanner_summary/top_5_match/signals[]/market_background/source_effectiveness/experiment_observations）；
   - 每条信号含 influence_window、entry_timing、stage3_handoff 三字段及其 evidence；
   - MD 具备首页 GTM 决策页 + Qualification Card + 汇总统计 + Demand Learning Summary；
   - Stage 4 评分分布：新增线索全部 ≥4 分；
   - 无 PDF 产物。

## 四、已知不一致与校准说明（重要）

复现时以下两点无法从单一来源自洽确定，已按证据链如实记录，**建议在目标环境首次运行前与用户确认口径**：

1. **工业 latest.json 的去留**：
   - 任务消息（v4.0 修正 2 + v4.1 推送步骤 5）明确写：只生成并推送当日 daily JSON，「不再生成 latest.json，不覆盖 intelligence/industrial/latest.json」。
   - 但：① 用户 2026-09-17/09-21 的记忆指示记录有「latest.json 聚合规则（全量聚合、按归一化公司名去重、标 current_status）并推送 intelligence/industrial/latest.json」；② 仓库实际存在 intelligence/industrial/latest.json（2026-09-24 快照，report_date=2026-09-24，含 scanner_summary + 全量 signals 去重聚合）；③ 集团软件证据核查规范（2026-09-27）写明工业信号"同步 latest.json 聚合"。
   - 结论：**实际生产行为以「维护并推送 latest.json（全量聚合）」为准的可能性更高**，但 09-26 运行未更新 latest.json（仍停留 09-24）。本包以任务消息正文为基准（不改原文），并在 memory_context.md §7 保留聚合规则供启用；请用户二选一后固化到目标环境消息中。
2. **Spec 版本引用**：任务消息引用 `Industrial_Radar_Spec_v4.0.md` 为最新（2026-09-12）；仓库 docs 内 v2.0 为中间版本（记忆条目曾写 v2.0 路径）。本包 4 个版本规范全部收录、保持原文，任务消息按存在性读取，不影响复现。

## 五、交付物与质量要求（复现目标）

每次运行必须产出：
1. **MD 日报**（会话输出 + 落盘 `ims_industrial_radar/IND_Radar_Daily_YYYYMMDD.md`，file_export 声明）；
2. **daily JSON**（`ims_industrial_radar/daily_YYYY-MM-DD.json` → 推送 `intelligence/industrial/daily/`）；
3. **enriched 合并**（`python3 scripts/merge_radar_daily_to_enriched.py --segment industrial`）→ `intelligence/industrial/enriched/indctx_latest_jd_<date>.json` + `indctx_latest.json` + 重建 `customer/industrial-leads/leads-data.json`/`index.html`；
4. **无 PDF**；
5. MD 末尾附 Stage 4 合并结果行（新增 N 条、4/5 分分布、缺失项）。

质量红线（与当前 Agent 一致）：禁止编造联系人/URL/招聘证据；宁缺毋滥；UNKNOWN 如实标注；证明不足时明确降级；任何「大项目但业务无关/非具体项目」的线索不得自动 PASS。

## 六、追溯说明

- 所有文件保留原始命名与内容，未做改写；仅本 README 与 memory_context、environment 说明为新增整理件。
- 主 Prompt 原样取自调度任务（提取日期 2026-09-29）；若用户后续在目标平台修改了任务消息，以修改后为准并同步更新本包。