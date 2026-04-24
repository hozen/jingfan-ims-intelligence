---
name: competitive-analysis-workshop
description: "Run a competitive analysis project with multi-expert panel framing and structured frameworks. Use when user asks for competitive intelligence, market analysis, or strategic business research. Combines web research, expert role assignment, and framework-driven analysis delivered as actionable PPT/report."
license: Proprietary
---

# Competitive Analysis Workshop Skill

## When to Use

Trigger when user asks for:
- Competitive analysis / competitive intelligence
- Market landscape / competitive positioning
- "What are competitors doing?" type questions
- Strategic research for business decisions
- SWOT analysis, Porter's Five Forces, or similar frameworks

## Core Approach

### 1. Expert Panel Framing

Assign **4 distinct expert roles** to provide diverse analytical perspectives:

| Role | Focus | Frameworks |
|------|-------|------------|
| 战略分析专家 | 竞争格局与战略定位 | 波特五力 + 价值链分析 |
| 产品技术专家 | 产品功能与技术能力 | 功能对比矩阵 + 技术成熟度 |
| 市场情报专家 | 市场趋势与竞争动态 | SWOT + 趋势外推 |
| 商务模式专家 | 定价策略与商业模式 | LTV/CAC + 订阅制分析 |

### 2. Research Workflow

```
1. Verify assumptions first - ask user or research "who actually exhibited/showed up"
2. Research international competitors (ABB, Siemens, Yokogawa, E+H if relevant)
3. Research domestic/Chinese competitors (local brands, pricing, government relations)
4. Identify market trends (software platforms, subscription models, AI integration)
5. Compile findings into structured frameworks
```

### 3. Framework Selection

**For product/technology analysis:**
- SWOT (Strengths, Weaknesses, Opportunities, Threats)
- Feature comparison matrix
- Technology maturity curve

**For market/competitive analysis:**
- Porter's Five Forces
- Competitive positioning matrix (2x2: e.g., 技术实力 vs 市场覆盖)
- Threat assessment grid (高/中/低)

**For business model analysis:**
- Subscription/LTV analysis
- TCO (Total Cost of Ownership) comparison

### 4. Output Format

Deliver as **structured PPT with professional design**:
- Title slide with expert panel branding
- Framework overview slide
- Competitor exhibitor landscape (if trade show context)
- Deep-dive SWOT or analysis per major competitor
- Positioning matrix visualization
- Actionable conclusions with specific timelines

**Design principles:**
- Dark backgrounds for title/conclusion, light for content ("sandwich")
- Color-coded threat levels (red=高威胁, yellow=中威胁, green=低威胁)
- Framework visualizations (2x2 matrices, SWOT quadrants)
- Specific, actionable recommendations (not generic "加强" statements)

## Critical Rules

### Verify Before Assuming
- If user mentions a specific event (trade show, conference), **verify who actually participated**
- Don't assume international competitors are present at Chinese domestic events
- E+H, ABB, Siemens may or may not appear at Chinese regional trade shows

### User Feedback is Mandatory
- This user explicitly rejected "worthless" template content multiple times
- If content feels generic, pivot to more specific, actionable analysis
- Ask clarifying questions about which competitors matter most

### Actionable > Comprehensive
- 3 specific actions > 10 vague recommendations
- Include timelines (90天, 30天, 72小时)
- Name specific customer segments (半导体, 制药, 市政)

## Output File

Save competitive analysis PPT to:
```
/home/agentuser/IMS竞争分析报告_环博会_专家小组.pptx
```

## Example Slide Structure

1. **封面** - 竞争分析报告 + 专家小组阵容
2. **分析框架** - 四位专家角色定义
3. **参展商全景** - 重要发现（确认谁实际参展）
4. **竞争对手SWOT** - 每家主要竞品一页
5. **波特五力** - 竞争强度分析
6. **竞争定位矩阵** - 2x2可视化
7. **综合SWOT + 行动方案** - SO/WT战略 + 90天计划
8. **核心结论** - 三点关键发现

## Dependencies

- pptxgenjs for PPT generation
- Browser/camoufox for web research
- markitdown for content verification
