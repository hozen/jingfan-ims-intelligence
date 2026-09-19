# 杨崇和动向追踪 - 结构化数据仓库

## 目录结构

```
yang_chonghe_tracker/
├── README.md                # 本说明文件
├── weekly/                  # 按周生成的数据文件
│   └── 2026-09-w38.json     # 示例：2026年9月第38周
├── monthly/                 # 按月度聚合（可选，未来迭代）
│   └── 2026-09.json         # 示例：2026年9月
└── latest.json              # 最新一期数据快照（可选，未来迭代）
```

## 命名规范

- **按周文件**：`YYYY-MM-wNN.json` → 例：`2026-09-w38.json`（体现年月+周，不含日）
- **按月文件**：`YYYY-MM.json` → 例：`2026-09.json`（体现年月）
- **时间字段**：JSON 内部 `meta` 区块记录完整时间范围（start_date/end_date/generated_at，格式 ISO 8601）

## JSON 顶层结构（schema_version=1.0）

```jsonc
{
  "schema_version": "1.0",
  "meta": {
    "subject": "杨崇和动向追踪",
    "report_type": "weekly",          // weekly | monthly
    "period_label": "2026-09-W38",
    "year": 2026,
    "month": 9,
    "week": 38,
    "start_date": "2026-09-14",       // 周起始（ISO周，周一）
    "end_date": "2026-09-19",         // 周结束（周六）
    "generated_at": "2026-09-19T11:14:23+08:00",
    "source": "公开信息搜索",
    "framework": "巴菲特价值投资 v1.0",
    "perspective": "以杨崇和为投资向导"
  },
  "core_events":        [本期最重要事件的字符串数组],
  "yang_chonghe_dynamics": {          // 第2节：杨崇和动态
    "earnings_call": {...},           // 业绩说明会/演讲
    "investor_relations": {...},      // 调研要点
    "announcements": [...],           // 公告列表
    "events": [...],                  // 其他事件
    "financials": {...}               // 财务数据
  },
  "zhivei_lingfeng_fund": {           // 第3节：智微凌峰与生态圈
    "fund_update": {...},
    "yin_zhiyao": {...},              // 尹志尧动向
    "portfolio": [...]                // 被投企业进展
  },
  "ecosystem": {                      // 澜起生态圈
    "hengqin_subsidiary": {...},      // 横琴子公司
    "yf_fund": {...},                 // 云锋基金
    "changxin": {...},                // 长鑫科技
    "customers": [...],               // 客户结构
    "korea_antitrust": {...},         // 韩国反垄断调查
    "acquisition_targets": {...}      // 潜在并购标的
  },
  "targets": [                        // 第4节：标的速评（巴菲特框架）
    {
      "ticker": "688008",
      "name": "澜起科技",
      "role": "core_holding",         // core_holding | watchlist
      "moat": {...},
      "buffett_scores": {
        "roe": {"value": 18.25, "unit": "%", "period": "2025FY", "threshold": 15, "passed": true},
        "roic": {"value": 15.47, "unit": "%", "period": "2025FY", "threshold": 15, "passed": true},
        "fcf": {"value": 1.85, "unit": "billion_cny", "period": "2025FY", "positive": true, "trend": "healthy"}
      },
      "valuation": {"pe_ttm": 80.42, "pb": 11.43},
      "management": {...},
      "combined_rating": "持有/回调加仓",
      "note": "..."
    }
  ],
  "action_advice": "一句话行动建议"
}
```

## 数值与单位约定

- 金额统一：元（CNY）、亿元（billion_cny）、万元（million_cny）；美股若涉及用美元（USD），不出现 `$` 符号
- 百分比统一：%
- 日期统一：ISO 8601（YYYY-MM-DD）
- 周期字段：FY 表示财年（如 2025FY），E 表示预测（如 2026E）
- 巴菲特三大并列指标缺失任一即视为不合格，FCF 必须给出具体数值与趋势判断

## 与 ABC 投资系统的衔接

本目录为已采集、处理、整理后的结构化数据源。ABC 投资系统可通过 GitHub 拉取
`weekly/*.json` 增量更新，或订阅 `latest.json` 获取最新快照。字段命名保持稳定，
schema 变更通过 `schema_version` 标识并进行向后兼容。