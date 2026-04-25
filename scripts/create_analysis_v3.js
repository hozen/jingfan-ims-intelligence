const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "IMS竞争分析报告 - 2026环博会实测数据";
pres.author = "Hach IMS战略规划团队";

// Color palette
const PRIMARY = "1F4E79";      // Dark blue
const SECONDARY = "4472C4";   // Medium blue
const ACCENT = "ED7D31";      // Orange
const LIGHT_BG = "F2F2F2";
const DARK_TEXT = "1F1F1F";
const WHITE = "FFFFFF";
const GREEN = "70AD47";
const RED = "C00000";
const YELLOW = "FFC000";

// ========== SLIDE 1: 封面 ==========
let slide1 = pres.addSlide();
slide1.background = { color: PRIMARY };

// Title
slide1.addText("IMS竞争分析报告", {
  x: 0.5, y: 1.8, w: 9, h: 1,
  fontSize: 44, fontFace: "Arial", bold: true, color: WHITE, align: "center"
});

slide1.addText("2026环博会现场实证", {
  x: 0.5, y: 2.9, w: 9, h: 0.6,
  fontSize: 28, fontFace: "Arial", color: ACCENT, align: "center"
});

slide1.addText("基于实测展商数据 × 专家小组研判", {
  x: 0.5, y: 3.6, w: 9, h: 0.5,
  fontSize: 18, fontFace: "Arial", color: "B8CCE4", align: "center"
});

slide1.addShape(pres.shapes.LINE, {
  x: 3, y: 4.3, w: 4, h: 0,
  line: { color: ACCENT, width: 2 }
});

slide1.addText("哈希公司 IMS产品线", {
  x: 0.5, y: 4.8, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Arial", color: "B8CCE4", align: "center"
});

// ========== SLIDE 2: 实测展商数据 ==========
let slide2 = pres.addSlide();
slide2.background = { color: WHITE };

// Header bar
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9,
  fill: { color: PRIMARY }
});

slide2.addText("已确认参展数据（实测）", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 26, fontFace: "Arial", bold: true, color: WHITE, margin: 0
});

// Data source note
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 0.5,
  fill: { color: "FFF2CC" }
});

slide2.addText("数据来源: 展商名单图片 + 用户现场确认 | 截至2026年4月18日", {
  x: 0.6, y: 1.2, w: 8.8, h: 0.3,
  fontSize: 11, fontFace: "Arial", color: "7F6000", margin: 0
});

// Hach section
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.8, w: 2.8, h: 0.4,
  fill: { color: SECONDARY }
});

slide2.addText("✅ 哈希 Hach", {
  x: 0.5, y: 1.8, w: 2.8, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
});

slide2.addText([
  { text: "E1565 / E1625 / E1636", options: { bold: true, breakLine: true } },
  { text: "过程仪表技术（上海）有限公司", options: { breakLine: true } },
  { text: "水质监测 + 实验室仪器 + 试剂耗材", options: {} }
], {
  x: 0.5, y: 2.3, w: 2.8, h: 1.2,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// E+H section
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 3.6, y: 1.8, w: 2.8, h: 0.4,
  fill: { color: SECONDARY }
});

slide2.addText("✅ E+H", {
  x: 3.6, y: 1.8, w: 2.8, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
});

slide2.addText([
  { text: "E1612 / E1632", options: { bold: true, breakLine: true } },
  { text: "恩德斯豪斯（中国）自动化有限公司", options: { breakLine: true } },
  { text: "过程仪表 + 物位 + 流量 + 分析仪", options: {} }
], {
  x: 3.6, y: 2.3, w: 2.8, h: 1.2,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// Veolia section
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 6.7, y: 1.8, w: 2.8, h: 0.4,
  fill: { color: GREEN }
});

slide2.addText("✅ 威立雅 Veolia", {
  x: 6.7, y: 1.8, w: 2.8, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
});

slide2.addText([
  { text: "展位号待确认", options: { bold: true, breakLine: true } },
  { text: "威立雅（中国）环境服务有限公司", options: { breakLine: true } },
  { text: "综合环境治理 + 水务运营", options: {} }
], {
  x: 6.7, y: 2.3, w: 2.8, h: 1.2,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// Key insight box
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.7, w: 9, h: 0.6,
  fill: { color: "DEEBF7" }
});

slide2.addText("关键洞察: E+H与哈希在E1馆直接对标，展位相邻。威立雅定位综合环境服务，与哈希IMS存在合作关系大于竞争。", {
  x: 0.6, y: 3.8, w: 8.8, h: 0.4,
  fontSize: 12, fontFace: "Arial", color: PRIMARY, margin: 0
});

// Data gap warning
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.5, w: 9, h: 0.8,
  fill: { color: "FCE4D6" }
});

slide2.addText("⚠️ 数据缺口: E3/E4馆（环境监测/过程控制）展商图片无法OCR识别，需用户补充5-10家实际观察到的展商名称，方可构建完整竞争矩阵。", {
  x: 0.6, y: 4.6, w: 8.8, h: 0.6,
  fontSize: 12, fontFace: "Arial", color: RED, margin: 0
});

// ========== SLIDE 3: 专家小组研判 - 竞争格局 ==========
let slide3 = pres.addSlide();
slide3.background = { color: WHITE };

slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9,
  fill: { color: PRIMARY }
});

slide3.addText("专家小组研判: 竞争格局定位", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 26, fontFace: "Arial", bold: true, color: WHITE, margin: 0
});

// 2x2 Matrix
slide3.addText("IMS市场竞争定位矩阵", {
  x: 0.5, y: 1.1, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true, color: DARK_TEXT
});

// Y-axis label
slide3.addText("技术深度 →", {
  x: 0.1, y: 2.8, w: 0.5, h: 0.5,
  fontSize: 10, fontFace: "Arial", color: DARK_TEXT, rotate: 270
});

// X-axis label  
slide3.addText("市场覆盖广度 →", {
  x: 3.5, y: 5.0, w: 2, h: 0.3,
  fontSize: 10, fontFace: "Arial", color: DARK_TEXT
});

// Quadrant labels
slide3.addText("高端专业", {
  x: 0.5, y: 1.5, w: 2, h: 0.3,
  fontSize: 10, fontFace: "Arial", color: "7F7F7F"
});

slide3.addText("平台整合", {
  x: 2.5, y: 1.5, w: 2, h: 0.3,
  fontSize: 10, fontFace: "Arial", color: "7F7F7F"
});

slide3.addText("利基细分", {
  x: 0.5, y: 4.2, w: 2, h: 0.3,
  fontSize: 10, fontFace: "Arial", color: "7F7F7F"
});

slide3.addText("规模竞争", {
  x: 2.5, y: 4.2, w: 2, h: 0.3,
  fontSize: 10, fontFace: "Arial", color: "7F7F7F"
});

// Hach marker
slide3.addShape(pres.shapes.OVAL, {
  x: 1.5, y: 2.0, w: 0.5, h: 0.5,
  fill: { color: SECONDARY }
});
slide3.addText("哈希", {
  x: 1.5, y: 2.0, w: 0.5, h: 0.5,
  fontSize: 9, fontFace: "Arial", color: WHITE, align: "center", valign: "middle", margin: 0
});

// E+H marker
slide3.addShape(pres.shapes.OVAL, {
  x: 2.0, y: 2.5, w: 0.5, h: 0.5,
  fill: { color: SECONDARY }
});
slide3.addText("E+H", {
  x: 2.0, y: 2.5, w: 0.5, h: 0.5,
  fontSize: 9, fontFace: "Arial", color: WHITE, align: "center", valign: "middle", margin: 0
});

// Veolia marker
slide3.addShape(pres.shapes.OVAL, {
  x: 3.0, y: 3.0, w: 0.5, h: 0.5,
  fill: { color: GREEN }
});
slide3.addText("威立雅", {
  x: 3.0, y: 3.0, w: 0.5, h: 0.5,
  fontSize: 9, fontFace: "Arial", color: WHITE, align: "center", valign: "middle", margin: 0
});

// Right side: Key insights
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.1, w: 4.3, h: 4.2,
  fill: { color: LIGHT_BG }
});

slide3.addText("战略分析专家观点", {
  x: 5.4, y: 1.3, w: 4, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true, color: PRIMARY
});

slide3.addText([
  { text: "竞争层级（已确认）", options: { bold: true, breakLine: true } },
  { text: "• 哈希 vs E+H: 直接对标，技术路线相似（在线水质监测+过程控制）", options: { breakLine: true } },
  { text: "• 威立雅: 水务运营背景，采购决策人角色，非直接技术竞争", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "市场威胁分层", options: { bold: true, breakLine: true } },
  { text: "• L1威胁: E+H（技术同质化）", options: { breakLine: true } },
  { text: "• L2威胁: 软件平台跨界（AVEVA PI, Siemens）", options: { breakLine: true } },
  { text: "• L3威胁: 云厂商（阿里云、华为云）", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "数据缺口限制", options: { bold: true, breakLine: true } },
  { text: "E3/E4馆展商数据缺失，无法评估国内厂商真实竞争压力", options: {} }
], {
  x: 5.4, y: 1.8, w: 4, h: 3.3,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// ========== SLIDE 4: SWOT分析 ==========
let slide4 = pres.addSlide();
slide4.background = { color: WHITE };

slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9,
  fill: { color: PRIMARY }
});

slide4.addText("哈希IMS - SWOT战略分析（基于实测数据）", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 26, fontFace: "Arial", bold: true, color: WHITE, margin: 0
});

// Strengths (green)
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 4.3, h: 2.0,
  fill: { color: "E2EFDA" }
});

slide4.addText("S 优势", {
  x: 0.6, y: 1.2, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true, color: GREEN
});

slide4.addText([
  { text: "• 哈希品牌在水务行业的高认知度", options: { breakLine: true } },
  { text: "• 三个展位曝光（E1565/E1625/E1636），视觉覆盖大", options: { breakLine: true } },
  { text: "• 实验室+在线双线产品组合", options: { breakLine: true } },
  { text: "• Veolia关系网络（合作>竞争）", options: {} }
], {
  x: 0.6, y: 1.6, w: 4, h: 1.4,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// Weaknesses (red)
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.1, w: 4.3, h: 2.0,
  fill: { color: "FCE4D6" }
});

slide4.addText("W 劣势", {
  x: 5.3, y: 1.2, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true, color: RED
});

slide4.addText([
  { text: "• 与E+H同馆，价格竞争压力大", options: { breakLine: true } },
  { text: "• 国内厂商价格冲击（成本优势）", options: { breakLine: true } },
  { text: "• 软件平台整合能力弱", options: { breakLine: true } },
  { text: "• 数据缺口导致战略盲区", options: {} }
], {
  x: 5.3, y: 1.6, w: 4, h: 1.4,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// Opportunities (blue)
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.3, w: 4.3, h: 2.0,
  fill: { color: "DEEBF7" }
});

slide4.addText("O 机会", {
  x: 0.6, y: 3.4, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true, color: SECONDARY
});

slide4.addText([
  { text: "• 双碳政策驱动智能监测需求", options: { breakLine: true } },
  { text: "• 云边协同架构升级窗口期", options: { breakLine: true } },
  { text: "• 与Veolia等运营商战略合作", options: { breakLine: true } },
  { text: "• 国产化替代政策加持", options: {} }
], {
  x: 0.6, y: 3.8, w: 4, h: 1.4,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// Threats (yellow/orange)
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 3.3, w: 4.3, h: 2.0,
  fill: { color: "FFF2CC" }
});

slide4.addText("T 威胁", {
  x: 5.3, y: 3.4, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true, color: "7F6000"
});

slide4.addText([
  { text: "• E+H直接竞争（同馆，相邻展位）", options: { breakLine: true } },
  { text: "• 软件平台跨界打劫（AVEVA/Siemens）", options: { breakLine: true } },
  { text: "• 云厂商低价策略（阿里/华为/腾讯）", options: { breakLine: true } },
  { text: "• 国内厂商性价比竞争", options: {} }
], {
  x: 5.3, y: 3.8, w: 4, h: 1.4,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// ========== SLIDE 5: 行动建议 ==========
let slide5 = pres.addSlide();
slide5.background = { color: WHITE };

slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9,
  fill: { color: PRIMARY }
});

slide5.addText("行动建议（90天作战路径）", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 26, fontFace: "Arial", bold: true, color: WHITE, margin: 0
});

// Immediate actions (30 days)
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 1.3,
  fill: { color: "FCE4D6" }
});

slide5.addText("⚡ 30天内 - 数据补全与客户跟进", {
  x: 0.6, y: 1.2, w: 8.8, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true, color: RED
});

slide5.addText([
  { text: "1. 补充E3/E4展商名单（用户提供5-10家实际观察）→ 构建完整竞争矩阵", options: { breakLine: true } },
  { text: "2. 展会客户线索清洗→ 销售团队24小时触达", options: { breakLine: true } },
  { text: "3. E+H同馆竞品话术准备→ 差异化对比文档", options: {} }
], {
  x: 0.6, y: 1.6, w: 8.8, h: 0.8,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// Medium term (60 days)
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 2.6, w: 9, h: 1.3,
  fill: { color: "FFF2CC" }
});

slide5.addText("📅 60天内 - 竞争策略深化", {
  x: 0.6, y: 2.7, w: 8.8, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true, color: "7F6000"
});

slide5.addText([
  { text: "1. 完成E3/E4展商深度调研→ 竞品产品/价格/策略分析", options: { breakLine: true } },
  { text: "2. 与Veolia等运营商建立IMS联合推广合作", options: { breakLine: true } },
  { text: "3. 软件平台合作方案（AVEVA PI/华为云）→ 集成落地", options: {} }
], {
  x: 0.6, y: 3.1, w: 8.8, h: 0.8,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// Long term (90 days)
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.1, w: 9, h: 1.3,
  fill: { color: "E2EFDA" }
});

slide5.addText("🎯 90天内 - 战略成果转化", {
  x: 0.6, y: 4.2, w: 8.8, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true, color: GREEN
});

slide5.addText([
  { text: "1. 展会社群沉淀→ 微信社群/LinkedIn运营", options: { breakLine: true } },
  { text: "2. IMS白皮书发布→ 行业影响力构建", options: { breakLine: true } },
  { text: "3. 下届展会预订→ 锁定核心展位", options: {} }
], {
  x: 0.6, y: 4.6, w: 8.8, h: 0.8,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// ========== SLIDE 6: 数据缺口与下一步 ==========
let slide6 = pres.addSlide();
slide6.background = { color: WHITE };

slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9,
  fill: { color: PRIMARY }
});

slide6.addText("当前数据缺口 & 所需支持", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 26, fontFace: "Arial", bold: true, color: WHITE, margin: 0
});

// Data gap summary
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 1.0,
  fill: { color: "FCE4D6" }
});

slide6.addText("⚠️ 关键数据缺口", {
  x: 0.6, y: 1.2, w: 8.8, h: 0.35,
  fontSize: 14, fontFace: "Arial", bold: true, color: RED
});

slide6.addText("E3/E4馆展商名单（图片OCR识别失败）。展商名单图片无法通过AI自动识别，需要人工输入或现场拍摄的真实展商数据。", {
  x: 0.6, y: 1.55, w: 8.8, h: 0.45,
  fontSize: 11, fontFace: "Arial", color: DARK_TEXT
});

// What we need from user
slide6.addText("请您补充以下信息（任意选择）：", {
  x: 0.5, y: 2.3, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Arial", bold: true, color: PRIMARY
});

slide6.addText([
  { text: "A. E3馆展商名称（3-5家即可）", options: { bullet: true, breakLine: true } },
  { text: "B. E4馆展商名称（3-5家即可）", options: { bullet: true, breakLine: true } },
  { text: "C. 展会现场拍摄的名片/资料照片", options: { bullet: true, breakLine: true } },
  { text: "D. 您记得的任何展商名称", options: { bullet: true } }
], {
  x: 0.8, y: 2.7, w: 8, h: 1.5,
  fontSize: 13, fontFace: "Arial", color: DARK_TEXT
});

// Next step CTA
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.4, w: 9, h: 0.9,
  fill: { color: SECONDARY }
});

slide6.addText("收到您的补充数据后 → 立即生成完整竞争分析PPT（含E3/E4展商矩阵）", {
  x: 0.6, y: 4.6, w: 8.8, h: 0.5,
  fontSize: 16, fontFace: "Arial", bold: true, color: WHITE, align: "center", margin: 0
});

// Save
pres.writeFile({ fileName: "/home/agentuser/IMS竞争分析报告_v3_实测版.pptx" })
  .then(() => console.log("PPT created: IMS竞争分析报告_v3_实测版.pptx"))
  .catch(err => console.error("Error:", err));
