---
name: financial-claim-verification
description: Verify specific quantitative claims from Chinese financial bloggers ("搬砖部", "循因缉药" etc.) against primary sources. Prevents accepting unverified data points.
triggers:
  - "验证"
  - "claim.*source"
  - "earnings call"
  - "management said"
  - "博主说"
---

# Financial Claim Verification Checklist

当微信公众号文章引用"管理层说"、"财报会"、"earnings call"等来源的具体数字时，按以下层级验证。

## 验证层级（按可信度排序）

### Level 1 — SEC EDGAR（最高可信）
- **10-K**：年度，Segment revenue、cash flow、RPO
- **10-Q**：季度，MD&A section有详细业务描述
- **8-K**：重大事件

**关键发现**：SEC文件里Danaher **不披露** equipment bookings/backlog/order intake，只披露RPO（Remaining Performance Obligations）。任何"设备订单增长X%"在10-K/10-Q里找不到是正常的——这不是漏洞，是公司选择不披露。

Danaher Q1 2026 10-Q原文（ Biotechnology段）：
> "high-single digit increases in core sales in the bioprocessing business and was **primarily driven by improved consumables demand** from large pharmaceutical customers, **partially offset by lower equipment sales**"

Life Sciences段：
> "increase in consumables sales, **partially offset by decreased demand for equipment**"
> "In the life science instruments businesses, core sales **decreased** year-over-year as **lower equipment demand** more than offset increased demand for consumables"

**注意**：Danaher近期filing中segment名称已从"Bioprocessing"改为"Biotechnology"。FY2025 10-K中 "Biotechnology" = 历史"Bioprocessing"业务。

### Level 2 — Press Release / Earnings Call
- Press release：仅包含管理层确认的高层次数字，无订单数据
- Earnings call transcript：最可能有细节，但**SeekingAlpha经常captcha阻挡**
- 替代找法：Danaher investor website + search engine cached transcripts

### Level 3 — Western Analyst Reports
- Bloomberg、FactSet、SeekingAlpha Analyst Coverage
- 关键词搜索：`"Danaher equipment orders"`、`"Danaher backlog"`
- 比中国博主可靠，但仍有口径差异

### Level 4 — 中国博主（最低可信）
- 公众号文章准确率高的是：营收数字、segment growth percentage
- 公众号文章经常出问题的是：具体订单数字、管理层引述、未经披露的运营指标

## Danaher案例：设备订单30%增长

**Claim**：公众号"循因缉药"称"管理层在财报会上说设备订单增长超过30%"

**验证结果**：
- 10-Q（SEC filed）：只有"lower equipment sales"，无30%数字 ❌
- Press release：无订单数据 ❌
- 10-K RPO：FY2024→FY2025 = +21%（最接近但不是30%）❌
- Earnings call transcript：SeekingAlpha captcha阻挡，未能获取 ❌

**结论**：无法证伪，但无法证实。30%这个数字在公开SEC文件里不存在。

**警示**：公众号在营收/利润数字上准确（17.97亿、11.5%），但在运营细节上可能 paraphrasing 或二次传播误差。

---

## 关键验证框架

**假说验证流程**：
1. 提取公众号原文中的具体数字claim
2. 列出该claim属于哪类数据（revenue？order？backlog？margin？）
3. 确认该数据类型是否在SEC文件中有披露
4. 10-K/10-Q里找不到 ≠ 博主说谎，但需要alternative source确认
5. 如果博主说"管理层在财报会说"，但SEC文件无记录 → 红旗

## Danaher案例：设备订单30%增长

**Claim**：公众号"循因缉药"称"管理层在财报会上说设备订单增长超过30%"

**验证结果**：
- 10-Q（SEC filed）：只有"lower equipment sales"，无30%数字 ❌
- Press release：无订单数据 ❌
- 10-K RPO：FY2024→FY2025 = +21%（最接近但不是30%）❌
- Earnings call transcript：SeekingAlpha captcha阻挡，未能获取 ❌

**结论**：无法证伪，但无法证实。30%这个数字在公开SEC文件里不存在。

**警示**：公众号在营收/利润数字上准确（17.97亿、11.5%），但在运营细节上可能 paraphrasing 或编造。

## 典型"红旗"清单

| 红旗信号 | 解释 |
|---------|------|
| 博主说"管理层说"但SEC文件无记录 | 可能是 paraphrasing 或二次传播误差；也可能是earnings call里有但10-K/10-Q不披露 |
| 具体数字（非区间）+ 冷门指标 | 如"backlog增长X%"，Danaher不披露backlog，只披露RPO |
| 数字以"约"、"超过"、"高个位数"模糊表述 | 故意模糊以避免被证伪 |
| 与已知数据矛盾 | 如"RPO +21%"但博主写"订单+30%" |
| 公众号转述management comment但找不到原始quote | 管理层可能只在Q&A环节随口提了一句，非正式指引 |

## 常见数字差异来源

| 博主引用 | 实际SEC数据 | 差异原因 |
|----------|-------------|---------|
| 设备订单增长30% | RPO增长21% | 博主可能混淆了RPO与bookings，或传播误差 |
| 设备收入增长X% | 实际设备收入下滑 | "订单增长"和"收入确认"是不同概念，不能混用 |
| "管理层说"某数字 | SEC文件无记录 | 可能来自earnings call Q&A环节（非正式发言） |

## 工具

**SEC文件检索**：
- SEC EDGAR：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=DHR&type=10-K
- SEC EFTS API（程序化检索）：`https://efts.sec.gov/LATEST/search-index?q=DHR&dateRange=custom&startdt=2026-01-01&enddt=2026-04-30&forms=10-Q`
- Danaher Investor：https://investors.danaher.com

**Earnings Call Transcript**：
- SeekingAlpha（captcha经常阻挡）
- earningscast.com（替代来源）
- Danaher investor website有call录音，但通常不直接暴露文本

**微信公众号文章溯源**：
1. 文章URL格式：`https://mp.weixin.qq.com/s/SHORTCODE`
2. 下载HTML：`urllib.request` + headers（User-Agent: Mozilla/5.0）
3. 文章内容在 `id="js_content"` div中（通常2-3MB HTML文件）
4. 提取：用正则 `r'id="js_content"[^>]*>(.*?)(?=<div[^>]*id="js_preview"|$)'`
5. 剥除HTML标签后搜索目标内容

**市场数据（补充上下文）**：
- Finviz：`https://finviz.com/quote.ashx?t=DHR` — 获取P/E、52周高低、YTD涨跌、市值
- 支持多个ticker批量抓取（finviz不反爬）
- 字段：P/E(ttm)、Forward P/E、Market Cap、52W High/Low、Perf Week/Month/YTD/Year/3Y

## 工作流

```
收到博主claim（如"设备订单增长30%"）
    ↓
判断数据类型：revenue / order / margin / guidance
    ↓
查SEC Level 1文件（10-K/10-Q MD&A）
    ↓
找不到？→ 查press release / earnings call（Level 2）
    ↓
还找不到？→ 查Western分析师（Level 3）
    ↓
仍然找不到 → 标注"无法证实"，不作为决策依据
```
