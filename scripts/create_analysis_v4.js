const pptxgen = require("pptxgenjs");

// ─── Verified Exhibitor Data (from 828i.com confirmed + user observations) ───
// E1馆: Hach(E1565/E1625/E1636), E+H(E1612/E1632)
// User confirmed: Veolia also exhibited
// Official expo stats: 1,987 exhibitors, 20 countries, 82,419 visitors, 17万㎡

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "IMS竞争分析报告_v4_官方数据版";
pres.author = "哈希中国IMS战略规划";

// ─── Slide 1: 封面 ───
let slide1 = pres.addSlide();
slide1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: "0D2137" } });
slide1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 4.4, w: 10, h: 1.225, fill: { color: "0078D4" } });
slide1.addText("IMS竞争分析报告", { x: 0.5, y: 1.5, w: 9, h: 1, fontSize: 44, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei" });
slide1.addText("2026环博会参展后深度分析 | 官方数据验证版", { x: 0.5, y: 2.5, w: 9, h: 0.6, fontSize: 22, color: "CCCCCC", fontFace: "Microsoft YaHei" });
slide1.addText("哈希中国 IMS产品线", { x: 0.5, y: 4.6, w: 5, h: 0.5, fontSize: 16, color: "FFFFFF", fontFace: "Microsoft YaHei" });
slide1.addText("2026年4月18日", { x: 7, y: 4.6, w: 2.5, h: 0.5, fontSize: 14, color: "AAAAAA", fontFace: "Microsoft YaHei", align: "right" });

// ─── Slide 2: 官方数据 — 展会规模 ───
let slide2 = pres.addSlide();
slide2.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.8, fill: { color: "0078D4" } });
slide2.addText("官方数据：2026环博会规模", { x: 0.3, y: 0.15, w: 9, h: 0.5, fontSize: 22, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei" });

const stats = [
  { value: "1,987", label: "参展企业", color: "0078D4" },
  { value: "82,419", label: "专业观众", color: "107C10" },
  { value: "20", label: "参展国家", color: "FF8C00" },
  { value: "119", label: "观众来源国", color: "881798" },
];
stats.forEach((s, i) => {
  const x = 0.5 + i * 2.35;
  slide2.addShape(pres.shapes.RECTANGLE, { x, y: 1.2, w: 2.1, h: 1.6, fill: { color: "F0F0F0" }, line: { color: "CCCCCC", width: 1 } });
  slide2.addText(s.value, { x, y: 1.35, w: 2.1, h: 0.9, fontSize: 36, bold: true, color: s.color, fontFace: "Arial", align: "center" });
  slide2.addText(s.label, { x, y: 2.2, w: 2.1, h: 0.4, fontSize: 13, color: "555555", fontFace: "Microsoft YaHei", align: "center" });
});

slide2.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.1, w: 9, h: 2.2, fill: { color: "FAFAFA" }, line: { color: "E0E0E0", width: 1 } });
slide2.addText([
  { text: "展馆布局：", options: { bold: true, breakLine: true } },
  { text: "E1/E2馆 = 过程控制与仪表 | E3/E4馆 = 环境监测/仪表 | N馆 = 新能源/综合", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "哈希展位（E1馆）：E1565 / E1625 / E1636", options: { bold: true, color: "0078D4", breakLine: true } },
  { text: "E+H展位（E1馆）：E1612 / E1632", options: { bold: true, color: "107C10", breakLine: true } },
  { text: "威立雅：已确认参展（展位号未知）", options: { color: "881798" } },
], { x: 0.7, y: 3.25, w: 8.6, h: 2, fontSize: 14, color: "333333", fontFace: "Microsoft YaHei" });

slide2.addText("数据来源：第27届上海国际环博会官方闭幕报告 (2026.04.17)", { x: 0.5, y: 5.35, w: 9, h: 0.25, fontSize: 10, color: "999999", fontFace: "Microsoft YaHei" });

// ─── Slide 3: 官方定调 — 行业趋势 ───
let slide3 = pres.addSlide();
slide3.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.8, fill: { color: "0078D4" } });
slide3.addText("官方定调：行业转型方向", { x: 0.3, y: 0.15, w: 9, h: 0.5, fontSize: 22, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei" });

// Quote box
slide3.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.1, w: 9, h: 1.4, fill: { color: "E8F4FD" }, line: { color: "0078D4", width: 2 } });
slide3.addText([
  { text: "「数字化、智能化技术已从'辅助工具'升级为环保治理的'核心引擎'」", options: { bold: true, breakLine: true } },
  { text: "—— 官方闭幕报告", options: { fontSize: 12, color: "666666", italic: true } },
], { x: 0.7, y: 1.25, w: 8.6, h: 1.1, fontSize: 18, color: "0D2137", fontFace: "Microsoft YaHei" });

// Two columns
const trends = [
  { title: "转型逻辑", points: ["从「末端治理」→「全链条协同」", "从「规模驱动」→「质量驱动」", "跨领域、多介质、系统协同"] },
  { title: "技术热点", points: ["AI + 环保治理深度融合", "物联网 + 精准监测", "大数据 + 高效运维"] },
];
trends.forEach((t, i) => {
  const x = 0.5 + i * 4.7;
  slide3.addShape(pres.shapes.RECTANGLE, { x, y: 2.75, w: 4.4, h: 2.5, fill: { color: "FAFAFA" }, line: { color: "DDDDDD", width: 1 } });
  slide3.addText(t.title, { x: x + 0.15, y: 2.85, w: 4.1, h: 0.4, fontSize: 15, bold: true, color: "0078D4", fontFace: "Microsoft YaHei" });
  slide3.addText(t.points.map(p => ({ text: "• " + p, options: { breakLine: true } })), { x: x + 0.15, y: 3.3, w: 4.1, h: 1.8, fontSize: 13, color: "333333", fontFace: "Microsoft YaHei" });
});

slide3.addText("哈希被官方报道引用：市场主管孙思聪评价「本次环博会哈希携新品家族亮相，聚焦水处理全场景监测解决方案」", { x: 0.5, y: 5.35, w: 9, h: 0.25, fontSize: 10, color: "0078D4", fontFace: "Microsoft YaHei" });

// ─── Slide 4: 三层竞争格局（已验证） ───
let slide4 = pres.addSlide();
slide4.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.8, fill: { color: "107C10" } });
slide4.addText("已验证展商 — 三层竞争格局", { x: 0.3, y: 0.15, w: 9, h: 0.5, fontSize: 22, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei" });

const layers = [
  { 
    layer: "L1 仪表硬件层", color: "1E88E5",
    exhibitors: [
      { name: "哈希 Hach", booth: "E1565/E1625/E1636", verified: true, note: "官方报道引用，新品家族亮相" },
      { name: "E+H Endress+Hauser", booth: "E1612/E1632", verified: true, note: "FieldEdge IIoT平台" },
      { name: "威立雅 Veolia", booth: "未知", verified: true, note: "用户确认参展" },
    ]
  },
  {
    layer: "L2 软件平台层", color: "7B1FA2",
    exhibitors: [
      { name: "AVEVA (Schneider)", booth: "预计参展", verified: false, note: "OSoft PI/ Wonderware" },
      { name: "Siemens", booth: "预计参展", verified: false, note: "WinCC / MindSphere" },
    ]
  },
  {
    layer: "L3 云厂商/系统集成层", color: "C62828",
    exhibitors: [
      { name: "阿里云", booth: "市场威胁", verified: false, note: "非实际参展商" },
      { name: "华为云", booth: "市场威胁", verified: false, note: "非实际参展商" },
    ]
  }
];

let yPos = 1.0;
layers.forEach((l) => {
  slide4.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: yPos, w: 9.4, h: 0.35, fill: { color: l.color } });
  slide4.addText(l.layer, { x: 0.4, y: yPos + 0.02, w: 3, h: 0.3, fontSize: 13, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei" });
  yPos += 0.38;
  l.exhibitors.forEach((ex) => {
    const bg = ex.verified ? "FFFFFF" : "FFF8E1";
    const border = ex.verified ? "CCCCCC" : "FFE082";
    slide4.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: yPos, w: 9.4, h: 0.5, fill: { color: bg }, line: { color: border, width: 0.5 } });
    slide4.addText(ex.name, { x: 0.45, y: yPos + 0.08, w: 2.5, h: 0.35, fontSize: 12, bold: true, color: l.color, fontFace: "Microsoft YaHei" });
    slide4.addText(ex.booth, { x: 2.9, y: yPos + 0.08, w: 2.2, h: 0.35, fontSize: 11, color: "555555", fontFace: "Microsoft YaHei" });
    slide4.addText(ex.note, { x: 5.1, y: yPos + 0.08, w: 4.4, h: 0.35, fontSize: 10, color: "777777", fontFace: "Microsoft YaHei" });
    if (!ex.verified) slide4.addText("⚠ 待验证", { x: 8.6, y: yPos + 0.08, w: 1, h: 0.35, fontSize: 9, color: "FF8C00", fontFace: "Microsoft YaHei" });
    yPos += 0.52;
  });
  yPos += 0.1;
});

slide4.addText("✅ = 官方确认/用户确认  ⚠ = 基于历史数据预测，需现场核实", { x: 0.3, y: 5.35, w: 9.4, h: 0.25, fontSize: 10, color: "999999", fontFace: "Microsoft YaHei" });

// ─── Slide 5: Porter's Five Forces ───
let slide5 = pres.addSlide();
slide5.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.8, fill: { color: "881798" } });
slide5.addText("波特五力分析 — IMS赛道", { x: 0.3, y: 0.15, w: 9, h: 0.5, fontSize: 22, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei" });

const forces = [
  { force: "现有竞争者", level: "高", color: "C62828", detail: "哈希 vs E+H正面竞争；威立雅一体化方案威胁" },
  { force: "新进入者威胁", level: "中", color: "FF8C00", detail: "云厂商（阿里/华为）从平台层向下切入仪表层" },
  { force: "替代品威胁", level: "中高", color: "FF8C00", detail: "便携式监测仪、无人监测站替代传统在线仪表" },
  { force: "供应商议价", level: "低", color: "107C10", detail: "传感器/芯片供应商分散，议价能力弱" },
  { force: "客户议价", level: "中高", color: "FF8C00", detail: "市政大客户招标压价；工业客户需求定制化" },
];

forces.forEach((f, i) => {
  const y = 1.0 + i * 0.88;
  slide5.addShape(pres.shapes.RECTANGLE, { x: 0.3, y, w: 2.2, h: 0.75, fill: { color: f.color } });
  slide5.addText(f.force, { x: 0.3, y: y + 0.15, w: 2.2, h: 0.45, fontSize: 13, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei", align: "center" });
  slide5.addShape(pres.shapes.RECTANGLE, { x: 2.5, y, w: 0.8, h: 0.75, fill: { color: f.color }, line: { color: f.color, width: 0 } });
  slide5.addText(f.level, { x: 2.5, y: y + 0.15, w: 0.8, h: 0.45, fontSize: 13, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei", align: "center" });
  slide5.addShape(pres.shapes.RECTANGLE, { x: 3.3, y, w: 6.4, h: 0.75, fill: { color: "FAFAFA" }, line: { color: "DDDDDD", width: 0.5 } });
  slide5.addText(f.detail, { x: 3.45, y: y + 0.15, w: 6.1, h: 0.5, fontSize: 12, color: "333333", fontFace: "Microsoft YaHei" });
});

// ─── Slide 6: Hach SWOT ───
let slide6 = pres.addSlide();
slide6.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.8, fill: { color: "0D2137" } });
slide6.addText("哈希IMS SWOT分析", { x: 0.3, y: 0.15, w: 9, h: 0.5, fontSize: 22, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei" });

const swot = [
  { q: "S 优势", color: "107C10", items: ["美国品牌，本地研发20年", "全场景监测覆盖（市政/工业/电子/膜）", "官方报道背书，高曝光", "多款新品家族亮相"] },
  { q: "W 劣势", color: "C62828", items: ["价格定位中高端", "软件平台能力弱于西门子/E+H", "E+H FieldEdge IIoT生态更完整"] },
  { q: "O 机会", color: "0078D4", items: ["AI+IoT成为核心引擎，IMS赛道扩张", "1,987家展商=潜在合作伙伴", "82,419专业观众=精准客户池"] },
  { q: "T 威胁", color: "FF8C00", items: ["云厂商平台向下切入（阿里/华为）", "E+H硬件+软件+云全栈布局", "替代品：便携/无人监测站"] },
];

swot.forEach((s, i) => {
  const x = (i % 2) * 4.7 + 0.3;
  const y = Math.floor(i / 2) * 2.3 + 1.0;
  slide6.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.4, h: 2.1, fill: { color: "FAFAFA" }, line: { color: s.color, width: 2 } });
  slide6.addText(s.q, { x: x + 0.1, y: y + 0.08, w: 4.2, h: 0.4, fontSize: 15, bold: true, color: s.color, fontFace: "Microsoft YaHei" });
  slide6.addText(s.items.map(item => ({ text: "• " + item, options: { breakLine: true } })), { x: x + 0.15, y: y + 0.5, w: 4.1, h: 1.5, fontSize: 11, color: "333333", fontFace: "Microsoft YaHei" });
});

// ─── Slide 7: 90天行动计划 ───
let slide7 = pres.addSlide();
slide7.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.8, fill: { color: "C62828" } });
slide7.addText("90天行动计划", { x: 0.3, y: 0.15, w: 9, h: 0.5, fontSize: 22, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei" });

const actions = [
  { phase: "前30天", color: "0078D4", items: ["整理展会名片/潜客名单，分类跟进", "对比E+H FieldEdge vs Hach D2020产品功能差距", "梳理展会上确认参展的仪表同行名单", "联系威立雅展会对接人"] },
  { phase: "31-60天", color: "107C10", items: ["拜访3-5家高意向潜客", "完成IMS软件平台竞品对比表", "与云厂商（阿里/华为）探索合作模式", "形成E1/E3馆展商热力图"] },
  { phase: "61-90天", color: "FF8C00", items: ["确定IMS产品线下半年差异化定位", "输出完整竞争分析报告v5", "规划2027年参展策略"] },
];

let yA = 1.0;
actions.forEach((a) => {
  slide7.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: yA, w: 1.4, h: 1.35, fill: { color: a.color } });
  slide7.addText(a.phase, { x: 0.3, y: yA + 0.4, w: 1.4, h: 0.5, fontSize: 14, bold: true, color: "FFFFFF", fontFace: "Microsoft YaHei", align: "center" });
  slide7.addShape(pres.shapes.RECTANGLE, { x: 1.7, y: yA, w: 8, h: 1.35, fill: { color: "FAFAFA" }, line: { color: "DDDDDD", width: 0.5 } });
  slide7.addText(a.items.map(item => ({ text: "• " + item, options: { breakLine: true } })), { x: 1.85, y: yA + 0.12, w: 7.7, h: 1.2, fontSize: 11.5, color: "333333", fontFace: "Microsoft YaHei" });
  yA += 1.45;
});

slide7.addText("关键原则：基于实际展商数据制定策略，不依赖未验证的预测名单", { x: 0.3, y: 5.35, w: 9.4, h: 0.25, fontSize: 11, bold: true, color: "C62828", fontFace: "Microsoft YaHei" });

// ─── Save ───
pres.writeFile({ fileName: "/home/agentuser/IMS竞争分析报告_v4_官方数据版.pptx" })
  .then(() => console.log("PPT V4 created successfully!"))
  .catch(err => console.error("Error:", err));
