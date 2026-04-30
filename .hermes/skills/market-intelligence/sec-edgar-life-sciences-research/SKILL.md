---
name: sec-edgar-life-sciences-research
description: "Research life sciences / lab equipment companies (TMO, Agilent, DHR, WAT, etc.) using SEC EDGAR primary sources. Use when comparing competitors, verifying cross-company financial claims, or building market intelligence on the instruments/scientific tools sector. Replaces guesswork with primary-source verification and cross-company benchmarking."
---

# SEC EDGAR Life Sciences Research — Cross-Company Workflow

## When to Use

- Comparing software/digital strategy across TMO, Agilent, Danaher (DHR), Waters (WAT)
- Verifying a financial claim about a life sciences company from secondary sources
- Researching a competitor's recurring vs. non-recurring revenue mix
- Building competitive intelligence on instrument companies' software positioning
- Any task requiring primary-source financial data from US SEC filings

## Core Principle

**Life sciences instrument companies disclose less than you expect.** Key blind spots:
- Software revenue: **NOT separately disclosed** by any major instrument company (TMO, DHR, A, WAT)
- Order intake: typically **NOT disclosed** → use RPO/backlog proxies
- Recurring/non-recurring breakdown by **segment**: **NOT disclosed** → only company-wide
- Quarterly segment revenue: **NOT in 10-K** → requires 10-Q

## Step 1: Get ADSH from EFTS Search API (Always Start Here)

SEC's browse-edgar and direct HTML downloads frequently block automated requests. **Always use the EFTS search API first** to get the correct accession number (ADSH), then try direct download.

```python
import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cik = "0000097745"  # TMO example
search_url = f"https://efts.sec.gov/LATEST/search-index?q=%22thermo+fisher%22&forms=10-K&dateRange=custom&startdt=2025-02-01&enddt=2025-02-28"
req = urllib.request.Request(search_url, headers={'User-Agent': 'Research Bot research@example.com'})
with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
    data = json.loads(resp.read())

hits = data['hits']['hits']
tmo_hits = [h for h in hits if 'THERMO' in str(h['_source'].get('display_names', [])) and h['_source'].get('form') == '10-K']
for h in tmo_hits[:3]:
    src = h['_source']
    print(f"ADSH: {src['adsh']}, desc: {src['file_description']}, period: {src['period_ending']}, date: {src['file_date']}")
```

**EFTS search-index pattern** (works when browse-edgar is blocked):
```
https://efts.sec.gov/LATEST/search-index?q=<company+name>&forms=10-K&dateRange=custom&startdt=<YYYY-MM-DD>&enddt=<YYYY-MM-DD>
```

## Step 2: Download the 10-K / 10-Q Filing

**Try in this order:**

### Route A: SEC Archives direct HTML (most companies allow this)
```python
# Pattern: https://www.sec.gov/Archives/edgar/data/<CIK>/<ADSH-clean>/<filename>
# ADSH-clean = remove dashes from ADSH
adsh = "0000097745-25-000010"
acc = adsh.replace('-', '')  # → 000009774525000010
url = f"https://www.sec.gov/Archives/edgar/data/97745/{acc}/tmo-20241231.htm"
```

### Route B: annualreports.com PDF (fallback when SEC HTML is blocked)
```python
urls = [
    "https://www.annualreports.com/HostedData/AnnualReports/PDF/NYSE_TMO_2024.pdf",
    "https://www.annualreports.com/HostedData/AnnualReports/PDF/NYSE_A_2024.pdf",
    "https://www.annualreports.com/HostedData/AnnualReports/PDF/NYSE_DHR_2024.pdf",
]
```

### Route C: XBRL JSON API (for structured data)
```python
# Works for companies that expose XBRL via data.sec.gov
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK:010d}.json"
# Search for segment revenue: us-gaap.SegmentReportingInformationRevenue
```

**Known blocking patterns:**
- TMO: SEC HTML → 403 Forbidden. Annualreports.com PDF → WORKS (4.6MB)
- Agilent: SEC HTML via full Archives path → WORKS (3.7MB)
- Danaher: SEC HTML → sometimes works, sometimes blocked

## Step 3: Extract Text from PDF or HTML

### For PDF (annualreports.com):
```bash
# pdftotext not available on this system — use pypdf via uv
uv run --with pypdf python3 << 'EOF'
from pypdf import PdfReader
import re
r = PdfReader('/path/to/report.pdf')
text = ''
for p in r.pages:
    try:
        text += p.extract_text() + ' '
    except:
        pass
text = re.sub(r'\\s+', ' ', text)
# Now search
import re
for term in ['software', 'subscription', 'recurring']:
    hits = [(m.start(), text[max(0,m.start()-80):m.start()+250]) for m in re.finditer(term, text, re.I)]
    print(f'{term}: {len(hits)} hits')
EOF
```

### For HTML (SEC filings):
```python
import re
with open('filing.htm', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()
text = re.sub(r'<[^>]+>', ' ', content)
text = re.sub(r'\\s+', ' ', text)
```

### XBRL JSON API (company-facts endpoint)

```python
import urllib.request, json, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK:010d}.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Research Bot research@example.com', 'Accept': 'application/json'})
with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
    data = json.loads(resp.read())

# Structure: {facts: {us-gaap: {TAXONOMY_ELEMENT: {units: {USD: [{val, start, end, accn, fy, fp, form}...]}}}}
# Segment revenue key: us-gaap.SegmentReportingInformationRevenue
facts = data['facts']['us-gaap']
seg_keys = [k for k in facts.keys() if 'Segment' in k or 'Revenue' in k]
for k in seg_keys:
    v = facts[k]
    if isinstance(v, dict) and 'units' in v:
        for unit, data_list in list(v['units'].items())[:2]:
            recent = [d for d in data_list if isinstance(d, dict) and d.get('end','').startswith('2024')]
            if recent:
                print(f"{k} ({unit}): {recent}")
```

**XBRL JSON structure note:** The actual XBRL tag values are NOT in a top-level `us-gaap` key directly — they are inside `facts > us-gaap`. The initial top-level key check for `'us-gaap'` returns empty, but `data['facts']['us-gaap']` contains the actual taxonomy elements.

## Step 4: Cross-Company Software Revenue Comparison

**The finding (verified across TMO, DHR, A):** No major instrument company separately discloses software revenue. Software is always embedded.

**What to look for:**
1. Count "software" mentions in 10-K (Agilent: 88, TMO: 5, DHR: 5 — all embedded)
2. Revenue recognition description: is software license "point in time" (non-recurring) or "over time" (subscription)?
3. Agilent explicitly describes software license vs. maintenance contract treatment
4. TMO/DHR never quantify software separately

**Cross-company comparison table to build:**

| Company | Software mentions | Standalone software? | License = point-in-time? | Maintenance = subscription? |
|---------|-----------------|---------------------|------------------------|---------------------------|
| TMO | ~5 | ❌ No | Not described | Not described |
| DHR | ~5 | ❌ No | Yes (non-recurring) | Yes (recurring) |
| Agilent | ~88 | ❌ No | Yes | Yes |

**Recurring vs. Non-Recurring patterns:**
- Life sciences instrument companies typically: Consumables + Service = Recurring; Instruments = Non-recurring
- Software license: usually Non-recurring (point in time)
- Software maintenance/support contract: Recurring (over time)
- Operating lease (OTL): Recurring — but includes hardware too

## Step 5: Key URLs by Company

| Company | CIK | FY2024 10-K | FY2025 10-K | Annual Report PDF |
|---------|-----|------------|------------|-----------------|
| Thermo Fisher (TMO) | 0000097745 | tmo-20241231 | — | NYSE_TMO_2024.pdf |
| Danaher (DHR) | 0000313616 | dhr-20241231 | dhr-20251231 | NYSE_DHR_2024.pdf |
| Agilent (A) | 0001090872 | a-20241031 | a-20251031 | NYSE_A_2024.pdf |
| Waters (WAT) | 0001000690 | — | — | — |

## Key Findings to Report

### Software Business: All Three Are Instrument Companies, Not Software Companies

**TMO (Thermo Fisher):**
- No standalone software segment
- 5 mentions of "software" in FY2024 10-K — all in product description context
- Software = instrument companion (chromatography data systems, instrument control)
- Revenue: $42.88B total (FY2024): Laboratory Products 52% ($22.3B), Analytical Instruments 17% ($7.3B), Life Sciences 21% ($9.0B), Specialty Diagnostics 10% ($4.3B)

**Danaher (DHR):**
- Software embedded in recurring revenue (service + OTL) or non-recurring (license)
- Q1 OTL (operating lease) = $143M — includes software-as-service component, also hardware
- 10-Q MD&A唯一提到的数字化描述: "data connectivity and automation" — equipment IoT, not AI/ML analytics
- Revenue: $24.6B total (FY2025): Biotechnology $7.3B, Life Sciences $7.3B, Diagnostics $9.9B

**Agilent (A):**
- Most software-forward disclosure: 88 mentions in FY2024 10-K
- Explicitly describes: software license (non-recurring, point in time) vs. maintenance contract (recurring, over time)
- Software products: MassHunter (LC/GC-MS), Cytation (cell imaging), Cartographer (column database)
- CrossLab segment (service + software)唯一实现增长: +5%
- Revenue: $6.51B total (FY2024): LSAMS 下降8%, Diagnostics & Genomics 下降6%, CrossLab 增长5%

### Conclusion

None of these companies have a standalone SaaS or software product line that contributes independent valuation. Software is a **customer retention / instrument ecosystem lock-in tool** bundled with:
- Instruments (配套软件)
- Service contracts (维护合同)
- Consumables (试剂数据包)

This is structurally different from pure-play software companies (Illumina BaseSpace, Dassault BIOVIA) that do separately disclose software revenue.

## Troubleshooting

| Problem | Solution |
|---------|---------|
| SEC browse-edgar returns 403 | Use EFTS search-index API to find ADSH first |
| SEC HTML returns 403 Forbidden | Try annualreports.com PDF as fallback |
| TMO 10-K HTML blocked | Use annualreports.com PDF directly |
| Agilent 10-K blocked at efts.sec.gov | Use full Archives path: `https://www.sec.gov/Archives/edgar/data/1090872/000109087224000067/a-20241031.htm` |
| pdftotext not available | Use `uv run --with pypdf python3` |
| XBRL JSON returns 404 | Company may not expose XBRL via data.sec.gov — use HTML/PDF instead |
| Browser tools (browser_navigate) fail | Never use browser for SEC — direct HTTP via Python urllib is more reliable |
| SEC rate limiting | Add delay between requests; use `User-Agent` with real-looking string |
