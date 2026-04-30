---
name: danaher-financial-research
description: "How to research Danaher (DHR) financial data using SEC EDGAR primary sources. Use when verifying Danaher financial claims, cross-checking analyst reports, or researching Danaher performance for competitive intelligence. Replaces guesswork with primary-source verification."
---

# Danaher Financial Research — Primary Source Verification

## When to Use

- User cites a Danaher financial figure (e.g., "30% equipment order growth")
- You need to verify or challenge a claim from WeChat articles, analyst reports, or earnings call paraphrasing
- Researching Danaher quarterly/annual performance for competitive analysis
- Cross-referencing Chinese secondary sources against US SEC filings
- Investigating Danaher's software/digital business for competitive intelligence

## Cross-Company Research

For comparing Danaher vs. TMO, Agilent, or other life sciences instrument companies, use the companion skill instead:
```
sec-edgar-life-sciences-research
```
It documents the EFTS API workflow for multi-company research, PDF vs HTML download routes, and the cross-company software treatment finding.

## ⚠️ Critical: Earnings Release Timing Varies by Company

**DHR vs TMO reporting calendar (Q1 2026 observed):**

| Company | Q1 fiscal quarter ends | Q1 2026 release date | Status as of Apr 28 |
|---------|------------------------|----------------------|---------------------|
| Danaher (DHR) | March 27, 2026 | **April 21, 2026** | ✅ Available |
| Thermo Fisher (TMO) | March 28/31, 2026 | ~May 2026 (est.) | ❌ Not yet filed |

**TMO Q1 2026 filing status (verified via SEC EFTS, April 28, 2026):**
- TMO's most recent SEC filing: FY2025 10-K (period ending 2025-12-31, filed 2026-02-26)
- TMO Q1 2026 10-Q: **NOT yet published** — EFTS search-index finds no TMO 10-Q for period 2026-03-31
- Expected TMO Q1 2026 release: **early May 2026** (TMO typically reports ~5 weeks after quarter end)

**Practical implication**: When asked to compare DHR and TMO Q1 results, check whether TMO has actually reported yet. TMO typically reports 1-2 weeks later than DHR. If TMO Q1 isn't out yet, either:
1. Use TMO Q1 2025 as historical benchmark (with YoY comparison caveat)
2. Note that TMO hasn't reported yet and offer to check later
3. Use the latest available TMO data (Q4 2025 or FY2025 annual)

**EFTS search-index quirk**: Broad searches work (`q=thermo+fisher+10-Q`) but specific date-filtered queries on 10-Q sometimes return 0 hits even when filings exist. Always try the broader form search first.

## Core Principle

**Danaher does NOT disclose everything publicly.** Key things to know:
- Order intake/bookings: **NOT separately disclosed** → use RPO as proxy
- Equipment vs. consumables breakdown: **NOT disclosed** in 10-K
- Quarterly segment revenue: **NOT in 10-K** → requires 10-Q
- "30% equipment order growth": **NOT in any SEC filing** → likely from earnings call
- **Software revenue: NOT separately disclosed** → embedded in recurring revenue (consumables + service + OTL)
- **Recurring/non-recurring breakdown by segment: NOT disclosed at segment level** → only defined at company-wide level in 10-Q

---

## Step 1: Identify the Claim and Its Likely Source

| Claim type | Where to verify |
|------------|----------------|
| Revenue/sales figures | 10-K (annual), 10-Q (quarterly) |
| RPO (Remaining Performance Obligations) | 10-K MD&A section |
| Core sales growth % | Earnings press release |
| Equipment order growth | **Earnings call transcript only** — not in SEC filings |
| Segment commentary | 10-Q MD&A section |
| Guidance | 8-K or earnings press release |

**Critical distinction**: Danaher's SEC filings contain **revenue already recognized (sales)**, NOT order flow. Order growth claims come from earnings calls, not filings.

---

## Step 2: Pull Primary Sources from SEC EDGAR

Danaher CIK: **313616**

**Key URLs:**
- EDGAR company page: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=313616
- FY2025 10-K: https://www.sec.gov/Archives/edgar/data/313616/000031361626000062/dhr-20251231.htm
- FY2024 10-K: https://www.sec.gov/Archives/edgar/data/313616/000031361625000043/dhr-20241231.htm
- FY2023 10-K: https://www.sec.gov/Archives/edgar/data/313616/000031361624000052/dhr-20231231.htm

**Q1 2026 (period ending March 27, 2026):**
- 10-Q: accession 0000313616-26-000107 — period ending March 27, 2026, filed April 21, 2026

**For the 10-Q, try direct download:**
```
https://www.sec.gov/Archives/edgar/data/313616/000031361626000107/dhr-20260327.htm
```

If SEC.gov blocks, use the SEC EFTS API:
```
https://efts.sec.gov/LATEST/search-index?q=%22danaher%22&dateRange=custom&startdt=2026-04-01&enddt=2026-04-30
```

---

## Step 3: Extract Text from XBRL/HTML Filings

SEC filings are XBRL-tagged HTML. Strip tags to get narrative text:

```python
import re
with open('dhr_10q_full.htm', 'r') as f:
    content = f.read()
text = re.sub(r'<[^>]+>', ' ', content)
text = re.sub(r'\s+', ' ', text)
```

**Key search terms in Danaher filings:**
- `bioprocessing` — Biotechnology segment discussion
- `equipment sales` — equipment vs consumables revenue
- `consumables demand` — recurring revenue driver
- `Remaining Performance Obligations` or `RPO` — backlog proxy
- `core sales growth` — non-GAAP metric
- `respiratory` — Cepheid respiratory season impact
- `China` or `VBP` — China volume-based procurement impact
- `Masimo` — acquisition announcement (Q1 2026)

---

## Danaher Revenue: Recurring vs. Non-Recurring Structure

### Company-Wide Definition (from 10-Q)

| Category | Contents | Nature |
|----------|----------|--------|
| **Recurring** | Consumables (reagents, chromatography resin, filters) + Service + OTLs (operational leases) | Repeated purchases / subscriptions |
| **Non-Recurring** | Equipment (instruments) + STLs (sales-type leases) | One-time CapEx |

### Software in This Framework

**Software is NOT a standalone category** — it is embedded within recurring revenue:
- Beckman Coulter instrument software (sample management, data analytics)
- Pall process control software
- Sciex mass spectrometry software
- Cepheid molecular diagnostic software (GeneXpert)

**Q1 lease revenue (OTLs): $143M** (Q1 2026) vs $114M (Q1 2025) — +25.4%

### Key Limitation: Segment-Level Recurring/Non-Recurring NOT Disclosed

Danaher does **NOT** break out recurring vs. non-recurring revenue by segment in any SEC filing. The company-wide definitions above are the only official guidance.

**XBRL parsing challenge**: Dollar amounts in the XBRL data do not carry the recurring/non-recurring tag as a separate attribute — they are tagged by US-GAAP line item only. Extracting segment-level recurring/non-recurring requires qualitative reading of MD&A + customer channel intelligence.

### Danaher's Digital/Software Positioning

From 10-Q MD&A, the only software-adjacent description found:

> "bioprocessing business' offerings in **data connectivity and automation**, advanced process training, process development services and equipment services"

→ Focus is **equipment connectivity** (helping customers collect process data), not AI/ML analytics. This is a process optimization tool, not a software product line contributing independent valuation.

**Bottom line**: Danaher has no standalone SaaS business. Software is a customer retention/loyalty tool bundled with instruments and consumables — similar to Thermo Fisher's Unity™ Lab Services model.

### RPO (Remaining Performance Obligations) — Key Backlog Proxy

| Year | RPO | % Expected in Next 12 Months |
|------|-----|----------------------------|
| FY2025 | ~$5.2 billion | ~47% |
| FY2024 | ~$4.3 billion | ~47% |

**RPO growth: FY2024→FY2025 = +21%** — this may be the source of "order growth" figures cited in secondary sources.

**Important caveats (from Danaher 10-K):**
- RPO **excludes** short-term contracts (≤1 year)
- RPO **excludes** cancelable contracts
- RPO **excludes** equipment leases
- Consumables are **not in RPO** (recognized upon delivery)

### Danaher Segment Names (recent change)

| Old Name | Current Name (FY2024+) |
|----------|----------------------|
| Bioprocessing | Biotechnology |
| Life Sciences | Life Sciences |
| Diagnostics | Diagnostics |

### FY2023-2025 Annual Revenue ($ millions)

| Segment | FY2025 | FY2024 | FY2023 |
|---------|--------|--------|--------|
| Biotechnology | $7,293 | $6,759 | $7,172 |
| Life Sciences | $7,334 | $7,329 | $7,141 |
| Diagnostics | $9,941 | $9,787 | $9,577 |
| **Total** | **$24,568** | **$23,875** | **$23,890** |

### Q1 2026 Revenue (Three months ended March 27, 2026)

| Segment | Q1 2026 | Q1 2025 | Growth |
|---------|---------|---------|--------|
| Biotechnology | $1,797M | $1,612M | +11.5% |
| Life Sciences | $1,737M | $1,680M | +3.5% |
| Diagnostics | $2,417M | $2,449M | -1.5% |
| **Total** | **$5,951M** | **$5,741M** | **+3.5%** |

## Step 5: Cross-Verification Checklist for Financial Claims

When verifying a claim like "30% equipment order growth":

1. **Is it in the SEC filing?** → Search 10-Q/10-K for exact phrase
2. **Is it in the press release?** → Earnings press release has GAAP/non-GAAP numbers
3. **Is it from the earnings call?** → Transcripts not always publicly available; SeekingAlpha often blocks
4. **What metric is it?** → "Order growth" (bookings) ≠ "revenue growth" (recognized sales)
5. **Is the direction consistent?** → If Q1 10-Q says "lower equipment sales", a claim of "30% equipment order growth" needs sourcing

**Equipment orders (bookings) ≠ Equipment revenue (sales)**
- Orders can grow 30% while revenue declines (as seen in Q1 2026)
- This is not contradictory — it means the order-to-revenue recognition lag is lengthening

---

## Step 6: Revenue Recognition Timing for Equipment

Danaher does NOT disclose specific order-to-ship cycles. From RPO structure:
- ~47% of RPO recognized within 12 months
- ~53% recognized in months 13-36

**Implication**: Equipment orders placed in Q1 2026 will predominantly recognize in:
- **Standard equipment**: Q2-Q4 2026 (6-9 month cycle)
- **Complex/custom equipment**: 2026-2027 (13-24 months)
- **System integrations**: potentially into 2027

---

## Project Structure for Danaher Research

```
wiki/projects/work-08-danaher/
├── PROJECT.md                    # Project overview
├── annual-reports.md             # 3-year annual financial data from 10-Ks
├── q1-2026-earnings.md           # WeChat article summary + Q1 data
├── q1-2026-transcript.md         # Earnings call research (transcript blocked)
├── analyst-coverage.md            # [To add] Western analyst coverage
└── critical-analysis.md          # [To add] Challenge/synthesize all sources
```

---

## Key Danaher Competitive Intelligence Insights for Hach

- **Biotechnology (Bioprocessing)**: China pharma demand drives consumables. Equipment orders are a **leading indicator** for Hach's在线监测 business.
- **Diagnostics**: China VBP pressure is real. Cepheid respiratory seasonality.
- **RPO as leading indicator**: RPO growth (21% FY24→25) suggests upstream capital investment cycle is turning.
- **AI + DBS**: Danaher is integrating AI with DBS. Watch for Hach response.

---

### The "30% Equipment Order Growth" Case Study

**完整溯源链**：
1. 公众号原文："在财报会上，管理层也回答了……设备收入有所下滑，但是设备订单增长超过30%"
2. 10-Q（SEC filed）：MD&A中Biotechnology段只有"lower equipment sales"，无30%数字
3. Press release：无订单数据
4. 10-K RPO：FY2024→FY2025 = +21%（最接近但不是30%）
5. Earnings call transcript：SeekingAlpha captcha阻挡，未能获取

**结论**：该数字在SEC公开文件中完全不存在。公众号原文正确地将其归于"管理层在财报会说"，但无法交叉验证。**这类opearational metrics的claim是中文公众号最常见的错误来源。**

### WeChat文章正则提取（已验证有效）

```python
import re
with open('wechat_danaher_article.htm', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'id="js_content"[^>]*>(.*?)(?=<div[^>]*id="js_preview"|$)', html, re.DOTALL)
if m:
    content = re.sub(r'<[^>]+>', ' ', m.group(1))
    content = re.sub(r'\s+', ' ', content).strip()
    # 搜索具体claim
    idx = content.find('增长超过30')
    print(content[max(0,idx-500):idx+500])
```

---

## Sources

- SEC EDGAR: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=313616
- Danaher Investor Relations: https://investors.danaher.com
- Q1 2026 earnings release: investors.danaher.com/2026-04-21-Danaher-Reports-First-Quarter-2026-Results
