const pptxgen = require("/home/agentuser/node_modules/pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "2026环博会竞品动态分析";
pres.author = "Hach中国IMS产品线";

// Color palette
const BLUE = "007EB5";
const DKGRAY = "4D4D4D";
const LTGRAY = "999999";
const WHITE = "FFFFFF";
const RED = "C0392B";
const ORANGE = "E67E22";
const YELLOW = "F39C12";
const GREEN = "27AE60";

function addSlideHeader(slide, num, title, subtitle) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.35, w: 0.55, h: 0.55,
    fill: { color: BLUE }, line: { color: BLUE }
  });
  slide.addText(num, {
    x: 0.4, y: 0.35, w: 0.55, h: 0.55,
    fontSize: 22, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide.addText(title, {
    x: 1.1, y: 0.35, w: 8.2, h: 0.55,
    fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, valign: "middle", margin: 0
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 1.1, y: 0.85, w: 8.2, h: 0.3,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: LTGRAY, valign: "top", margin: 0
    });
  }
}

function addFooter(slide, source) {
  slide.addText(source, {
    x: 0.4, y: 5.2, w: 9.2, h: 0.3,
    fontSize: 9, fontFace: "Microsoft YaHei",
    color: LTGRAY, valign: "bottom"
  });
}

// ============================================================
// SLIDE A: 硬件仪表竞品动态
// 矩阵: X轴=技术创新成熟度, Y轴=市场覆盖度
// ============================================================
let slideA = pres.addSlide();
addSlideHeader(slideA, "A", "硬件仪表竞品动态：有新品，有威胁，也有不动", "分析方法：技术创新成熟度 x 市场覆盖度象限分析 | 数据来源：展商样本 + 公开报道");
addFooter(slideA, "数据来源：展商样本；结论性质：★★★ 事实 / ★★ 有依据推断 / ★ 方向性判断");

// Matrix axis labels
slideA.addText("市场覆盖度 \u2192", {
  x: 0.5, y: 1.2, w: 4.5, h: 0.25,
  fontSize: 10, fontFace: "Microsoft YaHei",
  color: LTGRAY, align: "center"
});

slideA.addText("\u2191 技术创新成熟度", {
  x: 0.15, y: 2.5, w: 0.3, h: 1.5,
  fontSize: 10, fontFace: "Microsoft YaHei",
  color: LTGRAY, valign: "middle", rotate: 270
});

// Axis lines
slideA.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.45, w: 9.35, h: 0,
  line: { color: LTGRAY, width: 0.75 }
});
slideA.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.45, w: 0, h: 3.6,
  line: { color: LTGRAY, width: 0.75 }
});

// Quadrant dividers (dashed)
slideA.addShape(pres.shapes.LINE, {
  x: 5.2, y: 1.45, w: 0, h: 3.6,
  line: { color: "E0E0E0", width: 1, dashType: "dash" }
});
slideA.addShape(pres.shapes.LINE, {
  x: 0.5, y: 3.2, w: 9.35, h: 0,
  line: { color: "E0E0E0", width: 1, dashType: "dash" }
});

// Quadrant labels
const qLabels = [
  { x: 0.65, y: 1.55, text: "高成熟\n低覆盖", color: LTGRAY },
  { x: 5.35, y: 1.55, text: "高成熟\n高覆盖", color: GREEN },
  { x: 0.65, y: 3.3, text: "低成熟\n低覆盖", color: ORANGE },
  { x: 5.35, y: 3.3, text: "低成熟\n高覆盖", color: RED },
];
qLabels.forEach(q => {
  slideA.addText(q.text, {
    x: q.x, y: q.y, w: 1.0, h: 0.55,
    fontSize: 8, fontFace: "Microsoft YaHei",
    color: q.color, align: "center"
  });
});

// Competitor chips in quadrants
// Q1: High maturity, Low coverage (top-left) - "老牌守成"
const q1Items = [
  { name: "E+H / 梅特勒 / 横河", desc: "国际老牌，展会无大动作", badge: "静默", badgeColor: LTGRAY },
];
q1Items.forEach((item, i) => {
  const x = 1.0, y = 2.0;
  slideA.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 3.8, h: 0.95,
    fill: { color: WHITE }, line: { color: LTGRAY, width: 1 }
  });
  slideA.addText(item.name, {
    x: x + 0.12, y: y + 0.08, w: 3.5, h: 0.3,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slideA.addText(item.desc, {
    x: x + 0.12, y: y + 0.38, w: 2.6, h: 0.25,
    fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
  });
  slideA.addShape(pres.shapes.RECTANGLE, {
    x: x + 3.2, y: y + 0.35, w: 0.5, h: 0.25,
    fill: { color: item.badgeColor }
  });
  slideA.addText(item.badge, {
    x: x + 3.2, y: y + 0.35, w: 0.5, h: 0.25,
    fontSize: 8, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
});

// Q2: High maturity, High coverage (top-right) - "强势统治"
const q2Items = [
  { name: "聚光/谱育", desc: "双奖得主，实验室无人化+巡检机器人，平台化整套输出", badge: "领导者", badgeColor: GREEN },
  { name: "赛莱默(Xylem)", desc: "POM系统+臭氧新品，硬件AI融合，E1馆市政水务", badge: "领导者", badgeColor: GREEN },
];
q2Items.forEach((item, i) => {
  const x = 5.4, y = 1.85 + i * 1.05;
  slideA.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 4.4, h: 0.9,
    fill: { color: WHITE }, line: { color: GREEN, width: 1.5 }
  });
  slideA.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.06, h: 0.9,
    fill: { color: GREEN }
  });
  slideA.addText(item.name, {
    x: x + 0.15, y: y + 0.08, w: 3.2, h: 0.3,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slideA.addText(item.desc, {
    x: x + 0.15, y: y + 0.4, w: 4.1, h: 0.42,
    fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
  });
});

// Q3: Low maturity, Low coverage (bottom-left) - "新兴试探"
const q3Items = [
  { name: "格林凯瑞", desc: "水质预制试剂新品", badge: "新品", badgeColor: ORANGE },
  { name: "诺方", desc: "0.1\u03BCm颗粒计数器", badge: "新品", badgeColor: ORANGE },
];
q3Items.forEach((item, i) => {
  const x = 1.0 + i * 2.3, y = 3.85;
  slideA.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 2.1, h: 0.95,
    fill: { color: WHITE }, line: { color: ORANGE, width: 1 }
  });
  slideA.addText(item.name, {
    x: x + 0.1, y: y + 0.08, w: 1.9, h: 0.28,
    fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slideA.addText(item.desc, {
    x: x + 0.1, y: y + 0.38, w: 1.9, h: 0.25,
    fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
  });
  slideA.addShape(pres.shapes.RECTANGLE, {
    x: x + 0.1, y: y + 0.65, w: 0.45, h: 0.2,
    fill: { color: ORANGE }
  });
  slideA.addText(item.badge, {
    x: x + 0.1, y: y + 0.65, w: 0.45, h: 0.2,
    fontSize: 7, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
});

// Q4: Low maturity, High coverage (bottom-right) - "快速扩张"
const q4Items = [
  { name: "国产替代军团\n(雷磁/虹润/深昌鸿等)", desc: "价格低40-60%，满足国产优先政策，市政采购入围", badge: "替代威胁", badgeColor: RED },
  { name: "威立雅", desc: "人形机器人+AI降碳，综合服务AI化，E1馆", badge: "综合威胁", badgeColor: RED },
];
q4Items.forEach((item, i) => {
  const x = 5.4, y = 3.75 + i * 0.7;
  slideA.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 4.4, h: 0.6,
    fill: { color: WHITE }, line: { color: RED, width: 1 }
  });
  slideA.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.06, h: 0.6,
    fill: { color: RED }
  });
  slideA.addText(item.name, {
    x: x + 0.15, y: y + 0.04, w: 3.0, h: 0.3,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slideA.addText(item.desc, {
    x: x + 0.15, y: y + 0.32, w: 4.1, h: 0.22,
    fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
  });
});

// ============================================================
// SLIDE B: 软件/平台/AI服务竞品动态
// 分层: 极高/高/中威胁 + 机遇
// ============================================================
let slideB = pres.addSlide();
addSlideHeader(slideB, "B", "软件/平台/AI服务竞品动态：谁在重新定义竞争规则", "分析方法：威胁本质 x 可copy性分层 | 数据来源：展商样本 + 论坛内容");
addFooter(slideB, "数据来源：展商样本；论坛录音整理；可copy性：自研难度（高=难以复制，中=可以借鉴，低=容易被抄）");

// Threat level header bands
const threatBands = [
  {
    level: "\u26A0\u26A0\u26A0 极高威胁",
    color: RED,
    y: 1.3,
    h: 1.25,
    companies: [
      { name: "江苏纽带智能 (E3-G61)", product: "传感器+云平台+运维一体化", mechanism: "平台型：端到端智能监测，传感器是入口，云平台是底座，运维是粘性", copy: "极高", copyColor: LTGRAY, action: "优先评估其平台成熟度；探索硬件合作而非对抗" },
      { name: "首创环保 / 鸿泰华瑞", product: "ASMART模型+WEAM / 飛鸿AI系统", mechanism: "把运营经验/AI决策变平台，让仪器变数据源，算法成决策核心", copy: "高", copyColor: ORANGE, action: "加速 Hach 软件能力建设，从设备供应商转型监测服务伙伴" },
    ]
  },
  {
    level: "\u26A0\u26A0 高威胁",
    color: ORANGE,
    y: 2.65,
    h: 1.05,
    companies: [
      { name: "智易时代 (E3-D19/C20)", product: "AI巡检机器人+算法", mechanism: "AI算法切入巡检场景，机器人替代人工巡检，AI创新奖认证", copy: "高", copyColor: ORANGE, action: "关注AI算法与Hach硬件的结合可能性" },
      { name: "E20环境平台 (E1馆)", product: "数字化平台", mechanism: "平台型数字化公司，用平台能力绑定客户，重构采购决策链", copy: "高", copyColor: ORANGE, action: "纳入渠道合作伙伴评估体系" },
      { name: "昕彤智能", product: "剑企AI智能风机", mechanism: "硬件内嵌AI，曝气能耗降低30%，L4级水厂核心设备", copy: "中", copyColor: YELLOW, action: "AI风机是可借鉴方向；关注Hach设备AI化路径" },
    ]
  },
  {
    level: "\u26A0 中威胁（33家细分型）", color: YELLOW, y: 3.8, h: 0.85,
    companies: [
      { name: "尚云互联 / 易环智能 / 盘古自动化 等33家", product: "智慧环保平台/自动化控制+AI算法", mechanism: "垂直场景绑定特定客户群体，技术copy壁垒不高但客户关系深", copy: "中", copyColor: YELLOW, action: "防止在细分场景被渗透；关注行业Know-how积累" },
    ]
  }
];

threatBands.forEach((band, bi) => {
  // Band background
  slideB.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: band.y, w: 9.35, h: band.h,
    fill: { color: WHITE },
    line: { color: band.color, width: 1 }
  });

  // Level label (left strip)
  slideB.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: band.y, w: 0.08, h: band.h,
    fill: { color: band.color }
  });
  slideB.addText(band.level, {
    x: 0.65, y: band.y + 0.06, w: 1.5, h: 0.28,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: band.color
  });

  band.companies.forEach((comp, ci) => {
    const cx = 0.65 + ci * 4.6;
    const cw = 4.4;

    // Company name
    slideB.addText(comp.name, {
      x: cx, y: band.y + 0.08, w: cw, h: 0.28,
      fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
    });

    // Product
    slideB.addText("产品: " + comp.product, {
      x: cx, y: band.y + 0.36, w: cw, h: 0.22,
      fontSize: 9, fontFace: "Microsoft YaHei", color: BLUE
    });

    // Mechanism
    slideB.addText("\u27A4 " + comp.mechanism, {
      x: cx, y: band.y + 0.58, w: cw, h: 0.35,
      fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
    });

    // Copy badge + Action
    slideB.addShape(pres.shapes.RECTANGLE, {
      x: cx + cw - 0.55, y: band.y + 0.06, w: 0.5, h: 0.22,
      fill: { color: comp.copyColor }
    });
    slideB.addText("可copy:" + comp.copy, {
      x: cx + cw - 0.55, y: band.y + 0.06, w: 0.5, h: 0.22,
      fontSize: 7, fontFace: "Microsoft YaHei", bold: true,
      color: WHITE, align: "center", valign: "middle"
    });
  });
});

// Opportunity insight box at bottom
slideB.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.75, w: 9.35, h: 0.75,
  fill: { color: "E8F5E9" },
  line: { color: GREEN, width: 1 }
});
slideB.addText("\u{1F4A1} 机遇窗口：", {
  x: 0.65, y: 4.82, w: 1.3, h: 0.25,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: GREEN
});
slideB.addText("政府AI体系已成型（山水大模型+700亿知识库），监测数据进入AI分析链——数据合规性审核变严利好头部仪器厂商；水质报告AI生成参照土壤/地下水案例已落地，Hach应抢占先机。", {
  x: 0.65, y: 5.08, w: 9.05, h: 0.38,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});

// ============================================================
// SLIDE C: 竞品动态对标行动建议
// ============================================================
let slideC = pres.addSlide();
addSlideHeader(slideC, "C", "竞品对标与Hach行动建议", "分析方法：基于竞品动态矩阵 | 适合管理层/IMS产品线内部讨论");
addFooter(slideC, "结论性质：★★ 有依据的推断 | 适合作为IMS产品线战略讨论输入，不构成确定性建议");

// 2x2 grid: 竞品类型 vs Hach应对策略
const actionGrid = [
  {
    type: "硬件\u6587\u660E\u516C\u53F8\n(聚光/赛莱默/威立雅)",
    threat: "产品技术领先，平台化整套输出",
    hach: "加速软件能力内建，从卖设备转向卖监测服务",
    priority: "P0",
    color: RED
  },
  {
    type: "AI软件跨界\n(鸿泰华瑞/首创环保/纽带智能)",
    threat: "让仪器变数据源，算法成决策核心",
    hach: "硬件必须有软件接口，否则被管道化",
    priority: "P0",
    color: RED
  },
  {
    type: "国产替代军团\n(雷磁/虹润/深昌鸿)",
    threat: "价格低40-60%，国产优先政策受益",
    hach: "强化服务价值和长期总拥有成本优势",
    priority: "P1",
    color: ORANGE
  },
  {
    type: "AI创新新锐\n(智易时代/昕彤智能)",
    threat: "垂直场景AI落地，轻量化改造",
    hach: "评估合作或收购可能，填补AI能力短板",
    priority: "P1",
    color: ORANGE
  },
];

actionGrid.forEach((item, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const x = 0.5 + col * 4.7;
  const y = 1.3 + row * 2.1;

  // Card
  slideC.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 4.5, h: 1.95,
    fill: { color: WHITE },
    line: { color: item.color, width: 1.5 }
  });

  // Header band
  slideC.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 4.5, h: 0.45,
    fill: { color: item.color }
  });
  slideC.addText(item.type, {
    x, y, w: 3.7, h: 0.45,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, valign: "middle"
  });

  // Priority badge
  slideC.addShape(pres.shapes.RECTANGLE, {
    x: x + 3.85, y: y + 0.08, w: 0.55, h: 0.28,
    fill: { color: WHITE }
  });
  slideC.addText(item.priority, {
    x: x + 3.85, y: y + 0.08, w: 0.55, h: 0.28,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
    color: item.color, align: "center", valign: "middle"
  });

  // Threat
  slideC.addText("威胁本质:", {
    x: x + 0.12, y: y + 0.55, w: 1.0, h: 0.25,
    fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: LTGRAY
  });
  slideC.addText(item.threat, {
    x: x + 0.12, y: y + 0.78, w: 4.25, h: 0.38,
    fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
  });

  // Hach action
  slideC.addText("Hach应对:", {
    x: x + 0.12, y: y + 1.18, w: 1.0, h: 0.25,
    fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: BLUE
  });
  slideC.addText(item.hach, {
    x: x + 0.12, y: y + 1.4, w: 4.25, h: 0.45,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
});

// ============================================================
// SAVE
// ============================================================
pres.writeFile({ fileName: "/home/agentuser/竞品动态_v18.pptx" })
  .then(() => console.log("Done: /home/agentuser/竞品动态_v18.pptx"))
  .catch(e => console.error(e));
