---
name: eastmoney-announcement-api
description: Research Chinese A-share listed companies using East Money announcement API. Pull announcement lists and full text content for stocks on SSE/SZSE.
triggers:
  - "A股公告查询"
  - "上交所公告"
  - "东方财富公告"
  - "股票 公告 抓取"
  - "audit opinion research China"
---

# East Money A股公告API研究法

## 功能
通过东方财富网（East Money）API抓取A股上市公司的公告列表和全文内容，适用于上交所/深交所上市公司的公开信息收集。

## 核心API端点

### 1. 公告列表API
```
GET https://np-anotice-stock.eastmoney.com/api/security/ann
```

**参数：**
| 参数 | 值 | 说明 |
|------|-----|------|
| sr | -1 | 降序排列 |
| page_size | 50 | 每页数量 |
| page_index | 1,2,3... | 页码 |
| ann_type | A%2CSHA | 沪市A股（深市需试ann_type=SZA） |
| client_source | web | |
| stock_list | 600745 | 股票代码 |

**返回字段：**
- `art_code` — 公告唯一标识符（获取全文的钥匙）
- `notice_date` — 公告日期
- `title_ch` — 公告标题

### 2. 公告全文API
```
GET https://np-cnotice-stock.eastmoney.com/api/content/ann
```

**参数：**
| 参数 | 值 | 说明 |
|------|-----|------|
| art_code | AN202601301818591388 | 来自列表API |
| client_source | web | |
| page | 1 | |
| ann_type | A,SHA | |

**返回字段：**
- `data.notice_content` — 纯文本内容
- `data.attach_list[].attach_url` — PDF附件链接

## Python完整示例

```python
import urllib.request
import json

def get_announcement_list(stock_code, page=1):
    url = (f"https://np-anotice-stock.eastmoney.com/api/security/ann"
           f"?sr=-1&page_size=50&page_index={page}&ann_type=A%2CSHA"
           f"&client_source=web&stock_list={stock_code}")
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json', 'Referer': 'https://data.eastmoney.com/'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data.get('data', {}).get('list', [])

def get_announcement_content(art_code):
    url = (f"https://np-cnotice-stock.eastmoney.com/api/content/ann"
           f"?art_code={art_code}&client_source=web&page=1&ann_type=A,SHA")
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com/', 'Accept': 'application/json'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode('utf-8')
        data = json.loads(raw)
        return data.get('data', {}).get('notice_content', '')

# 示例：获取公告列表并找关键公告
anns = get_announcement_list('600745')
for ann in anns:
    if any(k in ann['title_ch'] for k in ['业绩预告', '审计', '问询函', '变更会计师']):
        print(f"{ann['notice_date'][:10]} | {ann['title_ch']} | {ann['art_code']}")

# 获取特定公告全文
content = get_announcement_content('AN202601301818591388')
print(content[:2000])
```

## 踩坑记录

1. **公告列表每页50条**，需翻页覆盖更长时间
2. **art_code是获取全文的钥匙** — 来自列表API，不在标题里
3. **art_code格式** — 通常是`AN+日期时间戳+序号`，如`AN202601301818591388`
4. **常见错误响应：**
   - `{"success":0,"error":"基本信息为空！"}` → art_code格式错误
   - `{"result":null,"code":9501}` → API端点名称错误
5. **PDF附件URL格式：**
   ```
   https://pdf.dfcfw.com/pdf/H2_AN{art_code}_1.pdf
   ```

## 关键公告类型关键词

| 公告类型 | 关键词 |
|---------|--------|
| 年度业绩 | 业绩预告、年度业绩 |
| 审计意见 | 审计报告、标准无保留意见、保留意见、无法表示 |
| 监管问询 | 问询函、问询函回复 |
| 审计师变更 | 变更会计师事务所 |
| 信用评级 | 评级调整、信用等级 |
| 可转债 | 转债、转股价格、赎回 |
| 停复牌 | 停牌、复牌 |
| 重大资产 | 重大资产出售、重大资产重组 |
| 高管变动 | 董事辞职、高管变动 |
| 股东减持 | 股东减持、股份转让 |

## 适用场景
- A股持仓风险评估（审计意见、监管问询、财务风险）
- 事件驱动研究（并购重组、高管变动）
- 竞品动态跟踪（上市公司公告）
- 尽职调查（审计师变更、内控问题）
