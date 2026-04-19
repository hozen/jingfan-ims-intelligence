---
title: Wiki Schema
created: 2026-04-19
updated: 2026-04-19
type: meta
---

# Wiki Schema — 环博会市场观察知识库

## Domain
环保/水务行业市场研究 + AI技术在环境监测领域的应用。
聚焦：2026年第27届上海国际环博会（2026.04.13-15）。

## Conventions
- 文件名：小写、连字符、无空格（例：`hach-company.md`）
- 每个wiki页面以YAML frontmatter开头
- 使用 `[[wikilinks]]` 跨页面链接（每页至少2个出站链接）
- 更新页面时必须更新 `updated` 日期
- 新页面必须添加到 `index.md`
- 所有操作必须追加到 `log.md`

## Tag Taxonomy（标签分类）

### 实体（Entities）
- `company` — 公司（仪器厂商、服务商、云厂商）
- `product` — 产品/技术
- `event` — 展会/论坛/会议
- `award` — 奖项/榜单

### 概念（Concepts）
- `market` — 市场规模/趋势
- `software` — 软件/AI/数字化能力
- `hardware` — 硬件/仪器/传感器
- `policy` — 政策/法规/标准
- `strategy` — 竞争策略/商业分析
- `forum` — 论坛演讲内容

### 维度（Meta）
- `comparison` — 对比分析
- `raw` — 原始数据/未加工材料
- `summary` — 摘要/结论

## Entity Pages
每个公司一页，包含：
- 概述 / 定位
- 关键事实和数据
- 与其他实体的关系（[[wikilinks]]）
- 来源引用

## Concept Pages
每个主题一页，包含：
- 定义 / 解释
- 当前认知状态
- 开放问题或争议
- 相关概念（[[wikilinks]]）

## Comparison Pages
包含：
- 对比对象和对比原因
- 对比维度（表格格式优先）
- 结论或综合判断
- 来源

## Update Policy（更新策略）
新信息与现有内容冲突时：
1. 检查日期——新来源通常覆盖旧来源
2. 真正矛盾时，注明双方立场和来源
3. 在frontmatter标记：`contradictions: [page-name]`
4. 在lint报告中提交用户审核

## Page Thresholds
- **创建页面**：实体/概念在2+来源中出现，或在单一核心来源中处于中心位置
- **追加现有页面**：来源提到已覆盖内容
- **不创建页面**：仅在脚注中提及的次要细节
- **拆分页面**：超过200行时拆分为子主题
