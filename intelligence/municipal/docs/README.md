# iMS GTM Public Signal Radar — Prompt 版本谱系

市政市场机会雷达（Municipal Radar）prompt 历史版本归档。

> 范围说明：本目录只归档**市政雷达**（iMS GTM Public Signal Radar / Hach iMS 公共市场机会雷达）的 prompt。工业雷达（Industrial Opportunity Radar，job_1594ac48 对应）在 `intelligence/industrial/` 相关的 spec 文件维护，不在本目录。

| 文件 | 版本 | 日期 | 来源/说明 |
| --- | --- | --- | --- |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.0.md` | v3.0（中文完整版） | 2026-08-10 前后 | 初版「Public Market Opportunity Radar」，六大扫描雷达 + 6-18 个月机会窗口。原文件 `ims-public-radar/prompts/radar-v3.0-zh.md` |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.1.md` | v3.1（英文 Patch） | 2026-08-10 | Patch：Trigger 分类（Regulatory/Investment/Sentiment）+ Opportunity 分层（Verification→Qualification→Advocacy）+ Internal Match Priority。作用于 v3.0 之上 |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.2.md` | v3.2（完整版） | 2026-08-11 起生效 | Signal → Opportunity Hypothesis → Company Agent Handoff 三段管线。新增 `potential_ims_use_case` / `logic_chain_check` / `qc_checklist`。原文件 `ims-public-radar/prompts/radar-v3.2.md` |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.3_incremental_20260831.md` | v3.3 增量升级 Prompt | 2026-08-31 | Stage 1 Discovery + Stage 2 Qualification 增量升级；对 v3.2 增量叠加，不整体替换。原文件为用户 8/31 上传文本 |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.3.md` | v3.3（完整版） | 2026-09-11 | 将增量升级 + v3.2 合并为完整主 prompt（235 行）：Stage Gate 阶段准入、Action Triad 行动三要素、Project-Customer Stage 第一权重（招标阶段总分封顶 55）、项目线索与市场情报分列表 |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.4.md` | v3.4（完整版） | 2026-09-11/12 | 三段管线（three-stage pipeline）完整版。当前 GitHub 远程已包含 |

## 版本演进要点

- **v3.0 → v3.1**：从"扫描 6 类雷达触发"转向"Trigger 分类 + Opportunity 分层验证"，明确 Internal Match（产品线匹配度）为排序第一优先级。
- **v3.1 → v3.2**：引入 Opportunity Hypothesis 结构（四问），要求每条候选机会输出 `potential_ims_use_case` 与 `logic_chain_check`，末尾附 `qc_checklist` 自检；输出从"信号列表"进化为"可交接的假设"。
- **v3.2 → v3.3**：针对 9 月初复盘发现"线索退化为招标公告""缺行动三要素"等问题的四条固化：①Stage Gate 阶段准入；②Action Triad（find_who/talk_what/why_now）；③评分封顶 55；④分列表输出。
- **v3.3 → v3.4**：Stage 1 Discovery + Stage 2 Qualification 三段管线继续演进，为 Company Agent 交接提供更细的阶段化信息。

## 未找到的版本

- **v1 / v2**：工作区、会话目录、记忆文件及 Git 历史中均未找到 v1/v2 独立原文。现有最早完整原文为 v3.0-zh；复盘记录显示 8/10 之前已有更早版本，但其原文未留存。如后续在历史会话/上传记录中找到，可补充进本目录。