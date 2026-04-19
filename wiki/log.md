# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-04-19] ingest | Initial data population
- Ingested: 9 company entities, 1 event entity, 1 policy entity, 2 concepts, 2 comparisons, 2 raw sources
- Companies: Hach, Juguang/PUYU, Xylem, Zhiyi, Veolia, Shouchuang, Hongtai, Xintong, Endress+Hauser
- Events: IE expo 2026
- Policy: MEE AI Action Plan
- Concepts: AI in environmental monitoring, (software strategy TBD)
- Comparisons: hardware competitors, software competitors
- Raw: E3 exhibitor list (WeChat OCR), AI forum transcript (Yuanbao)

## [2026-04-19] create | Wiki initialized
- Domain: 环保/水务行业市场研究 + AI在环境监测的应用
- Event: 第27届上海国际环博会 2026.04.13-15
- Structure created: SCHEMA.md, index.md, log.md
- Directory structure: wiki/raw/{articles,transcripts,assets}, wiki/entities/companies/, wiki/concepts/, wiki/comparisons/, wiki/queries/

## [2026-04-19] ingest | Complete session documentation
- Created: projects/ie-expo-2026-market-watch/PROJECT.md (项目总览)
- Created: projects/ie-expo-2026-market-watch/SESSION-2026-04-19.md (完整工作记录)
- PPT: 4代脚本迭代 (v16→v17→v18→v19)，Slide B两次重建解决重叠
- PPT最终版: 环博会市场观察_20260419.pptx，16页，441KB，封面加AI声明
- Wiki: 9个公司实体 + 1事件 + 1政策 + 2概念 + 2对比 + 2原始资料，全部归档
- Git: 5次commit，未push（GitHub超时，Bitbucket/GitCode/GitLab.cn可访问）
- PPT生成脚本全部入git: gen_v16.js, gen_v17.js, gen_v19.js
