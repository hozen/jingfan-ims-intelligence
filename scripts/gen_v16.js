const pptxgen = require("/home/agentuser/node_modules/pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "2026环博会市场观察报告";
pres.author = "Hach中国IMS产品线";

// Color palette (user spec: blue 0,126,181 / dark gray 77,77,77 / light gray 153,153,153)
const BLUE = "007EB5";
const DKGRAY = "4D4D4D";
const LTGRAY = "999999";
const WHITE = "FFFFFF";

// Helper: section number badge (FIXED: removed duplicate addText before shape)
function addSlideHeader(slide, num, title, subtitle) {
  // Shape first, then text on top
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.35, w: 0.55, h: 0.55,
    fill: { color: BLUE }, line: { color: BLUE }
  });
  slide.addText(num, {
    x: 0.4, y: 0.35, w: 0.55, h: 0.55,
    fontSize: 22, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  // Title
  slide.addText(title, {
    x: 1.1, y: 0.35, w: 7.5, h: 0.55,
    fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, valign: "middle", margin: 0
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 1.1, y: 0.85, w: 7.5, h: 0.3,
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

// ==================== SLIDE 1: Cover ====================
let slide1 = pres.addSlide();
slide1.background = { color: BLUE };

slide1.addText("2026环博会市场观察报告", {
  x: 0.5, y: 1.6, w: 9, h: 0.9,
  fontSize: 40, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center"
});

slide1.addText("水务环保行业从业者的实战参考资料", {
  x: 0.5, y: 2.5, w: 9, h: 0.5,
  fontSize: 18, fontFace: "Microsoft YaHei",
  color: WHITE, align: "center"
});

// Divider line
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 3.15, w: 3, h: 0.03,
  fill: { color: WHITE }
});

slide1.addText("产品趋势 · 技术趋势 · 客户需求 · 政策驱动", {
  x: 0.5, y: 3.3, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: WHITE, align: "center"
});

slide1.addText("2026年4月  |  上海新国际博览中心  |  第27届上海国际环博会", {
  x: 0.5, y: 3.85, w: 9, h: 0.35,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: WHITE, align: "center"
});

slide1.addText("数据来源：官方发布 + 展商样本交叉验证", {
  x: 0.5, y: 4.95, w: 9, h: 0.3,
  fontSize: 10, fontFace: "Microsoft YaHei",
  color: WHITE, align: "center"
});

// ==================== SLIDE 2: Official Stats ====================
let slide2 = pres.addSlide();
addSlideHeader(slide2, "01", "官方数据：1,987家展商告诉我们什么", "数据来源：官方发布 + 公众号样本交叉验证");
addFooter(slide2, "数据来源：第27届上海国际环博会官方发布（2026.04.15）；样本校验：微信公众号「城市中国」「环保开幕」OCR识别展商样本");

// 4 big stats
const stats = [
  { num: "1,987", label: "家参展企业", sub: "来自20个国家和地区", color: BLUE },
  { num: "82,419", label: "名专业观众", sub: "来自119个国家和地区", color: DKGRAY },
  { num: "17万", label: "平方米展示面积", sub: "15个展馆启用", color: DKGRAY },
  { num: "82,419", label: "国际观众增幅", sub: "连续两年超30%", color: LTGRAY },
];
stats.forEach((s, i) => {
  const x = 0.5 + i * 2.35;
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.4, w: 2.15, h: 1.7,
    fill: { color: WHITE },
    line: { color: i === 0 ? BLUE : LTGRAY, width: i === 0 ? 2 : 1 }
  });
  if (i === 0) {
    slide2.addShape(pres.shapes.RECTANGLE, {
      x: x, y: 1.4, w: 2.15, h: 0.06,
      fill: { color: BLUE }
    });
  }
  slide2.addText(s.num, {
    x: x, y: 1.55, w: 2.15, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei", bold: true,
    color: i === 0 ? BLUE : DKGRAY, align: "center", valign: "middle"
  });
  slide2.addText(s.label, {
    x: x, y: 2.2, w: 2.15, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, align: "center", valign: "middle"
  });
  slide2.addText(s.sub, {
    x: x, y: 2.6, w: 2.15, h: 0.35,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: LTGRAY, align: "center", valign: "top"
  });
});

// Key insights
slide2.addText("关键洞察", {
  x: 0.5, y: 3.35, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: DKGRAY
});
const insights = [
  { tag: "规模超预期", text: "实际1,987家 vs 预期近2,000家，基本符合；15馆启用 vs 上年略有收缩，说明行业整体规模趋稳" },
  { tag: "国际化加速", text: "119国观众 + 7国家展团 + 35个国际采购团，国际观众连续两年增幅超30%，出海是真实机会" },
  { tag: "智能化主线", text: "官方主题\"百国共襄 智能引领\"，AI+环保融合已成行业共识，非概念而是落地" },
];
insights.forEach((ins, i) => {
  const y = 3.8 + i * 0.45;
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 1.2, h: 0.32,
    fill: { color: BLUE }
  });
  slide2.addText(ins.tag, {
    x: 0.5, y: y, w: 1.2, h: 0.32,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide2.addText(ins.text, {
    x: 1.8, y: y, w: 7.7, h: 0.32,
    fontSize: 11, fontFace: "Microsoft YaHei",
    color: DKGRAY, valign: "middle"
  });
});

// ==================== SLIDE 3: Exhibition Hall Distribution ====================
let slide3 = pres.addSlide();
addSlideHeader(slide3, "02", "展馆分布：行业全景地图（官方版）", "数据来源：官方展馆数据 + 公众号样本交叉验证");
addFooter(slide3, "E4/E6/E5/E2/E1数据来源：官方发布；E3馆约200家展商，官方未公开完整数据，展位号来自展商整理（微信搜索2026环博会展商名单公众号文章）");

// 6 halls in 2 rows x 3 cols - ALL use same card format
const halls = [
  { hall: "E4馆", count: "182家", theme: "过程控制/仪器仪表", insight: "仪器仪表最集中，同行竞争最激烈" },
  { hall: "E6馆", count: "187家", theme: "大气治理/余热回收", insight: "规模最大，细分领域覆盖最广" },
  { hall: "E5馆", count: "174家", theme: "大气治理/VOCs", insight: "VOC治理、无组织排放管控热点" },
  { hall: "E2馆", count: "120家", theme: "综合环境解决方案", insight: "工程/运营/咨询类展商最多" },
  { hall: "E1馆", count: "93家", theme: "水处理/膜材料/泵阀", insight: "膜材料国产化、价格下探明显" },
  { hall: "E3馆", count: "~200家", theme: "监测与检测", insight: "水质监测企业最集中；官方未公开完整数据，本列表来自展商自己整理" },
];

halls.forEach((h, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.5 + col * 3.1;
  const y = 1.35 + row * 1.55;

  slide3.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 2.9, h: 1.35,
    fill: { color: WHITE },
    line: { color: i === 5 ? LTGRAY : (i === 0 ? BLUE : LTGRAY), width: i === 0 ? 1.5 : 0.75 }
  });

  // Hall name badge
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 0.7, h: 0.35,
    fill: { color: i === 5 ? LTGRAY : BLUE }
  });
  slide3.addText(h.hall, {
    x: x, y: y, w: 0.7, h: 0.35,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });

  slide3.addText(h.count, {
    x: x + 0.8, y: y + 0.05, w: 2, h: 0.35,
    fontSize: h.count.length > 5 ? 12 : 18,
    fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, valign: "middle"
  });

  slide3.addText(h.theme, {
    x: x + 0.1, y: y + 0.45, w: 2.7, h: 0.3,
    fontSize: 11, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY
  });

  slide3.addText(h.insight, {
    x: x + 0.1, y: y + 0.78, w: 2.7, h: 0.5,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: LTGRAY
  });
});

// ==================== SLIDE 4: Porter's Five Forces ====================
let slide4 = pres.addSlide();
addSlideHeader(slide4, "03", "波特五力分析：行业竞争格局", "数据来源：基于展馆分布数据推断 + 公开政策文件");
addFooter(slide4, "结论性质：★★★ = 有数据支撑的推断；★★ = 行业共识推断；★ = 方向性判断");

const forces = [
  { title: "行业内现有竞争", score: "高", color: "C0392B", detail: "E4馆182家仪器仪表扎堆；价格战已从设备蔓延到耗材（膜价格低40-60%）；纯硬件模式越来越难", evidence: "★★★ 展商分布数据" },
  { title: "新进入者威胁", score: "中高", color: "E67E22", detail: "39家数字化公司跨界切入（云平台+数据+IoT）；软件能力强的跨界者正在重新定义竞争规则", evidence: "★★★ 展商分类数据" },
  { title: "上游议价能力", score: "中", color: "F39C12", detail: "传感器/芯片国产化提升，但高端传感器仍依赖进口；传感器价格下探有助于降低仪表成本", evidence: "★★ 行业趋势推断" },
  { title: "下游议价能力", score: "高", color: "C0392B", detail: "水务集团/市政采购：政府招标、国产优先、性价比要求高；买方高度集中且信息化程度提升", evidence: "★★★ 政策导向+采购模式" },
  { title: "替代品威胁", score: "中", color: "7F8C8D", detail: "在线监测替代传统实验室抽样（趋势明确）；但高端检测仍需实验室，替代速度中等", evidence: "★★ 技术趋势推断" },
];

forces.forEach((f, i) => {
  const y = 1.3 + i * 0.8;

  // Score badge
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 0.6, h: 0.6,
    fill: { color: f.color }
  });
  slide4.addText(f.score, {
    x: 0.5, y: y, w: 0.6, h: 0.6,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });

  // Title
  slide4.addText(f.title, {
    x: 1.25, y: y, w: 2.3, h: 0.6,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, valign: "middle", margin: 0
  });

  // Detail
  slide4.addText(f.detail, {
    x: 3.6, y: y, w: 5.2, h: 0.6,
    fontSize: 11, fontFace: "Microsoft YaHei",
    color: DKGRAY, valign: "middle"
  });

  // Evidence tag
  slide4.addText(f.evidence, {
    x: 8.85, y: y, w: 1.0, h: 0.6,
    fontSize: 8, fontFace: "Microsoft YaHei",
    color: LTGRAY, valign: "middle", align: "right"
  });

  if (i < forces.length - 1) {
    slide4.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: y + 0.65, w: 9.35, h: 0.01,
      fill: { color: "E8E8E8" }
    });
  }
});

// ==================== SLIDE 5: Value Chain ====================
let slide5 = pres.addSlide();
addSlideHeader(slide5, "04", "行业价值链：从研发到服务的利润迁移", "数据来源：基于展商样本类型分布推断");
addFooter(slide5, "结论性质：★★★ = 有展商数据支撑；★★ = 行业共识推断；★ = 方向性判断");

const vcSteps = [
  { step: "01", name: "核心零部件", desc: "传感器/芯片/膜材料", players: "传感器国产替代中\n高端仍依赖进口", margin: "高", color: BLUE },
  { step: "02", name: "仪器仪表制造", desc: "水质/气体分析仪", players: "E4馆182家扎堆\n价格战激烈", margin: "中低", color: DKGRAY },
  { step: "03", name: "系统集成", desc: "IoT方案/边缘计算", players: "39家数字化公司\n跨界进入", margin: "中高", color: DKGRAY },
  { step: "04", name: "软件平台", desc: "SaaS云平台/AI分析", players: "70%数字化展商\n提供云服务", margin: "高", color: BLUE },
  { step: "05", name: "运维服务", desc: "校准/运维/运营", players: "卖设备→卖服务\n已成普遍现实", margin: "高且稳定", color: BLUE },
];

vcSteps.forEach((v, i) => {
  const x = 0.5 + i * 1.88;

  // Box
  slide5.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.35, w: 1.7, h: 2.5,
    fill: { color: WHITE },
    line: { color: v.color, width: 1.5 }
  });

  // Step number
  slide5.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.35, w: 1.7, h: 0.45,
    fill: { color: v.color }
  });
  slide5.addText(v.step, {
    x: x, y: 1.35, w: 1.7, h: 0.45,
    fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });

  // Name
  slide5.addText(v.name, {
    x: x + 0.08, y: 1.9, w: 1.54, h: 0.45,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, align: "center", valign: "middle"
  });

  // Desc
  slide5.addText(v.desc, {
    x: x + 0.08, y: 2.35, w: 1.54, h: 0.4,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: LTGRAY, align: "center", valign: "middle"
  });

  // Players
  slide5.addText(v.players, {
    x: x + 0.08, y: 2.75, w: 1.54, h: 0.7,
    fontSize: 9, fontFace: "Microsoft YaHei",
    color: DKGRAY, align: "center", valign: "top"
  });

  // Margin badge
  slide5.addShape(pres.shapes.RECTANGLE, {
    x: x + 0.25, y: 3.5, w: 1.2, h: 0.28,
    fill: { color: v.color }
  });
  slide5.addText("利润: " + v.margin, {
    x: x + 0.25, y: 3.5, w: 1.2, h: 0.28,
    fontSize: 9, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });

  // Arrow
  if (i < vcSteps.length - 1) {
    slide5.addText("▶", {
      x: x + 1.7, y: 2.2, w: 0.18, h: 0.5,
      fontSize: 14, color: LTGRAY, align: "center", valign: "middle"
    });
  }
});

// Key insight
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.05, w: 9.35, h: 0.9,
  fill: { color: "F5F8FA" }
});
slide5.addText("价值链洞察：", {
  x: 0.65, y: 4.15, w: 1.2, h: 0.3,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true,
  color: BLUE
});
slide5.addText("利润正从仪器仪表制造向软件平台和运维服务迁移。纯硬件销售利润空间持续收窄，\"设备+云+服务\"一体化模式是抵御价格战的关键路径。", {
  x: 0.65, y: 4.45, w: 9.05, h: 0.4,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: DKGRAY
});

// ==================== SLIDE 6: 3C Analysis ====================
let slide6 = pres.addSlide();
addSlideHeader(slide6, "05", "3C战略分析：Hach的机会与挑战", "数据来源：展商数据 + 公开新闻");
addFooter(slide6, "结论性质：★★★ = 事实；★★ = 有依据的推断；★ = 方向性判断");

const c3 = [
  {
    title: "Company\n我们",
    color: BLUE,
    items: [
      { t: "市场地位", d: "荣膺2026 IE环博奖年度领军企业（官方认证）★★★", ev: "★★★" },
      { t: "核心优势", d: "20年本土研发积累 + Veralto集团平台 + 水质监测全品类", ev: "★★★" },
      { t: "战略挑战", d: "纯硬件模式承压；数字化/AI能力需加速补齐；服务占比偏低", ev: "★★" },
      { t: "参展动作", d: "E3-C12展位 + 研发20周年庆典 + 七大行业解决方案", ev: "★★★" },
    ]
  },
  {
    title: "Competitors\n竞争对手",
    color: DKGRAY,
    items: [
      { t: "国内创新者", d: "智易时代：AI算法+巡检机器人★AI创新奖；聚光/谱育：环博奖双料★年度领军+出海先锋；格林凯瑞：水质预制试剂新品；诺方：0.1μm颗粒计数器", ev: "★★★" },
      { t: "平台型跨界者", d: "江苏纽带智能(E3-G61)：传感器+云平台+运维一体化；淳业科技(E3-C98)：水质监测全系列", ev: "★★★" },
      { t: "国产替代者", d: "雷磁(E3-D22，86年积累)、深昌鸿(E75)、虹润：价格低40-60%，满足国产优先政策", ev: "★★" },
      { t: "国际品牌", d: "E+H、西门子、横河等：官方目录未见；实际参展情况待现场确认", ev: "★" },
    ]
  },
  {
    title: "Customers\n客户",
    color: LTGRAY,
    items: [
      { t: "市政水务集团", d: "买设备→买平台→买服务；国产优先；单项目500万+", ev: "★★" },
      { t: "工业园区", d: "满足监管→降本增效→数据资产化；国产替代机会大", ev: "★★" },
      { t: "政府监管", d: "一张网+精准溯源；等保合规；区域型项目1000万+", ev: "★★" },
      { t: "采购决策变化", d: "不只是采购价，是3-5年运维+校准+升级总拥有成本", ev: "★★" },
    ]
  },
];

c3.forEach((col, i) => {
  const x = 0.5 + i * 3.1;

  // Header
  slide6.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.3, w: 2.9, h: 0.55,
    fill: { color: col.color }
  });
  slide6.addText(col.title, {
    x: x, y: 1.3, w: 2.9, h: 0.55,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });

  // Items
  col.items.forEach((item, j) => {
    const y = 1.95 + j * 0.78;

    slide6.addShape(pres.shapes.RECTANGLE, {
      x: x, y: y, w: 2.9, h: 0.7,
      fill: { color: WHITE },
      line: { color: "E8E8E8", width: 0.5 }
    });

    slide6.addText(item.t, {
      x: x + 0.1, y: y + 0.05, w: 2.7, h: 0.25,
      fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
      color: DKGRAY
    });

    slide6.addText(item.d, {
      x: x + 0.1, y: y + 0.28, w: 2.5, h: 0.4,
      fontSize: 9, fontFace: "Microsoft YaHei",
      color: LTGRAY
    });
  });
});

// ==================== SLIDE 7: PESTEL ====================
let slide7 = pres.addSlide();
addSlideHeader(slide7, "06", "PESTEL政策分析：2026年最值得关注的政策方向", "数据来源：公开政策文件 + 政府工作报告");
addFooter(slide7, "数据来源：十五五规划纲要（2026年启动）；全国两会政府工作报告2026；生态环境部公开文件；碳市场扩容政策");

const pestel = [
  { letter: "P", name: "政治/Policy", color: BLUE, items: [
    { t: "十五五规划开局", d: "美丽中国建设部署，县镇级监测能力建设带来增量市场，黑臭水体治理持续，监测点位加密" },
    { t: "政府招标国产优先", d: "国产化率要求提升，外资品牌进入采购名单门槛提高" },
  ]},
  { letter: "E", name: "经济/Economic", color: DKGRAY, items: [
    { t: "双碳目标推进", d: "碳市场扩容提速，钢铁/化工/水泥/航空等高排放行业分批纳入，碳监测成新增量赛道" },
    { t: "水务集团降本增效", d: "地方财政压力下，水务集团降本需求强烈，价格敏感度提升" },
  ]},
  { letter: "S", name: "社会/Social", color: LTGRAY, items: [
    { t: "公众环保意识提升", d: "环境数据公开需求增加，舆情监督倒逼企业监测升级" },
    { t: "监测从业人员结构变化", d: "数字化技能需求增加，传统运维人员面临转型压力" },
  ]},
  { letter: "T", name: "技术/Technological", color: BLUE, items: [
    { t: "AI+IoT加速融合", d: "数字孪生、预测性维护、异常预警技术成熟度提升，从概念走向落地" },
    { t: "5G模组成本下降", d: "5G+工业互联网预计2027年进入爆发期" },
  ]},
  { letter: "E", name: "环境/Environmental", color: DKGRAY, items: [
    { t: "水环境精细化管理", d: "流域监测、断面监测加密，饮用水源监测需求增加" },
    { t: "大气治理持续高压", d: "VOC无组织排放管控趋严，监测密度要求提升" },
  ]},
  { letter: "L", name: "法律/Legal", color: LTGRAY, items: [
    { t: "等保2.0+数据安全法", d: "数据联网合规要求筛掉大批中小平台厂商，利好头部" },
    { t: "碳核查法制化", d: "碳排放数据真实性要求提高，第三方监测市场扩容" },
  ]},
];

pestel.forEach((p, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.5 + col * 3.1;
  const y = 1.3 + row * 2.05;

  slide7.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 2.9, h: 1.9,
    fill: { color: WHITE },
    line: { color: p.color, width: 1 }
  });

  // Letter badge
  slide7.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 0.45, h: 0.45,
    fill: { color: p.color }
  });
  slide7.addText(p.letter, {
    x: x, y: y, w: 0.45, h: 0.45,
    fontSize: 20, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide7.addText(p.name, {
    x: x + 0.5, y: y + 0.05, w: 2.3, h: 0.35,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, valign: "middle"
  });

  p.items.forEach((item, j) => {
    const iy = y + 0.5 + j * 0.68;
    slide7.addText(item.t, {
      x: x + 0.1, y: iy, w: 2.7, h: 0.25,
      fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
      color: DKGRAY
    });
    slide7.addText(item.d, {
      x: x + 0.1, y: iy + 0.23, w: 2.7, h: 0.4,
      fontSize: 9, fontFace: "Microsoft YaHei",
      color: LTGRAY
    });
  });
});

// ==================== SLIDE 8: Technology Trends ====================
let slide8 = pres.addSlide();
addSlideHeader(slide8, "07", "技术趋势TOP5：这次展会上什么最火", "数据来源：展商样本分析 + 官方展会主题");
addFooter(slide8, "数据来源：公众号展商目录样本分析；推断结论标注置信度");

const techTrends = [
  { num: "①", title: "在线监测设备爆发", conf: "★★★", detail: "E4馆182家展商中超40%展示在线监测产品，24/7实时监测替代传统实验室抽样已成明确趋势。云+端一体化是活下去的基本要求。" },
  { num: "②", title: "传感器小型化与IoT化", conf: "★★", detail: "多款小型化水质传感器，光谱分析仪亮相，支持自适应采集、边缘预处理、分布式部署。农业面源污染、河道监测等新场景涌现。" },
  { num: "③", title: "AI与大数据分析落地", conf: "★★", detail: "预测性维护、异常预警、排放趋势预测是主要AI落地场景。异常检测>趋势预测>溯源分析，技术成熟度依次递减。" },
  { num: "④", title: "数字孪生从概念走向落地", conf: "★★", detail: "多个展台展示三维水厂、智慧水务大屏，但落地成本高，目前主要集中在大型水务集团和工业园区。" },
  { num: "⑤", title: "5G+工业互联网", conf: "★", detail: "5G网关、5G+监测方案首次大规模亮相，低延时特性支撑实时控制和远程运维。预计2027年进入爆发期。" },
];

techTrends.forEach((t, i) => {
  const y = 1.3 + i * 0.78;

  slide8.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9.35, h: 0.7,
    fill: { color: i % 2 === 0 ? WHITE : "F8F9FA" },
    line: { color: "E8E8E8", width: 0.5 }
  });

  slide8.addText(t.num, {
    x: 0.6, y: y, w: 0.35, h: 0.7,
    fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
    color: BLUE, valign: "middle"
  });

  slide8.addText(t.title, {
    x: 1.05, y: y + 0.05, w: 2.5, h: 0.35,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY
  });

  // FIXED: shape FIRST, then text on top (no more overlap)
  const confColor = t.conf === "★★★" ? BLUE : t.conf === "★★" ? DKGRAY : LTGRAY;
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: 1.05, y: y + 0.38, w: 0.4, h: 0.28,
    fill: { color: confColor }
  });
  slide8.addText(t.conf, {
    x: 1.05, y: y + 0.38, w: 0.4, h: 0.28,
    fontSize: 9, fontFace: "Microsoft YaHei",
    color: WHITE, align: "center", valign: "middle"
  });

  slide8.addText(t.detail, {
    x: 3.6, y: y + 0.05, w: 6.1, h: 0.6,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: DKGRAY, valign: "middle"
  });
});

// ==================== SLIDE 9: AI Forum Key Takeaways ====================
let slide9 = pres.addSlide();
addSlideHeader(slide9, "08", "AI分论坛核心结论：政府AI体系已成型，监测数据进入AI分析链", "数据来源：2026中国环境技术大会AI×环保论坛（4月13-14日，环博会同期）");
addFooter(slide9, "数据来源：2026中国环境技术大会AI×环保论坛（4月13-14日，上海）；腾讯元宝会议纪要（ID: ada69a26-45e4-4b8c-b92c-29e204aceeb4）");

// AI action plan summary
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.3, w: 4.4, h: 1.55,
  fill: { color: "F0F5F9" },
  line: { color: BLUE, width: 1 }
});
slide9.addText("生态环境部AI行动方案（核心政策信号）", {
  x: 0.6, y: 1.38, w: 4.2, h: 0.3,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: BLUE
});
const aiPlan = [
  "• 成立AI工作专班，2026年38个应用场景落地",
  "• \"山水大模型\"统一入口：接入DeepSeek、讯飞等",
  "• 700亿资源量环境知识库已建成",
  "• 环评报告：30分钟生成 + 10分钟审批（全流程AI）",
  "• 地下水污染报告智能生成：100+份规则模板",
];
slide9.addText(aiPlan.join("\n"), {
  x: 0.6, y: 1.68, w: 4.2, h: 1.1,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});

// Groundwater AI monitoring
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 5.1, y: 1.3, w: 4.75, h: 1.55,
  fill: { color: "F0F5F9" },
  line: { color: DKGRAY, width: 1 }
});
slide9.addText("地下水AI监管实测数据（来自论坛案例）", {
  x: 5.2, y: 1.38, w: 4.55, h: 0.3,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
const gwData = [
  { metric: "人工采样占比", value: "99%（当前）" },
  { metric: "AI视频审核效率提升", value: "4.1倍" },
  { metric: "采样合规率", value: "98.9%" },
  { metric: "后台专家人力减少", value: "73%" },
  { metric: "单份报告处理时间", value: "5分钟" },
];
gwData.forEach((d, i) => {
  slide9.addText(d.metric + "：", {
    x: 5.2, y: 1.68 + i * 0.22, w: 2.3, h: 0.22,
    fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
  });
  slide9.addText(d.value, {
    x: 7.5, y: 1.68 + i * 0.22, w: 2.2, h: 0.22,
    fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
});

// Three AI application scenarios
slide9.addText("三大已落地AI应用场景（论坛实测案例）", {
  x: 0.5, y: 3.0, w: 9, h: 0.3,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});

const aiScenarios = [
  { n: "①", title: "污染源数据异常智能诊断", tech: "4个AI专家智能体协同：数据预处理/诊断分析/结果解读/可视化", result: "6类异常自动识别（数据缺失、高值突增、低值骤降等）", color: BLUE },
  { n: "②", title: "湖库/河道AI智能识别", tech: "多模态：无人机航拍+固定摄像头+卫星遥感；YOLOv8+大模型", result: "某市河道违规行为识别准确率90%+；自动告警", color: DKGRAY },
  { n: "③", title: "污染溯源报告一键生成", tech: "环境知识库+全域溯源知识图谱+大模型", result: "自动生成：事件概况+溯源分析+处置建议", color: LTGRAY },
];

aiScenarios.forEach((s, i) => {
  const x = 0.5 + i * 3.1;
  slide9.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 3.35, w: 2.9, h: 1.35,
    fill: { color: WHITE },
    line: { color: s.color, width: 1.5 }
  });
  slide9.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 3.35, w: 2.9, h: 0.38,
    fill: { color: s.color }
  });
  slide9.addText(s.n + " " + s.title, {
    x: x, y: 3.35, w: 2.9, h: 0.38,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: WHITE, align: "center", valign: "middle"
  });
  slide9.addText(s.tech + "\n\n" + s.result, {
    x: x + 0.08, y: 3.78, w: 2.74, h: 0.88,
    fontSize: 8.5, fontFace: "Microsoft YaHei", color: DKGRAY
  });
});

// Hach implications
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.82, w: 9.35, h: 0.72,
  fill: { color: "FFF8E1" },
  line: { color: "E67E22", width: 1 }
});
slide9.addText("⚠️ 对Hach的直接影响：", {
  x: 0.6, y: 4.88, w: 2.2, h: 0.25,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: "E67E22"
});
slide9.addText("① 环评AI审批落地（30分钟生成）→ 客户报告生成门槛降低，但数据合规性审核变严\n② 监测数据直接进AI分析链 → 数据质量要求系统性提升，仪器精度是基础前提\n③ 报告自动生成已在土壤/地下水/环评落地 → 水质报告AI生成场景参照性强，机会窗口已开\n④ 地下水采样AI监管（视频+LLM审核）→ 采样规范性合规要求 → 硬件端需留有合规证据接口", {
  x: 0.6, y: 5.1, w: 9.15, h: 0.42,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});

// ==================== SLIDE 10: Customer Needs ====================
let slide10 = pres.addSlide();
addSlideHeader(slide10, "09", "客户需求变化：谁在买、买什么、为什么变", "数据来源：展商反馈 + 政策文件 + 行业调研");
addFooter(slide10, "数据来源：展商交流推断 + 政府招标文件分析 + 行业报告交叉验证");

const customers = [
  { type: "市政/水务集团", scale: "大型项目\n500万+", need: "从买设备→买平台→买服务", pain: "厂网河湖一体化监测、智慧水务大屏、数据联网", decision: "政府招标\n国产优先", color: BLUE },
  { type: "工业园区/企业", scale: "中型项目\n50-300万", need: "满足监管→降本增效→数据资产化", pain: "在线监测系统、碳核查、排放数据上报", decision: "企业自采\n价格敏感", color: DKGRAY },
  { type: "政府/监管机构", scale: "区域型项目\n1000万+", need: "从单点监测→一张网→精准溯源", pain: "污染源自动监控一张网、预警应急、污染溯源", decision: "政府专项债\n等保合规", color: LTGRAY },
];

customers.forEach((c, i) => {
  const x = 0.5 + i * 3.1;

  slide10.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.3, w: 2.9, h: 0.55,
    fill: { color: c.color }
  });
  slide10.addText(c.type, {
    x: x, y: 1.3, w: 2.9, h: 0.55,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });

  const rows = [
    { label: "采购规模", value: c.scale },
    { label: "需求变化", value: c.need },
    { label: "典型需求", value: c.pain },
    { label: "采购决策", value: c.decision },
  ];
  rows.forEach((r, j) => {
    const y = 1.95 + j * 0.6;
    slide10.addShape(pres.shapes.RECTANGLE, {
      x: x, y: y, w: 2.9, h: 0.55,
      fill: { color: WHITE },
      line: { color: "E8E8E8", width: 0.5 }
    });
    slide10.addText(r.label, {
      x: x + 0.1, y: y + 0.02, w: 2.7, h: 0.22,
      fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: LTGRAY
    });
    slide10.addText(r.value, {
      x: x + 0.1, y: y + 0.22, w: 2.7, h: 0.3,
      fontSize: 10, fontFace: "Microsoft YaHei",
      color: DKGRAY
    });
  });
});

// 4C insight
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.4, w: 9.35, h: 0.85,
  fill: { color: "F0F5F9" }
});
slide10.addText("4C视角：客户真正在买什么？", {
  x: 0.65, y: 4.48, w: 9, h: 0.28,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true,
  color: BLUE
});
slide10.addText("Customer Value（监测能力带来的决策支持） | Cost（3-5年总拥有成本） | Convenience（安装便捷、跨系统数据打通） | Communication（响应快、本地化支持）", {
  x: 0.65, y: 4.76, w: 9, h: 0.4,
  fontSize: 10, fontFace: "Microsoft YaHei",
  color: DKGRAY
});

// ==================== SLIDE 11: Competitive Landscape ====================
let slide11 = pres.addSlide();
addSlideHeader(slide11, "10", "竞争格局：39家数字化跨界公司值得重点关注", "数据来源：公众号展商目录筛选，同时包含云/平台/数据/智能/数字关键词的展商");
addFooter(slide11, "数据来源：微信公众号「城市中国」「环保开幕」展商目录，人工筛选数字化相关展商共39家");

const threats = [
  { level: "极高威胁", companies: "江苏纽带智能(E3-G61)\nE20环境平台(E1-C71)", desc: "平台型：端到端智能监测，传感器+云平台+运维一体化", color: "C0392B" },
  { level: "高威胁", companies: "尚云互联、易环智能\n盘古自动化、智易时代", desc: "垂直型：智慧环保平台、自动化控制+AI算法；智易时代已获AI巡检机器人创新奖", color: "E67E22" },
  { level: "中威胁", companies: "云景信息、崟盾智能\n缘循智能 等33家", desc: "细分型：智慧水务平台、流体控制智能化等垂直场景，绑定特定客户群体", color: "F39C12" },
];

slide11.addText("数字化跨界公司威胁分级", {
  x: 0.5, y: 1.3, w: 9, h: 0.35,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
  color: DKGRAY
});

threats.forEach((t, i) => {
  const x = 0.5 + i * 3.1;

  slide11.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.7, w: 2.9, h: 2.55,
    fill: { color: WHITE },
    line: { color: t.color, width: 2 }
  });

  slide11.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.7, w: 2.9, h: 0.42,
    fill: { color: t.color }
  });
  slide11.addText(t.level, {
    x: x, y: 1.7, w: 2.9, h: 0.42,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });

  slide11.addText(t.companies, {
    x: x + 0.1, y: 2.2, w: 2.7, h: 0.65,
    fontSize: 11, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY
  });

  slide11.addText(t.desc, {
    x: x + 0.1, y: 2.85, w: 2.7, h: 1.3,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: LTGRAY
  });
});

// Hach strategic position
slide11.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.4, w: 9.35, h: 0.85,
  fill: { color: "F0F5F9" }
});
slide11.addText("Hach战略定位建议：", {
  x: 0.65, y: 4.48, w: 2, h: 0.28,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true,
  color: BLUE
});
slide11.addText("这39家公司可能重塑行业格局——平台型公司是最大不确定性。建议：①优先评估其云平台成熟度和客户覆盖度；②加速软件能力建设，从\"设备供应商\"转型\"监测服务伙伴\"；③与平台型公司探索合作而非对抗（数据接口+硬件互补）。", {
  x: 0.65, y: 4.76, w: 9.05, h: 0.45,
  fontSize: 10, fontFace: "Microsoft YaHei",
  color: DKGRAY
});

// ==================== SLIDE 12: Industry Consensus ====================
let slide12 = pres.addSlide();
addSlideHeader(slide12, "11", "2026环博会：5大行业共识", "数据来源：展商行为分析 + 政策解读 + 行业交流");
addFooter(slide12, "数据来源：基于展馆数据、展商展示内容、官方主题的综合推断；适合朋友圈分享");

const consensus = [
  { n: "1", title: "产品：监测设备向实时化、智能化演进", fact: "E4馆182家仪器仪表展商中超40%展示在线监测产品，IoT版本已成标配",共鸣: "纯卖硬件越来越难，云+端一体化是活下去的基本要求" },
  { n: "2", title: "技术：云+AI是技术主线，但落地节奏差异大", fact: "39家数字化展商中70%提供云服务，AI异常检测是主要落地场景",共鸣: "大水务在数字孪生，小水厂还在搞定标——技术代差在拉大" },
  { n: "3", title: "客户：买服务不买设备已成普遍现实", fact: "展商普遍推出年度运维服务合同，政府招标将服务能力纳入评分",共鸣: "一次性采购的饼越来越小，维保服务的钱越来越重要" },
  { n: "4", title: "政策：十五五+双碳构成双重引擎", fact: "美丽中国建设+碳市场扩容，政策文件可直接引用，市场测算有据可查",共鸣: "政策红利还在，但竞争者也在增多，能不能吃到看能力和资源" },
  { n: "5", title: "格局：跨界打劫正在发生，但还未颠覆", fact: "39家数字化跨界公司以平台+数据能力切入，但硬件根基不稳",共鸣: "传统仪表厂商不要慌，但必须加速软件能力建设，否则会被跨进来" },
];

consensus.forEach((c, i) => {
  const y = 1.3 + i * 0.82;

  slide12.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9.35, h: 0.75,
    fill: { color: i % 2 === 0 ? WHITE : "F8F9FA" }
  });

  // Number
  slide12.addShape(pres.shapes.OVAL, {
    x: 0.6, y: y + 0.12, w: 0.5, h: 0.5,
    fill: { color: BLUE }
  });
  slide12.addText(c.n, {
    x: 0.6, y: y + 0.12, w: 0.5, h: 0.5,
    fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });

  slide12.addText(c.title, {
    x: 1.25, y: y + 0.05, w: 4.2, h: 0.35,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY
  });
  slide12.addText(c.fact, {
    x: 1.25, y: y + 0.38, w: 4.2, h: 0.33,
    fontSize: 9, fontFace: "Microsoft YaHei",
    color: LTGRAY
  });

  slide12.addShape(pres.shapes.RECTANGLE, {
    x: 5.6, y: y + 0.08, w: 0.03, h: 0.6,
    fill: { color: "E0E0E0" }
  });

  slide12.addText("💡 " + c.共鸣, {
    x: 5.75, y: y + 0.1, w: 3.95, h: 0.55,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: DKGRAY, valign: "middle"
  });
});

// ==================== SLIDE 13: Appendix ====================
let slide13 = pres.addSlide();
addSlideHeader(slide13, "附录", "数据来源与说明");
addFooter(slide13, "数据截至2026年4月15日展会闭幕；结论仅供参考，不构成投资建议");

const sources = [
  { cat: "官方数据", items: [
    "第27届上海国际环博会官方发布（2026.04.15）：1,987家展商、82,419名观众、17万平米、15馆",
    "官方展会主题：百国共襄 智能引领",
    "下一届：第28届上海环博会 2027年4月20-22日"
  ]},
  { cat: "展商数据", items: [
    "主数据源：微信公众号「城市中国」「环保开幕」展商目录，OCR识别E1/E2/E4/E5/E6馆展商样本",
    "E3馆：约200家，来自展商整理（微信搜索2026环博会展商名单公众号文章），展位号完整",
    "数字化公司：同时包含云/平台/数据/智能/数字关键词，共计39家"
  ]},
  { cat: "政策数据", items: [
    "十五五规划纲要（2026年启动）——美丽中国建设部署",
    "全国两会政府工作报告2026",
    "生态环境部公开文件"
  ]},
  { cat: "E3馆部分重点展商", items: [
    "哈希(E3-C12★年度领军)、聚光/谱育(★双奖年度领军+出海先锋)、智易时代(E3-D19/C20★机器人奖)",
    "格林凯瑞(E3-B42)、诺方(E3-B79)、深昌鸿(E3-E75)、淳业(E3-C98)、雷磁(E3-D22)、迪特西(E3-C39)",
    "沃德精准(E3-E3L-20)、莱特莱德(E3-A38)、虹润、皖仪(★成长先锋)、源易测、国林科技、纽带智能(E3-G61)",
    "★=2026 IE环博奖得主；E3馆约200家，完整名录来自展商整理"
  ]},
  { cat: "论坛数据", items: [
    "2026中国环境技术大会AI×环保论坛（4月13-14日，上海），腾讯元宝会议纪要",
    "演讲嘉宾：生态环境部技术专家、赵总（水环境AI）、陈荣研究员（AI驱动环境监管数字化）、高松教授（VOC与大气AI感知）"
  ]},
];

sources.forEach((s, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.5 + col * 3.1;
  const y = 1.3 + row * 1.9;

  slide13.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 2.9, h: 1.75,
    fill: { color: WHITE },
    line: { color: LTGRAY, width: 0.5 }
  });

  slide13.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 2.9, h: 0.38,
    fill: { color: BLUE }
  });
  slide13.addText(s.cat, {
    x: x, y: y, w: 2.9, h: 0.38,
    fontSize: 11, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });

  s.items.forEach((item, j) => {
    slide13.addText("• " + item, {
      x: x + 0.1, y: y + 0.45 + j * 0.38, w: 2.7, h: 0.36,
      fontSize: 8.5, fontFace: "Microsoft YaHei",
      color: DKGRAY
    });
  });
});

// ==================== SAVE ====================
pres.writeFile({ fileName: "/home/agentuser/环博会市场观察_v16.pptx" })
  .then(() => console.log("Done: /home/agentuser/环博会市场观察_v16.pptx"))
  .catch(e => console.error(e));
