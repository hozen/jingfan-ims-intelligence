# iMS GTM Public Signal Radar — Prompt 版本谱系

市政市场机会雷达（Municipal Radar）prompt 历史版本归档。

> 范围说明：本目录只归档**市政雷达**（iMS GTM Public Signal Radar / Hach iMS 公共市场机会雷达）的 prompt。工业雷达（Industrial Opportunity Radar，job_1594ac48 对应）在 `intelligence/industrial/` 相关的 spec 文件维护，不在本目录。

| 文件 | 版本 | 日期 | 来源/说明 |
| --- | --- | --- | --- |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.0.md` | v3.0（中文完整版） | 2026-08-10 前后 | 初版「Public Market Opportunity Radar」，六大扫描雷达 + 6-18 个月机会窗口。原文件 `ims-public-radar/prompts/radar-v3.0-zh.md` |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.1.md` | v3.1（英文 Patch） | 2026-08-10 | Patch：Trigger 分类（Regulatory/Investment/Sentiment）+ Opportunity 分层（Verification→Qualification→Advocacy）+ Internal Match Priority。作用于 v3.0 之上 |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.2.md` | v3.2（市政专用版） | 2026-08-11 起生效 | Signal → Opportunity Hypothesis → Company Agent Handoff 三段管线。新增 `potential_ims_use_case` / `logic_chain_check` / `qc_checklist`。2026-09-12 追加最高优先级边界声明（仅处理市政线索）。原文件 `ims-public-radar/prompts/radar-v3.2.md` |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.2_full_20260913.md` | v3.2（全量版） | 2026-09-13 归档 | 2026-09-13 会话实际运行版本：工作日周一至周五 8:00 执行；含 PDF 交付要求、GITHUB 接口（latest.json/daily/enriched 回写）、六大扫描雷达（含工业项目雷达）、五类 to_verify 结构化。与市政专用版的差异：无"仅市政"边界声明、增加多站点归集与 enriched 交付 |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.3_incremental_20260831.md` | v3.3 增量升级 Prompt | 2026-08-31 | Stage 1 Discovery + Stage 2 Qualification 增量升级；对 v3.2 增量叠加，不整体替换。原文件为用户 8/31 上传文本 |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.3.md` | v3.3（完整版） | 2026-09-11 | 将增量升级 + v3.2 合并为完整主 prompt（235 行）：Stage Gate 阶段准入、Action Triad 行动三要素、Project-Customer Stage 第一权重（招标阶段总分封顶 55）、项目线索与市场情报分列表 |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.4.md` | v3.4（完整版） | 2026-09-11/12 | 三段管线（three-stage pipeline）完整版。当前 GitHub 远程已包含 |
| `iMS_GTM_Public_Signal_Radar_prompt_v3.5.md` | v3.5（完整版） | 2026-09-12 | 基于 9/02—9/11 历史线索复盘的五项新增：①逻辑链质量门（BROKEN 禁入机会、WEAK 封顶 60）；②阶段-窗口绑定校验（档位统一 >9/6-9/3-6/<3）；③行业边界过滤（工业 Fab 归工业雷达）；④连续性强制执行（无新事实不重发）；⑤Schema 统一（version/trigger_type/top5 对齐） |

## 版本演进要点

- **v3.0 → v3.1**：从"扫描 6 类雷达触发"转向"Trigger 分类 + Opportunity 分层验证"，明确 Internal Match（产品线匹配度）为排序第一优先级。
- **v3.1 → v3.2**：引入 Opportunity Hypothesis 结构（四问），要求每条候选机会输出 `potential_ims_use_case` 与 `logic_chain_check`，末尾附 `qc_checklist` 自检；输出从"信号列表"进化为"可交接的假设"。
- **v3.2 → v3.3**：针对 9 月初复盘发现"线索退化为招标公告""缺行动三要素"等问题的四条固化：①Stage Gate 阶段准入；②Action Triad（find_who/talk_what/why_now）；③评分封顶 55；④分列表输出。
- **v3.3 → v3.4**：Stage 1 Discovery + Stage 2 Qualification 三段管线继续演进，为 Company Agent 交接提供更细的阶段化信息。
- **v3.4 → v3.5**：针对 9/02—9/11 历史线索复盘的五个遗留缺陷固化：招标/采购项目仍混入机会（63%）→ 行业边界与逻辑链质量门；tw 档位口径混乱 → 阶段-窗口绑定校验；华虹等工业 Fab 混入市政 → 行业边界过滤；无新事实仍重复重发 → 连续性强制执行；schema 缺 version/trigger_type → 统一 Schema。同时按新规对历史 daily 线索做了"补充为主、合并与修正为辅"的修订（见 daily/ 各文件 v35_revision 记录）。
- **v3.2 全量版（2026-09-13 归档）**：与 v3.2 市政专用版并行的一条主线——用于市政+工业全量线索归集、实体关联与销售洞察补全场景，产出 master consolidated JSON 并回写 `intelligence/municipal/enriched/` 与 `intelligence/industrial/enriched/`。当日同步归档至 `iMS_GTM_Public_Signal_Radar_prompt_v3.2_full_20260913.md`。

## 未找到的版本

- **v1 / v2**：工作区、会话目录、记忆文件及 Git 历史中均未找到 v1/v2 独立原文。现有最早完整原文为 v3.0-zh；复盘记录显示 8/10 之前已有更早版本，但其原文未留存。如后续在历史会话/上传记录中找到，可补充进本目录。