# iMS 市政机会雷达（Public Signal Radar）Agent 复现包 — README

> 用途：在另一套 Agent 环境（OpenCL/OpenCode 或任何支持 agent 的运行时）中**复现当前 DuMate 市政雷达任务的完整行为与产出**。
> 打包时间：2026-09-29（提取自调度任务 [DuMate task ID redacted]）
> 资格：本包为"市政线"独立复现包；工业线另见同目录 `industrial_radar_agent_repro.zip`。

## 1. 这个包是什么

当前生产环境中的"iMS 市场机会雷达"（市政线）是一个定时调度 Agent 任务：
- 周一/三/五 08:00 自动运行（模型 glm-5）
- 用公开互联网搜索扫描六大雷达信号源，经**三阶段流水线**（Stage 1 发现 → Stage 2 资格审定 → Stage 3 公开信息富化）产出结构化机会线索
- 将线索写入 GitHub 仓库 `hozen/jingfan-ims-intelligence`（daily JSON + Markdown 报告 + latest.json 累积快照 + enriched 合并），最终汇入靖帆系统线索 pipeline
- 关键产出要求：**仅 Markdown + JSON，不生成 PDF**

本包把「让这个 Agent 能跑起来」所需的一切材料做了快照，目标环境按 §3 部署即可开始复现。

## 2. 包内文件与用途

```
municipal_radar_agent_repro/
├── README.md                                ← 本文件
├── agent_prompt/
│   └── main_prompt_v3.4.2.md                ← 任务主 Prompt 完整原文（调度消息逐字转录，自包含，最高优先级）
├── specs/
│   ├── iMS_GTM_Public_Signal_Radar_prompt_v3.4.2.md  ← 本线现行版本（2026-09-24，与主 Prompt 同源）
│   ├── iMS_GTM_Public_Signal_Radar_prompt_v3.4.md    ← 历史版本（2026-09-09 评审，供演进参考）
│   ├── iMS_GTM_Public_Signal_Radar_prompt_v3.4_latest_20260917.md ← 历史版本（latest.json 语义确立版）
│   ├── iMS_GTM_Public_Signal_Radar_prompt_v3.3.md    ← 历史版本（Stage Gate/action_triad/分列表源头）
│   ├── README_版本谱系.md                           ← 版本演进说明（v3.3→v3.4→v3.4.1→v3.4.2，历史线 v3.5-v3.7 全量版说明）
│   └── Group_Software_Evidence_Check_v1.0.md  ← 集团软件证据核查规范（2026-09-27 强制，工业/市政共用）
├── scripts/
│   └── merge_radar_daily_to_enriched.py     ← Stage 4 合并脚本（幂等增量合并；--segment municipal；评分 Gate）
├── memory_context/
│   └── memory_context.md                    ← 长期记忆提炼（输出约束、版本演进、latest.json 语义、核查规范、环境备忘）
├── environment/
│   └── system_config_notes.md               ← 工具链/目录约定/GitHub SSH/调度参数/一次完整运行步骤
└── examples/
    ├── daily_2026-09-28.json                ← 最近一期每日结构化数据（真实产出样例）
    ├── latest.json                          ← 累积快照（真实产出样例）
    └── report_2026-09-28.md                 ← 最近一期 Markdown 报告（真实产出样例）
```

## 3. 部署步骤（目标环境）

1. **准备仓库**：`git clone git@github.com:hozen/jingfan-ims-intelligence.git`（含 scripts/）。
2. **放置主 Prompt**：将 `agent_prompt/main_prompt_v3.4.2.md` 全文作为调度任务的触发消息（相当于原任务 job_14c6b43e 的 message）。主 Prompt 自包含全部规则，不依赖本包内其他文件即可运行；specs/ 与记忆上下文用于对齐口径与背景。
3. **设置调度**：cron `0 8 * * 1,3,5`（Asia/Shanghai），模型选与 glm-5 性能相近者，超时 ≥1800s。
4. **配置 GitHub 推送**：目标环境放置有效 SSH 密钥并更新主 Prompt 中的密钥路径（包内不含密钥）；推送见 environment/system_config_notes.md §3。
5. **首次运行**：建议先手动触发一次，核对：daily JSON / reports MD / latest.json 三件套生成无误、`--segment municipal` 合并脚本可运行、评分 ≥4 分、推送触发 Actions 重建成功。
6. **校准对照**：用 `examples/` 中 2026-09-28 的真实产出对照自有输出格式与质量。

## 4. 交付要求速览（目标 Agent 必须满足）

- 会话内输出**完整中文 Markdown 报告**（Section 0 三阶段总览 → Section 1-10 + 分列表 + 补词提示 + QC Checklist）
- 生成 `intelligence/municipal/daily/YYYY-MM-DD.json`（结构化 + 保 Schema 兼容 + v3.4.2 新增字段）
- 同步更新 `intelligence/municipal/latest.json`（累积快照：全部有效线索 + first_seen/continuity + 处置标注）
- `intelligence/municipal/reports/YYYY-MM-DD.md`
- 推送前运行 Stage 4：`python3 scripts/merge_radar_daily_to_enriched.py --segment municipal` + 评分质量 Gate（新增线索 ≥4 分，尽量 5 分；宁可真缺不假补）
- 一次性 push（daily + reports + latest.json + indctx_latest.json + leads-data.json/index.html）→ 触发 Actions 重建
- **不生成、不推送任何 PDF**
- 会话交付 MD 报告文件（file_export 声明，不覆盖已交付文件）

## 5. 版本与口径的已知说明（重要）

1. **版本号**：本任务现行主 Prompt 为 **v3.4.2**（2026-09-24 用户评审确认，调度消息已更新）；任务名称与部分归档仍写"v3.4.1"（历史调度消息版本），记忆条目 2026-09-17 对应 v3.4.1。以 `main_prompt_v3.4.2.md` 为准：v3.4.2 = v3.4 + v3.4.1（Stage 4 合并+评分 Gate，2026-09-21 固化）+ 2026-09-24 增补（采购意向/需求公示入层、信号源扩展、win_result/topic_tag、关键词反哺）。
2. **采购意向档与 55 分封顶**：采购意向/需求公示档**不适用**招标封顶 55 分，阶段分按"高于方案、低于设计"中高档标定；只有正式招标/资格预审/采购（含挂网编号/截止时间）才触发 55 分封顶并转 background_monitoring[]。
3. **latest.json 语义**：v3.4 消息原文与 v3.4.2 均要求"同步覆盖更新"；2026-09-17 用户指示进一步明确为"累积快照、含全部收集数据、跨日保留 continuity"——执行时以后者语义为准（已写入主 Prompt）。
4. **三阶段覆盖**：每次执行必须完成 Stage 1/2/3；任一 Stage 缺失视为任务未完成，不得发布。
5. **集团软件证据核查**：2026-09-27 起每条机会/背景监控必须含 group_software_evidence 且 ims_link_strength 非空，缺失视为任务未完成（规范见 specs/）。
6. **主 Prompt 为唯一事实源**：本包内 specs/ 为归档与口径参考；若与主 Prompt 措辞冲突，以主 Prompt 为准。

## 6. 已知风险与改进建议

- 目标是「复现产出」，不是「复现检索足迹」：不同搜索引擎/检索配额下的信号覆盖会有差异，建议用 §3 步骤 6 的校准对照持续调参（检索词表人工回填依赖 qc_checklist.keyword_drift_checked）。
- SSH 密钥与 GitHub 访问权限需目标环境自备；密钥路径在任务消息中写明，首次运行前务必核对。
- 若目标环境无 WeasyPrint/无字体、或模型上下文更短，均不影响本任务（本任务纯文本 + JSON 输出）。