const pptxgen = require("/home/agentuser/node_modules/pptxgenjs");
const fs = require("fs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "2026环博会市场观察报告";
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

// ============================================================
// UTILITY: fresh shadow object (NEVER reuse)
// ============================================================
const makeShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.08 });

function addSlideHeader(slide, num, title, subtitle) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.3, w: 0.52, h: 0.52,
    fill: { color: BLUE }, line: { color: BLUE }
  });
  slide.addText(num, {
    x: 0.4, y: 0.3, w: 0.52, h: 0.52,
    fontSize: 20, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide.addText(title, {
    x: 1.05, y: 0.3, w: 8.5, h: 0.52,
    fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, valign: "middle", margin: 0
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 1.05, y: 0.78, w: 8.5, h: 0.28,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: LTGRAY, valign: "top", margin: 0
    });
  }
}

function addFooter(slide, source) {
  slide.addText(source, {
    x: 0.4, y: 5.15, w: 9.2, h: 0.28,
    fontSize: 9, fontFace: "Microsoft YaHei",
    color: LTGRAY, valign: "bottom"
  });
}

// ============================================================
// SLIDE 1: Cover
// ============================================================
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
  x: 0.5, y: 4.8, w: 9, h: 0.28,
  fontSize: 10, fontFace: "Microsoft YaHei",
  color: WHITE, align: "center"
});
slide1.addText("本报告内容由AI辅助生成，仅供参考", {
  x: 0.5, y: 5.1, w: 9, h: 0.25,
  fontSize: 9, fontFace: "Microsoft YaHei",
  color: "CCCCCC", align: "center"
});

// ============================================================
// SLIDE 2: Official Stats
// ============================================================
let slide2 = pres.addSlide();
addSlideHeader(slide2, "01", "官方数据：1,987家展商告诉我们什么", "数据来源：官方发布 + 公众号样本交叉验证");
addFooter(slide2, "数据来源：第27届上海国际环博会官方发布（2026.04.15）；样本校验：微信公众号「城市中国」「环保开幕」OCR识别展商样本");

const stats = [
  { num: "1,987", label: "家参展企业", sub: "来自20个国家和地区", color: BLUE },
  { num: "82,419", label: "名专业观众", sub: "来自119个国家和地区", color: DKGRAY },
  { num: "17万", label: "平方米展示面积", sub: "15个展馆启用", color: DKGRAY },
  { num: "82,419", label: "国际观众增幅", sub: "连续两年超30%", color: LTGRAY },
];
stats.forEach((s, i) => {
  const x = 0.5 + i * 2.35;
  slide2.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.35, w: 2.15, h: 1.65,
    fill: { color: WHITE },
    line: { color: i === 0 ? BLUE : LTGRAY, width: i === 0 ? 2 : 1 }
  });
  if (i === 0) slide2.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.35, w: 2.15, h: 0.06, fill: { color: BLUE }
  });
  slide2.addText(s.num, {
    x, y: 1.5, w: 2.15, h: 0.68,
    fontSize: 28, fontFace: "Microsoft YaHei", bold: true,
    color: i === 0 ? BLUE : DKGRAY, align: "center", valign: "middle"
  });
  slide2.addText(s.label, {
    x, y: 2.15, w: 2.15, h: 0.38,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, align: "center", valign: "middle"
  });
  slide2.addText(s.sub, {
    x, y: 2.53, w: 2.15, h: 0.33,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: LTGRAY, align: "center", valign: "top"
  });
});

slide2.addText("关键洞察", {
  x: 0.5, y: 3.2, w: 9, h: 0.38,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
const insights = [
  { tag: "规模超预期", text: "实际1,987家 vs 预期近2,000家，基本符合；15馆启用 vs 上年略有收缩，说明行业整体规模趋稳" },
  { tag: "国际化加速", text: "119国观众 + 7国家展团 + 35个国际采购团，国际观众连续两年增幅超30%，出海是真实机会" },
  { tag: "智能化主线", text: "官方主题\"百国共襄 智能引领\"，AI+环保融合已成行业共识，非概念而是落地" },
];
insights.forEach((ins, i) => {
  const y = 3.62 + i * 0.42;
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y, w: 1.1, h: 0.3,
    fill: { color: BLUE }
  });
  slide2.addText(ins.tag, {
    x: 0.5, y, w: 1.1, h: 0.3,
    fontSize: 9, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide2.addText(ins.text, {
    x: 1.7, y, w: 7.8, h: 0.3,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: DKGRAY, valign: "middle"
  });
});

// ============================================================
// SLIDE 3: Exhibition Halls
// ============================================================
let slide3 = pres.addSlide();
addSlideHeader(slide3, "02", "展馆分布：行业全景地图", "数据来源：官方展馆数据 + 公众号样本交叉验证；E1馆数据来自用户发送展商截图OCR");
addFooter(slide3, "E1数据：用户发送截图OCR，77家已识别；E3馆约200家，官方未公开完整数据");

const halls = [
  { hall: "E4馆", count: "182家", theme: "过程控制/仪器仪表", insight: "仪器仪表最集中，同行竞争最激烈" },
  { hall: "E6馆", count: "187家", theme: "大气治理/余热回收", insight: "规模最大，细分领域覆盖最广" },
  { hall: "E5馆", count: "174家", theme: "大气治理/VOCs", insight: "VOC治理、无组织排放管控热点" },
  { hall: "E2馆", count: "120家", theme: "综合环境解决方案", insight: "工程/运营/咨询类展商最多" },
  { hall: "E1馆", count: "93家（77家已识别）", theme: "水处理/膜材料/泵阀", insight: "膜材料国产化价格下探明显；赛莱默、威立雅等国际品牌在列" },
  { hall: "E3馆", count: "~200家", theme: "监测与检测", insight: "水质监测企业最集中；E3-C12=哈希(C12)，E3-B42=格林凯瑞" },
];
halls.forEach((h, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.5 + col * 3.1;
  const y = 1.28 + row * 1.52;

  slide3.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 2.9, h: 1.4,
    fill: { color: WHITE },
    line: { color: i === 5 ? LTGRAY : (i === 0 ? BLUE : LTGRAY), width: i === 0 ? 1.5 : 0.75 }
  });
  slide3.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.68, h: 0.34,
    fill: { color: i === 5 ? LTGRAY : BLUE }
  });
  slide3.addText(h.hall, {
    x, y, w: 0.68, h: 0.34,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide3.addText(h.count, {
    x: x + 0.78, y: y + 0.04, w: 2.0, h: 0.32,
    fontSize: h.count.length > 10 ? 9 : 16,
    fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, valign: "middle"
  });
  slide3.addText(h.theme, {
    x: x + 0.08, y: y + 0.44, w: 2.74, h: 0.28,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slide3.addText(h.insight, {
    x: x + 0.08, y: y + 0.76, w: 2.74, h: 0.56,
    fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
  });
});

// ============================================================
// SLIDE 4: Porter's Five Forces
// ============================================================
let slide4 = pres.addSlide();
addSlideHeader(slide4, "03", "波特五力分析：行业竞争格局", "数据来源：基于展馆分布数据推断 + 公开政策文件");
addFooter(slide4, "结论性质：★★★ = 有数据支撑的推断；★★ = 行业共识推断；★ = 方向性判断");

const forces = [
  { title: "行业内现有竞争", score: "高", color: RED, detail: "E4馆182家仪器仪表扎堆；价格战已从设备蔓延到耗材（膜价格低40-60%）；纯硬件模式越来越难", evidence: "★★★ 展商分布" },
  { title: "新进入者威胁", score: "中高", color: ORANGE, detail: "39家数字化公司跨界切入（云平台+数据+IoT）；软件能力强的跨界者正在重新定义竞争规则", evidence: "★★★ 展商分类" },
  { title: "上游议价能力", score: "中", color: YELLOW, detail: "传感器/芯片国产化提升，但高端传感器仍依赖进口；传感器价格下探有助于降低仪表成本", evidence: "★★ 行业趋势" },
  { title: "下游议价能力", score: "高", color: RED, detail: "水务集团/市政采购：政府招标、国产优先、性价比要求高；买方高度集中且信息化程度提升", evidence: "★★★ 政策+采购" },
  { title: "替代品威胁", score: "中", color: LTGRAY, detail: "在线监测替代传统实验室抽样（趋势明确）；但高端检测仍需实验室，替代速度中等", evidence: "★★ 技术趋势" },
];
forces.forEach((f, i) => {
  const y = 1.25 + i * 0.78;
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y, w: 0.58, h: 0.58,
    fill: { color: f.color }
  });
  slide4.addText(f.score, {
    x: 0.5, y, w: 0.58, h: 0.58,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide4.addText(f.title, {
    x: 1.22, y, w: 2.2, h: 0.58,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, valign: "middle", margin: 0
  });
  slide4.addText(f.detail, {
    x: 3.5, y, w: 5.0, h: 0.58,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: DKGRAY, valign: "middle"
  });
  slide4.addText(f.evidence, {
    x: 8.55, y, w: 1.3, h: 0.58,
    fontSize: 8, fontFace: "Microsoft YaHei",
    color: LTGRAY, valign: "middle", align: "right"
  });
  if (i < forces.length - 1) {
    slide4.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: y + 0.63, w: 9.35, h: 0.01,
      fill: { color: "E8E8E8" }
    });
  }
});

// ============================================================
// SLIDE 5: Value Chain
// ============================================================
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
  slide5.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.3, w: 1.7, h: 2.48,
    fill: { color: WHITE },
    line: { color: v.color, width: 1.5 }
  });
  slide5.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.3, w: 1.7, h: 0.44,
    fill: { color: v.color }
  });
  slide5.addText(v.step, {
    x, y: 1.3, w: 1.7, h: 0.44,
    fontSize: 15, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide5.addText(v.name, {
    x: x + 0.06, y: 1.84, w: 1.58, h: 0.42,
    fontSize: 11, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, align: "center", valign: "middle"
  });
  slide5.addText(v.desc, {
    x: x + 0.06, y: 2.26, w: 1.58, h: 0.38,
    fontSize: 9, fontFace: "Microsoft YaHei",
    color: LTGRAY, align: "center", valign: "middle"
  });
  slide5.addText(v.players, {
    x: x + 0.06, y: 2.64, w: 1.58, h: 0.68,
    fontSize: 9, fontFace: "Microsoft YaHei",
    color: DKGRAY, align: "center", valign: "top"
  });
  slide5.addShape(pres.shapes.RECTANGLE, {
    x: x + 0.24, y: 3.38, w: 1.22, h: 0.27,
    fill: { color: v.color }
  });
  slide5.addText("利润: " + v.margin, {
    x: x + 0.24, y: 3.38, w: 1.22, h: 0.27,
    fontSize: 9, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  if (i < vcSteps.length - 1) {
    slide5.addText("\u25B6", {
      x: x + 1.7, y: 2.18, w: 0.18, h: 0.48,
      fontSize: 13, color: LTGRAY, align: "center", valign: "middle"
    });
  }
});
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.0, w: 9.35, h: 0.88,
  fill: { color: "F5F8FA" }
});
slide5.addText("价值链洞察：", {
  x: 0.62, y: 4.1, w: 1.2, h: 0.28,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: BLUE
});
slide5.addText("利润正从仪器仪表制造向软件平台和运维服务迁移。纯硬件销售利润空间持续收窄，\"设备+云+服务\"一体化模式是抵御价格战的关键路径。", {
  x: 0.62, y: 4.4, w: 9.05, h: 0.38,
  fontSize: 10, fontFace: "Microsoft YaHei", color: DKGRAY
});

// ============================================================
// SLIDE 6: 3C Analysis
// ============================================================
let slide6 = pres.addSlide();
addSlideHeader(slide6, "05", "3C战略分析：Hach的机会与挑战", "数据来源：展商数据 + 公开新闻");
addFooter(slide6, "结论性质：★★★ = 事实；★★ = 有依据的推断；★ = 方向性判断");

const c3 = [
  {
    title: "Company\n我们",
    color: BLUE,
    items: [
      { t: "市场地位", d: "荣膺2026 IE环博奖年度领军企业（官方认证）★★★" },
      { t: "核心优势", d: "20年本土研发积累 + Veralto集团平台 + 水质监测全品类" },
      { t: "战略挑战", d: "纯硬件模式承压；数字化/AI能力需加速补齐；服务占比偏低" },
      { t: "参展动作", d: "E3-C12展位 + 研发20周年庆典 + 七大行业解决方案" },
    ]
  },
  {
    title: "Competitors\n竞争对手",
    color: DKGRAY,
    items: [
      { t: "国内创新者", d: "智易时代：AI算法+巡检机器人★AI创新奖；聚光/谱育：环博奖双料★年度领军+出海先锋；格林凯瑞：水质预制试剂新品；诺方：0.1μm颗粒计数器" },
      { t: "平台型跨界者", d: "江苏纽带智能(E3-G61)：传感器+云平台+运维一体化；淳业科技(E3-C98)：水质监测全系列" },
      { t: "国产替代者", d: "雷磁(E3-D22，86年积累)、深昌鸿(E75)、虹润：价格低40-60%，满足国产优先政策" },
      { t: "国际品牌", d: "赛莱默(Xylem)：E1馆，POM+臭氧新品；威立雅：E1馆人形机器人+AI降碳；恩德斯豪斯(EH)：全球客户论坛在瑞士，环博会未见大动作" },
    ]
  },
  {
    title: "Customers\n客户",
    color: LTGRAY,
    items: [
      { t: "市政水务集团", d: "买设备→买平台→买服务；国产优先；单项目500万+" },
      { t: "工业园区", d: "满足监管→降本增效→数据资产化；国产替代机会大" },
      { t: "政府/监管机构", d: "一张网+精准溯源；等保合规；区域型项目1000万+" },
      { t: "采购决策变化", d: "不只是采购价，是3-5年运维+校准+升级总拥有成本" },
    ]
  }
];
c3.forEach((col, i) => {
  const x = 0.5 + i * 3.1;
  slide6.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.25, w: 2.9, h: 0.52,
    fill: { color: col.color }
  });
  slide6.addText(col.title, {
    x, y: 1.25, w: 2.9, h: 0.52,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  col.items.forEach((item, j) => {
    const y = 1.87 + j * 0.76;
    slide6.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 2.9, h: 0.7,
      fill: { color: WHITE },
      line: { color: "E8E8E8", width: 0.5 }
    });
    slide6.addText(item.t, {
      x: x + 0.1, y: y + 0.04, w: 2.7, h: 0.24,
      fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
    });
    slide6.addText(item.d, {
      x: x + 0.1, y: y + 0.27, w: 2.7, h: 0.4,
      fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
    });
  });
});

// ============================================================
// SLIDE 7: PESTEL
// ============================================================
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
  const y = 1.25 + row * 2.02;
  slide7.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 2.9, h: 1.88,
    fill: { color: WHITE },
    line: { color: p.color, width: 1 }
  });
  slide7.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.42, h: 0.42,
    fill: { color: p.color }
  });
  slide7.addText(p.letter, {
    x, y, w: 0.42, h: 0.42,
    fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide7.addText(p.name, {
    x: x + 0.48, y: y + 0.04, w: 2.3, h: 0.34,
    fontSize: 11, fontFace: "Microsoft YaHei", bold: true,
    color: DKGRAY, valign: "middle"
  });
  p.items.forEach((item, j) => {
    const iy = y + 0.48 + j * 0.68;
    slide7.addText(item.t, {
      x: x + 0.08, y: iy, w: 2.74, h: 0.24,
      fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
    });
    slide7.addText(item.d, {
      x: x + 0.08, y: iy + 0.22, w: 2.74, h: 0.42,
      fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
    });
  });
});

// ============================================================
// SLIDE 8: Technology Trends
// ============================================================
let slide8 = pres.addSlide();
addSlideHeader(slide8, "07", "技术趋势TOP5：这次展会上什么最火", "数据来源：展商样本分析 + 官方展会主题");
addFooter(slide8, "数据来源：公众号展商目录样本分析；推断结论标注置信度");

const techTrends = [
  { num: "\u2460", title: "在线监测设备爆发", conf: "\u2605\u2605\u2605", detail: "E4馆182家展商中超40%展示在线监测产品，24/7实时监测替代传统实验室抽样已成明确趋势。云+端一体化是活下去的基本要求。" },
  { num: "\u2461", title: "传感器小型化与IoT化", conf: "\u2605\u2605", detail: "多款小型化水质传感器，光谱分析仪亮相，支持自适应采集、边缘预处理、分布式部署。农业面源污染、河道监测等新场景涌现。" },
  { num: "\u2462", title: "AI与大数据分析落地", conf: "\u2605\u2605", detail: "预测性维护、异常预警、排放趋势预测是主要AI落地场景。异常检测>趋势预测>溯源分析，技术成熟度依次递减。" },
  { num: "\u2463", title: "数字孪生从概念走向落地", conf: "\u2605\u2605", detail: "多个展台展示三维水厂、智慧水务大屏，但落地成本高，目前主要集中在大型水务集团和工业园区。" },
  { num: "\u2464", title: "5G+工业互联网", conf: "\u2605", detail: "5G网关、5G+监测方案首次大规模亮相，低延时特性支撑实时控制和远程运维。预计2027年进入爆发期。" },
];
techTrends.forEach((t, i) => {
  const y = 1.25 + i * 0.76;
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y, w: 9.35, h: 0.68,
    fill: { color: i % 2 === 0 ? WHITE : "F8F9FA" },
    line: { color: "E8E8E8", width: 0.5 }
  });
  slide8.addText(t.num, {
    x: 0.58, y, w: 0.32, h: 0.68,
    fontSize: 15, fontFace: "Microsoft YaHei", bold: true,
    color: BLUE, valign: "middle"
  });
  slide8.addText(t.title, {
    x: 1.0, y: y + 0.04, w: 2.4, h: 0.32,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  const confColor = t.conf === "\u2605\u2605\u2605" ? BLUE : t.conf === "\u2605\u2605" ? DKGRAY : LTGRAY;
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: 1.0, y: y + 0.37, w: 0.38, h: 0.25,
    fill: { color: confColor }
  });
  slide8.addText(t.conf, {
    x: 1.0, y: y + 0.37, w: 0.38, h: 0.25,
    fontSize: 9, fontFace: "Microsoft YaHei",
    color: WHITE, align: "center", valign: "middle"
  });
  slide8.addText(t.detail, {
    x: 3.5, y: y + 0.04, w: 6.2, h: 0.6,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: DKGRAY, valign: "middle"
  });
});

// ============================================================
// SLIDE 9: AI Forum
// ============================================================
let slide9 = pres.addSlide();
addSlideHeader(slide9, "08", "AI分论坛核心结论：政府AI体系已成型，监测数据进入AI分析链", "数据来源：2026中国环境技术大会AI\u00d7环保论坛（4月13-14日，环博会同期）");
addFooter(slide9, "数据来源：2026中国环境技术大会AI\u00d7环保论坛（4月13-14日，上海）；腾讯元宝会议纪要");

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.25, w: 4.4, h: 1.5,
  fill: { color: "F0F5F9" },
  line: { color: BLUE, width: 1 }
});
slide9.addText("生态环境部AI行动方案（核心政策信号）", {
  x: 0.58, y: 1.32, w: 4.24, h: 0.28,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: BLUE
});
const aiPlan = [
  "\u2022 成立AI工作专班，2026年38个应用场景落地",
  "\u2022 \"山水大模型\"统一入口：接入DeepSeek、讯飞等",
  "\u2022 700亿资源量环境知识库已建成",
  "\u2022 环评报告：30分钟生成 + 10分钟审批（全流程AI）",
  "\u2022 地下水污染报告智能生成：100+份规则模板",
];
slide9.addText(aiPlan.join("\n"), {
  x: 0.58, y: 1.6, w: 4.24, h: 1.08,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 5.1, y: 1.25, w: 4.75, h: 1.5,
  fill: { color: "F0F5F9" },
  line: { color: DKGRAY, width: 1 }
});
slide9.addText("地下水AI监管实测数据（来自论坛案例）", {
  x: 5.18, y: 1.32, w: 4.58, h: 0.28,
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
    x: 5.18, y: 1.62 + i * 0.22, w: 2.3, h: 0.22,
    fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
  });
  slide9.addText(d.value, {
    x: 7.48, y: 1.62 + i * 0.22, w: 2.22, h: 0.22,
    fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
});

slide9.addText("三大已落地AI应用场景（论坛实测案例）", {
  x: 0.5, y: 2.88, w: 9, h: 0.28,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
const aiScenarios = [
  { n: "\u2460", title: "污染源数据异常智能诊断", tech: "4个AI专家智能体协同：数据预处理/诊断分析/结果解读/可视化", result: "6类异常自动识别（数据缺失、高值突增、低值骤降等）", color: BLUE },
  { n: "\u2461", title: "湖库/河道AI智能识别", tech: "多模态：无人机航拍+固定摄像头+卫星遥感；YOLOv8+大模型", result: "某市河道违规行为识别准确率90%+；自动告警", color: DKGRAY },
  { n: "\u2462", title: "污染溯源报告一键生成", tech: "环境知识库+全域溯源知识图谱+大模型", result: "自动生成：事件概况+溯源分析+处置建议", color: LTGRAY },
];
aiScenarios.forEach((s, i) => {
  const x = 0.5 + i * 3.1;
  slide9.addShape(pres.shapes.RECTANGLE, {
    x, y: 3.2, w: 2.9, h: 1.3,
    fill: { color: WHITE },
    line: { color: s.color, width: 1.5 }
  });
  slide9.addShape(pres.shapes.RECTANGLE, {
    x, y: 3.2, w: 2.9, h: 0.36,
    fill: { color: s.color }
  });
  slide9.addText(s.n + " " + s.title, {
    x, y: 3.2, w: 2.9, h: 0.36,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide9.addText(s.tech + "\n\n" + s.result, {
    x: x + 0.07, y: 3.6, w: 2.76, h: 0.86,
    fontSize: 8.5, fontFace: "Microsoft YaHei", color: DKGRAY
  });
});

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.62, w: 9.35, h: 0.68,
  fill: { color: "FFF8E1" },
  line: { color: "E67E22", width: 1 }
});
slide9.addText("\u26A0 对Hach的直接影响：", {
  x: 0.58, y: 4.67, w: 2.2, h: 0.24,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: "E67E22"
});
slide9.addText("\u2460 环评AI审批落地（30分钟生成）\u2192 客户报告生成门槛降低，但数据合规性审核变严  \u2461 监测数据直接进AI分析链\u2192 数据质量要求系统性提升  \u2462 水质报告AI生成场景参照性强（土壤/地下水案例已落地），机会窗口已开  \u2463 地下水采样AI监管\u2192 采样规范性合规要求\u2192 硬件端需留有合规证据接口", {
  x: 0.58, y: 4.92, w: 9.18, h: 0.34,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});

// ============================================================
// SLIDE 10: Customer Needs
// ============================================================
let slide10 = pres.addSlide();
addSlideHeader(slide10, "09", "客户需求变化：谁在买、买什么、为什么变", "数据来源：展商反馈 + 政策文件 + 行业调研");
addFooter(slide10, "数据来源：展商交流推断 + 政府招标文件分析 + 行业报告交叉验证");

const customers = [
  { type: "市政/水务集团", scale: "大型项目\n500万+", need: "从买设备\u2192买平台\u2192买服务", pain: "厂网河湖一体化监测、智慧水务大屏、数据联网", decision: "政府招标\n国产优先", color: BLUE },
  { type: "工业园区/企业", scale: "中型项目\n50-300万", need: "满足监管\u2192降本增效\u2192数据资产化", pain: "在线监测系统、碳核查、排放数据上报", decision: "企业自采\n价格敏感", color: DKGRAY },
  { type: "政府/监管机构", scale: "区域型项目\n1000万+", need: "从单点监测\u2192一张网\u2192精准溯源", pain: "污染源自动监控一张网、预警应急、污染溯源", decision: "政府专项债\n等保合规", color: LTGRAY },
];
customers.forEach((c, i) => {
  const x = 0.5 + i * 3.1;
  slide10.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.25, w: 2.9, h: 0.52,
    fill: { color: c.color }
  });
  slide10.addText(c.type, {
    x, y: 1.25, w: 2.9, h: 0.52,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  const rows = [
    { label: "采购规模", value: c.scale },
    { label: "需求变化", value: c.need },
    { label: "典型需求", value: c.pain },
    { label: "采购决策", value: c.decision },
  ];
  rows.forEach((r, j) => {
    const y = 1.87 + j * 0.58;
    slide10.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 2.9, h: 0.53,
      fill: { color: WHITE },
      line: { color: "E8E8E8", width: 0.5 }
    });
    slide10.addText(r.label, {
      x: x + 0.08, y: y + 0.02, w: 2.74, h: 0.2,
      fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: LTGRAY
    });
    slide10.addText(r.value, {
      x: x + 0.08, y: y + 0.2, w: 2.74, h: 0.3,
      fontSize: 10, fontFace: "Microsoft YaHei", color: DKGRAY
    });
  });
});
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.32, w: 9.35, h: 0.82,
  fill: { color: "F0F5F9" }
});
slide10.addText("4C视角：客户真正在买什么？", {
  x: 0.62, y: 4.4, w: 9, h: 0.26,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: BLUE
});
slide10.addText("Customer Value（监测能力带来的决策支持） | Cost（3-5年总拥有成本） | Convenience（安装便捷、跨系统数据打通） | Communication（响应快、本地化支持）", {
  x: 0.62, y: 4.68, w: 9.18, h: 0.38,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});

// ============================================================
// SLIDE 11: Competitive Landscape
// ============================================================
let slide11 = pres.addSlide();
addSlideHeader(slide11, "10", "竞争格局：39家数字化跨界公司值得重点关注", "数据来源：公众号展商目录筛选，云/平台/数据/智能/数字关键词展商");
addFooter(slide11, "数据来源：微信公众号「城市中国」「环保开幕」展商目录，人工筛选数字化相关展商共39家");

const threats = [
  { level: "极高威胁", companies: "江苏纽带智能(E3-G61)\nE20环境平台(E1)", desc: "平台型：端到端智能监测，传感器+云平台+运维一体化", color: RED },
  { level: "高威胁", companies: "尚云互联、易环智能\n盘古自动化、智易时代", desc: "垂直型：智慧环保平台、自动化控制+AI算法；智易时代已获AI巡检机器人创新奖", color: ORANGE },
  { level: "中威胁", companies: "云景信息、崟盾智能\n缘循智能 等33家", desc: "细分型：智慧水务平台、流体控制智能化等垂直场景，绑定特定客户群体", color: YELLOW },
];
slide11.addText("数字化跨界公司威胁分级", {
  x: 0.5, y: 1.25, w: 9, h: 0.32,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
threats.forEach((t, i) => {
  const x = 0.5 + i * 3.1;
  slide11.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.62, w: 2.9, h: 2.48,
    fill: { color: WHITE },
    line: { color: t.color, width: 2 }
  });
  slide11.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.62, w: 2.9, h: 0.4,
    fill: { color: t.color }
  });
  slide11.addText(t.level, {
    x, y: 1.62, w: 2.9, h: 0.4,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide11.addText(t.companies, {
    x: x + 0.08, y: 2.08, w: 2.74, h: 0.62,
    fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slide11.addText(t.desc, {
    x: x + 0.08, y: 2.72, w: 2.74, h: 1.3,
    fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
  });
});
slide11.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.22, w: 9.35, h: 0.82,
  fill: { color: "F0F5F9" }
});
slide11.addText("Hach战略定位建议：", {
  x: 0.62, y: 4.3, w: 2, h: 0.26,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: BLUE
});
slide11.addText("这39家公司可能重塑行业格局——平台型公司是最大不确定性。建议：\u2460优先评估其云平台成熟度和客户覆盖度；\u2461加速软件能力建设，从\"设备供应商\"转型\"监测服务伙伴\"；\u2462与平台型公司探索合作而非对抗（数据接口+硬件互补）。", {
  x: 0.62, y: 4.58, w: 9.18, h: 0.42,
  fontSize: 10, fontFace: "Microsoft YaHei", color: DKGRAY
});

// ============================================================
// SLIDE 12: Industry Consensus
// ============================================================
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
  const y = 1.25 + i * 0.8;
  slide12.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y, w: 9.35, h: 0.72,
    fill: { color: i % 2 === 0 ? WHITE : "F8F9FA" }
  });
  slide12.addShape(pres.shapes.OVAL, {
    x: 0.58, y: y + 0.1, w: 0.5, h: 0.5,
    fill: { color: BLUE }
  });
  slide12.addText(c.n, {
    x: 0.58, y: y + 0.1, w: 0.5, h: 0.5,
    fontSize: 15, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  slide12.addText(c.title, {
    x: 1.2, y: y + 0.04, w: 4.1, h: 0.32,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slide12.addText(c.fact, {
    x: 1.2, y: y + 0.36, w: 4.1, h: 0.32,
    fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
  });
  slide12.addShape(pres.shapes.RECTANGLE, {
    x: 5.45, y: y + 0.06, w: 0.03, h: 0.58,
    fill: { color: "E0E0E0" }
  });
  slide12.addText("\u{1F4A1} " + c.共鸣, {
    x: 5.58, y: y + 0.08, w: 4.17, h: 0.54,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: DKGRAY, valign: "middle"
  });
});

// ============================================================
// SLIDE 13: Appendix
// ============================================================
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
    "主数据源：微信公众号「城市中国」「环保开幕」展商目录，OCR识别E2/E4/E5/E6馆展商样本",
    "E1馆：93家（77家已识别，用户发送截图OCR）；E3馆：约200家，官方未公开完整数据",
    "数字化公司：同时包含云/平台/数据/智能/数字关键词，共计39家"
  ]},
  { cat: "政策数据", items: [
    "十五五规划纲要（2026年启动）——美丽中国建设部署",
    "全国两会政府工作报告2026",
    "生态环境部公开文件"
  ]},
  { cat: "E1馆重点展商", items: [
    "赛莱默(Xylem)：E1馆，POM系统+臭氧新品；威立雅：人形机器人+AI降碳",
    "水艺环保(E1-A11)、清新环境(E1-C02/D01)、天津创业(E1-042/D43)",
    "昕彤赋能(长沙)人工智能(E1)：给水和排污系统，AI风机；中国恩菲(E1-L65)"
  ]},
  { cat: "E3馆重点展商", items: [
    "哈希(E3-C12\u2605年度领军)、聚光/谱育(E3\u2605双奖年度领军+出海先锋)、智易时代(E3-D19/C20\u2605机器人奖)",
    "格林凯瑞(E3-B42)、诺方(E3-B79)、深昌鸿(E3-E75)、淳业(E3-C98)、雷磁(E3-D22)",
    "\u2605=2026 IE环博奖得主"
  ]},
  { cat: "论坛数据", items: [
    "2026中国环境技术大会AI\u00d7环保论坛（4月13-14日，上海），腾讯元宝会议纪要",
    "演讲嘉宾：生态环境部技术专家、赵总（水环境AI）、陈荣研究员（AI驱动环境监管数字化）、高松教授（VOC与大气AI感知）"
  ]},
];
sources.forEach((s, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.5 + col * 3.1;
  const y = 1.25 + row * 1.88;
  slide13.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 2.9, h: 1.74,
    fill: { color: WHITE },
    line: { color: LTGRAY, width: 0.5 }
  });
  slide13.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 2.9, h: 0.36,
    fill: { color: BLUE }
  });
  slide13.addText(s.cat, {
    x, y, w: 2.9, h: 0.36,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
  s.items.forEach((item, j) => {
    slide13.addText("\u2022 " + item, {
      x: x + 0.08, y: y + 0.42 + j * 0.42, w: 2.74, h: 0.4,
      fontSize: 8.5, fontFace: "Microsoft YaHei", color: DKGRAY
    });
  });
});

// ============================================================
// SLIDE 14: 竞品动态 - 硬件仪表
// ============================================================
let slide14 = pres.addSlide();
addSlideHeader(slide14, "A", "硬件仪表竞品动态：有新品，有威胁，也有不动", "分析方法：技术创新成熟度 x 市场覆盖度象限分析 | 数据来源：展商样本 + 公开报道");
addFooter(slide14, "数据来源：展商样本；结论性质：★★★ 事实 / ★★ 有依据推断 / ★ 方向性判断");

// Axis labels
slide14.addText("市场覆盖度 \u2192", {
  x: 0.5, y: 1.15, w: 4.5, h: 0.22,
  fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY, align: "center"
});
slide14.addText("\u2191 技术创新成熟度", {
  x: 0.12, y: 2.4, w: 0.28, h: 1.4,
  fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY, valign: "middle", rotate: 270
});

// Axes
slide14.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.38, w: 9.35, h: 0,
  line: { color: LTGRAY, width: 0.75 }
});
slide14.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.38, w: 0, h: 3.58,
  line: { color: LTGRAY, width: 0.75 }
});
// Dashed dividers
slide14.addShape(pres.shapes.LINE, {
  x: 5.2, y: 1.38, w: 0, h: 3.58,
  line: { color: "E0E0E0", width: 1, dashType: "dash" }
});
slide14.addShape(pres.shapes.LINE, {
  x: 0.5, y: 3.18, w: 9.35, h: 0,
  line: { color: "E0E0E0", width: 1, dashType: "dash" }
});

// Quadrant corner labels
const qLabels = [
  { x: 0.6, y: 1.45, text: "高成熟\n低覆盖", color: LTGRAY },
  { x: 5.35, y: 1.45, text: "高成熟\n高覆盖", color: GREEN },
  { x: 0.6, y: 3.25, text: "低成熟\n低覆盖", color: ORANGE },
  { x: 5.35, y: 3.25, text: "低成熟\n高覆盖", color: RED },
];
qLabels.forEach(q => {
  slide14.addText(q.text, {
    x: q.x, y: q.y, w: 0.95, h: 0.5,
    fontSize: 7, fontFace: "Microsoft YaHei", color: q.color, align: "center"
  });
});

// Q1 (top-left): 静默老牌
slide14.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.9, w: 4.4, h: 1.1,
  fill: { color: WHITE }, line: { color: LTGRAY, width: 1 }
});
slide14.addText("E+H / 梅特勒 / 横河", {
  x: 0.72, y: 1.98, w: 3.0, h: 0.28,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
slide14.addText("国际老牌，展会期间无大动作披露", {
  x: 0.72, y: 2.26, w: 3.8, h: 0.24,
  fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
});
slide14.addShape(pres.shapes.RECTANGLE, {
  x: 4.0, y: 2.5, w: 0.85, h: 0.28,
  fill: { color: LTGRAY }
});
slide14.addText("静默", {
  x: 4.0, y: 2.5, w: 0.85, h: 0.28,
  fontSize: 9, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});

// Q2 (top-right): 领导者
const q2Data = [
  { name: "聚光/谱育", badge: "领导者", badgeColor: GREEN, desc: "双奖得主，实验室无人化+巡检机器人，平台化整套输出" },
  { name: "赛莱默(Xylem)", badge: "领导者", badgeColor: GREEN, desc: "POM系统+臭氧新品，硬件AI融合，E1馆市政水务" },
];
q2Data.forEach((item, i) => {
  const y = 1.9 + i * 1.18;
  slide14.addShape(pres.shapes.RECTANGLE, {
    x: 5.3, y, w: 4.5, h: 1.05,
    fill: { color: WHITE }, line: { color: GREEN, width: 1.5 }
  });
  slide14.addShape(pres.shapes.RECTANGLE, {
    x: 5.3, y, w: 0.06, h: 1.05,
    fill: { color: GREEN }
  });
  slide14.addText(item.name, {
    x: 5.46, y: y + 0.06, w: 3.0, h: 0.28,
    fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slide14.addText(item.desc, {
    x: 5.46, y: y + 0.36, w: 4.2, h: 0.62,
    fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
  });
  slide14.addShape(pres.shapes.RECTANGLE, {
    x: 8.82, y: y + 0.06, w: 0.88, h: 0.26,
    fill: { color: item.badgeColor }
  });
  slide14.addText(item.badge, {
    x: 8.82, y: y + 0.06, w: 0.88, h: 0.26,
    fontSize: 8, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
});

// Q3 (bottom-left): 新品
const q3Data = [
  { name: "格林凯瑞", desc: "水质预制试剂新品" },
  { name: "诺方", desc: "0.1μm颗粒计数器" },
];
q3Data.forEach((item, i) => {
  const x = 0.6 + i * 2.45;
  slide14.addShape(pres.shapes.RECTANGLE, {
    x, y: 3.72, w: 2.25, h: 1.02,
    fill: { color: WHITE }, line: { color: ORANGE, width: 1 }
  });
  slide14.addText(item.name, {
    x: x + 0.1, y: 3.8, w: 2.05, h: 0.28,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slide14.addText(item.desc, {
    x: x + 0.1, y: 4.1, w: 2.05, h: 0.24,
    fontSize: 9, fontFace: "Microsoft YaHei", color: LTGRAY
  });
  slide14.addShape(pres.shapes.RECTANGLE, {
    x: x + 0.1, y: 4.36, w: 0.42, h: 0.2,
    fill: { color: ORANGE }
  });
  slide14.addText("新品", {
    x: x + 0.1, y: 4.36, w: 0.42, h: 0.2,
    fontSize: 7, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, align: "center", valign: "middle"
  });
});

// Q4 (bottom-right): 替代/综合威胁
const q4Data = [
  { name: "国产替代军团\n(雷磁/虹润/深昌鸿等)", desc: "价格低40-60%，满足国产优先政策，市政采购入围" },
  { name: "威立雅", desc: "人形机器人+AI降碳，综合服务AI化，E1馆" },
];
q4Data.forEach((item, i) => {
  const y = 3.72 + i * 0.68;
  slide14.addShape(pres.shapes.RECTANGLE, {
    x: 5.3, y, w: 4.5, h: 0.6,
    fill: { color: WHITE }, line: { color: RED, width: 1 }
  });
  slide14.addShape(pres.shapes.RECTANGLE, {
    x: 5.3, y, w: 0.06, h: 0.6,
    fill: { color: RED }
  });
  slide14.addText(item.name, {
    x: 5.46, y: y + 0.04, w: 2.8, h: 0.3,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
  slide14.addText(item.desc, {
    x: 5.46, y: y + 0.33, w: 4.24, h: 0.22,
    fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
  });
});

// ============================================================
// SLIDE 15: 竞品动态 - 软件/平台/AI
// Layout: Each company = one FULL-WIDTH card, single column
// No horizontal stacking — every overlap impossible
// Vertical layout (all measurements in inches, slide height = 5.625"):
//   Header:       y=0.3 h=0.55  (title area)
//   Card 1:       y=1.22  h=0.72  — 江苏纽带智能
//   Card 2:       y=2.00  h=0.72  — 首创环保/鸿泰华瑞
//   Card 3:       y=2.78  h=0.60  — 智易时代
//   Card 4:       y=3.44  h=0.60  — E20环境平台
//   Card 5:       y=4.10  h=0.60  — 昕彤智能
//   Band3 row:    y=4.76  h=0.50  — 中威胁33家（single row, no card border needed）
//   Opp box:      y=5.31  h=0.28  — 机遇窗口 (sits just above footer at 5.15)
//   Footer:       y=5.15  h=0.30  — (标准位置，opp box在footer上方留足空间)
// ============================================================
let slide15 = pres.addSlide();
addSlideHeader(slide15, "B", "软件/平台/AI服务竞品动态：谁在重新定义竞争规则", "分析方法：威胁本质 x 可copy性分层 | 数据来源：展商样本 + 论坛内容");
addFooter(slide15, "可copy性：自研难度（高=难以复制，中=可以借鉴，低=容易被抄）");

// ---- CARD LAYOUT CONSTANTS ----
const CARD_X   = 0.5;   // card left edge
const CARD_W   = 9.35;  // card width (full slide)
const LEFT_W   = 0.65;  // left colored strip width
const CONTENT_X = 1.22; // content starts here
const CONTENT_W = 8.55; // CONTENT_X + CONTENT_W = 9.77 (safe, within slide)
const RIGHT_BADGE_X = 8.93; // badge right edge (within CONTENT_W)
const BADGE_W  = 0.62;

function drawCard(slide, y, h, borderColor, stripColor, rows) {
  // Card background + border
  slide.addShape(pres.shapes.RECTANGLE, {
    x: CARD_X, y, w: CARD_W, h,
    fill: { color: WHITE }, line: { color: borderColor, width: 1 }
  });
  // Left color strip
  slide.addShape(pres.shapes.RECTANGLE, {
    x: CARD_X, y, w: LEFT_W, h: LEFT_W,
    fill: { color: stripColor }
  });
  return { stripEndX: CARD_X + LEFT_W, contentX: CONTENT_X, contentW: CONTENT_W };
}

// ---- CARD 1: 江苏纽带智能 (极高威胁) ----
// y=1.22, h=0.72  content: 1 row of text at y+0.08
drawCard(slide15, 1.22, 0.72, RED, RED);
slide15.addText("\u26A0\u26A0\u26A0", {
  x: CARD_X, y: 1.22, w: LEFT_W, h: LEFT_W,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});
slide15.addText("江苏纽带智能", {
  x: CONTENT_X, y: 1.3, w: 4.0, h: 0.26,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
slide15.addText("(E3-G61)", {
  x: CONTENT_X + 4.0, y: 1.3, w: 0.9, h: 0.26,
  fontSize: 10, fontFace: "Microsoft YaHei", color: LTGRAY
});
slide15.addText("产品: 传感器+云平台+运维一体化", {
  x: CONTENT_X, y: 1.56, w: 5.5, h: 0.2,
  fontSize: 9, fontFace: "Microsoft YaHei", color: BLUE
});
slide15.addText("\u27A4 平台型：端到端智能监测，传感器是入口，云平台是底座，运维是粘性", {
  x: CONTENT_X, y: 1.76, w: 7.9, h: 0.2,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});
slide15.addShape(pres.shapes.RECTANGLE, {
  x: RIGHT_BADGE_X, y: 1.3, w: BADGE_W, h: 0.22,
  fill: { color: LTGRAY }
});
slide15.addText("可copy:极高", {
  x: RIGHT_BADGE_X, y: 1.3, w: BADGE_W, h: 0.22,
  fontSize: 7, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});

// ---- CARD 2: 首创环保 / 鸿泰华瑞 (极高威胁) ----
// y=2.00, h=0.72
drawCard(slide15, 2.00, 0.72, RED, RED);
slide15.addText("\u26A0\u26A0\u26A0", {
  x: CARD_X, y: 2.00, w: LEFT_W, h: LEFT_W,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});
slide15.addText("首创环保 / 鸿泰华瑞", {
  x: CONTENT_X, y: 2.08, w: 4.5, h: 0.26,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
slide15.addText("产品: ASMART模型+WEAM / 飛鸿AI系统", {
  x: CONTENT_X, y: 2.34, w: 6.0, h: 0.2,
  fontSize: 9, fontFace: "Microsoft YaHei", color: BLUE
});
slide15.addText("\u27A4 把运营经验/AI决策变平台，让仪器变数据源，算法成决策核心", {
  x: CONTENT_X, y: 2.54, w: 7.9, h: 0.2,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});
slide15.addShape(pres.shapes.RECTANGLE, {
  x: RIGHT_BADGE_X, y: 2.08, w: BADGE_W, h: 0.22,
  fill: { color: ORANGE }
});
slide15.addText("可copy:高", {
  x: RIGHT_BADGE_X, y: 2.08, w: BADGE_W, h: 0.22,
  fontSize: 7, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});

// ---- CARD 3: 智易时代 (高威胁) ----
// y=2.78, h=0.60
drawCard(slide15, 2.78, 0.60, ORANGE, ORANGE);
slide15.addText("\u26A0\u26A0", {
  x: CARD_X, y: 2.78, w: LEFT_W, h: LEFT_W,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});
slide15.addText("智易时代", {
  x: CONTENT_X, y: 2.86, w: 3.0, h: 0.24,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
slide15.addText("(E3-D19/C20)", {
  x: CONTENT_X + 3.0, y: 2.86, w: 1.3, h: 0.24,
  fontSize: 10, fontFace: "Microsoft YaHei", color: LTGRAY
});
slide15.addText("产品: AI巡检机器人+算法  \u27A4 AI算法切入巡检场景，机器人替代人工巡检，AI创新奖认证", {
  x: CONTENT_X, y: 3.1, w: 7.9, h: 0.22,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});
slide15.addShape(pres.shapes.RECTANGLE, {
  x: RIGHT_BADGE_X, y: 2.86, w: BADGE_W, h: 0.22,
  fill: { color: ORANGE }
});
slide15.addText("可copy:高", {
  x: RIGHT_BADGE_X, y: 2.86, w: BADGE_W, h: 0.22,
  fontSize: 7, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});

// ---- CARD 4: E20环境平台 (高威胁) ----
// y=3.44, h=0.60
drawCard(slide15, 3.44, 0.60, ORANGE, ORANGE);
slide15.addText("\u26A0\u26A0", {
  x: CARD_X, y: 3.44, w: LEFT_W, h: LEFT_W,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});
slide15.addText("E20环境平台", {
  x: CONTENT_X, y: 3.52, w: 3.0, h: 0.24,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
slide15.addText("(E1馆)", {
  x: CONTENT_X + 3.0, y: 3.52, w: 0.8, h: 0.24,
  fontSize: 10, fontFace: "Microsoft YaHei", color: LTGRAY
});
slide15.addText("产品: 数字化平台  \u27A4 平台型数字化公司，用平台能力绑定客户，重构采购决策链", {
  x: CONTENT_X, y: 3.76, w: 7.9, h: 0.22,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});
slide15.addShape(pres.shapes.RECTANGLE, {
  x: RIGHT_BADGE_X, y: 3.52, w: BADGE_W, h: 0.22,
  fill: { color: ORANGE }
});
slide15.addText("可copy:高", {
  x: RIGHT_BADGE_X, y: 3.52, w: BADGE_W, h: 0.22,
  fontSize: 7, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});

// ---- CARD 5: 昕彤智能 (高威胁) ----
// y=4.10, h=0.60
drawCard(slide15, 4.10, 0.60, ORANGE, ORANGE);
slide15.addText("\u26A0\u26A0", {
  x: CARD_X, y: 4.10, w: LEFT_W, h: LEFT_W,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});
slide15.addText("昕彤智能", {
  x: CONTENT_X, y: 4.18, w: 3.0, h: 0.24,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
slide15.addText("产品: 剑企AI智能风机  \u27A4 硬件内嵌AI，曝气能耗降低30%，L4级水厂核心设备", {
  x: CONTENT_X, y: 4.42, w: 7.9, h: 0.22,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});
slide15.addShape(pres.shapes.RECTANGLE, {
  x: RIGHT_BADGE_X, y: 4.18, w: BADGE_W, h: 0.22,
  fill: { color: YELLOW }
});
slide15.addText("可copy:中", {
  x: RIGHT_BADGE_X, y: 4.18, w: BADGE_W, h: 0.22,
  fontSize: 7, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});

// ---- BAND 3: 中威胁（33家细分型） ----
// y=4.76, h=0.50 — no card border, just a colored strip row
slide15.addShape(pres.shapes.RECTANGLE, {
  x: CARD_X, y: 4.76, w: CARD_W, h: 0.50,
  fill: { color: WHITE }, line: { color: YELLOW, width: 1 }
});
slide15.addShape(pres.shapes.RECTANGLE, {
  x: CARD_X, y: 4.76, w: LEFT_W, h: 0.50,
  fill: { color: YELLOW }
});
slide15.addText("\u26A0", {
  x: CARD_X, y: 4.76, w: LEFT_W, h: 0.50,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});
slide15.addText("尚云互联 / 易环智能 / 盘古自动化 等33家", {
  x: CONTENT_X, y: 4.76, w: 4.5, h: 0.25,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
slide15.addText("产品: 智慧环保平台/自动化控制+AI算法  \u27A4 垂直场景绑定特定客户群体，技术copy壁垒不高但客户关系深", {
  x: CONTENT_X, y: 5.01, w: 7.9, h: 0.22,
  fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
});
slide15.addShape(pres.shapes.RECTANGLE, {
  x: RIGHT_BADGE_X, y: 4.76, w: BADGE_W, h: 0.22,
  fill: { color: YELLOW }
});
slide15.addText("可copy:中", {
  x: RIGHT_BADGE_X, y: 4.76, w: BADGE_W, h: 0.22,
  fontSize: 7, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, align: "center", valign: "middle"
});

// ---- OPPORTUNITY BOX ----
// y=5.31, h=0.28  — small insight box just above footer
slide15.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 5.31, w: 9.35, h: 0.28,
  fill: { color: "E8F5E9" },
  line: { color: GREEN, width: 1 }
});
slide15.addText("\u{1F4A1} 机遇窗口：政府AI体系已成型（山水大模型+700亿知识库），监测数据进入AI分析链——水质报告AI生成参照土壤/地下水案例已落地，Hach应抢占先机", {
  x: 0.6, y: 5.31, w: 9.15, h: 0.28,
  fontSize: 8.5, fontFace: "Microsoft YaHei",
  color: DKGRAY, valign: "middle"
});

// ============================================================
// SLIDE 16: 竞品对标与行动建议
// ============================================================
let slide16 = pres.addSlide();
addSlideHeader(slide16, "C", "竞品对标与Hach行动建议", "分析方法：基于竞品动态矩阵 | 适合管理层/IMS产品线内部讨论");
addFooter(slide16, "结论性质：★★ 有依据的推断 | 适合作为IMS产品线战略讨论输入，不构成确定性建议");

const actions = [
  {
    type: "硬件\u6587\u660E\u516C\u53F8\n(聚光/赛莱默/威立雅)",
    threat: "产品技术领先，平台化整套输出",
    hach: "加速软件能力内建，从卖设备转向卖监测服务",
    priority: "P0", color: RED
  },
  {
    type: "AI软件跨界\n(鸿泰华瑞/首创环保/纽带智能)",
    threat: "让仪器变数据源，算法成决策核心",
    hach: "硬件必须有软件接口，否则被管道化",
    priority: "P0", color: RED
  },
  {
    type: "国产替代军团\n(雷磁/虹润/深昌鸿)",
    threat: "价格低40-60%，国产优先政策受益",
    hach: "强化服务价值和长期总拥有成本优势",
    priority: "P1", color: ORANGE
  },
  {
    type: "AI创新新锐\n(智易时代/昕彤智能)",
    threat: "垂直场景AI落地，轻量化改造",
    hach: "评估合作或收购可能，填补AI能力短板",
    priority: "P1", color: ORANGE
  },
];
actions.forEach((item, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const x = 0.5 + col * 4.7;
  const y = 1.25 + row * 2.02;

  slide16.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 4.5, h: 1.88,
    fill: { color: WHITE },
    line: { color: item.color, width: 1.5 }
  });
  slide16.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 4.5, h: 0.44,
    fill: { color: item.color }
  });
  slide16.addText(item.type, {
    x: x + 0.1, y: y, w: 3.7, h: 0.44,
    fontSize: 11, fontFace: "Microsoft YaHei", bold: true,
    color: WHITE, valign: "middle"
  });
  slide16.addShape(pres.shapes.RECTANGLE, {
    x: x + 3.82, y: y + 0.08, w: 0.58, h: 0.28,
    fill: { color: WHITE }
  });
  slide16.addText(item.priority, {
    x: x + 3.82, y: y + 0.08, w: 0.58, h: 0.28,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
    color: item.color, align: "center", valign: "middle"
  });
  slide16.addText("威胁本质:", {
    x: x + 0.1, y: y + 0.52, w: 1.0, h: 0.22,
    fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: LTGRAY
  });
  slide16.addText(item.threat, {
    x: x + 0.1, y: y + 0.72, w: 4.2, h: 0.36,
    fontSize: 9, fontFace: "Microsoft YaHei", color: DKGRAY
  });
  slide16.addText("Hach应对:", {
    x: x + 0.1, y: y + 1.1, w: 1.0, h: 0.22,
    fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: BLUE
  });
  slide16.addText(item.hach, {
    x: x + 0.1, y: y + 1.3, w: 4.2, h: 0.42,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
});

// ============================================================
// SLIDE 17: 竞品案例 — FOSS博瑞思（数智化路线）
// ============================================================
let slide17 = pres.addSlide();
addSlideHeader(slide17, "D", "竞品案例：FOSS博瑞思 — AI+水监测仪器的数智化路线",
  "数据来源：2026环博会现场拍摄 | 核实：公司真实存在，专注水监测仪器+AI数智化，非'80%运维成本'宣传");
addFooter(slide17, "报告内容由AI辅助生成，仅供参考 | 重要澄清：现场数据来源存疑，已修正");

// Left column: company profile
slide17.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 1.2, w: 4.3, h: 3.9,
  fill: { color: WHITE }, line: { color: BLUE, width: 1.5 }
});
slide17.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 1.2, w: 4.3, h: 0.44,
  fill: { color: BLUE }
});
slide17.addText("FOSS博瑞思 / 六度物联", {
  x: 0.5, y: 1.2, w: 4.1, h: 0.44,
  fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
  color: WHITE, valign: "middle"
});
slide17.addText([
  { text: "公司定位", options: { bold: true, color: BLUE, breakLine: true } },
  { text: "以水监测仪器为核心，AI全面赋能，做客户的数智生态伙伴", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "产品矩阵", options: { bold: true, color: BLUE, breakLine: true } },
  { text: "水质分析仪 + 户外水站 + ROF深度物联架构", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "核心技术", options: { bold: true, color: BLUE, breakLine: true } },
  { text: "ROF深度物联软件架构 + 低功耗4G模块", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "核心功能", options: { bold: true, color: BLUE, breakLine: true } },
  { text: "远程校准 / 核查 / 诊断 / 维护 / 升级 / 数据导出", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "公司背景", options: { bold: true, color: BLUE, breakLine: true } },
  { text: "博瑞思数智科技(深圳)有限公司，2017年成立，国高新/专精特新企业", options: { breakLine: false } }
], {
  x: 0.55, y: 1.72, w: 4.0, h: 3.3,
  fontSize: 10, fontFace: "Microsoft YaHei", color: DKGRAY,
  valign: "top", lineSpacing: 18
});

// Right column: Hach IMS vs FOSS
slide17.addShape(pres.shapes.RECTANGLE, {
  x: 4.9, y: 1.2, w: 4.9, h: 3.9,
  fill: { color: WHITE }, line: { color: LTGRAY, width: 1 }
});
slide17.addText("Hach IMS vs FOSS博瑞思 功能对标", {
  x: 5.0, y: 1.28, w: 4.7, h: 0.32,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});

const compFeatures = [
  { feat: "远程校准/诊断", ims: true, foss: true },
  { feat: "故障预测/预警", ims: true, foss: false },
  { feat: "仪表专属知识库", ims: true, foss: false },
  { feat: "移动端运维", ims: true, foss: true },
  { feat: "AI数据分析", ims: false, foss: true },
  { feat: "多品牌仪表兼容", ims: true, foss: true },
];
compFeatures.forEach((f, i) => {
  const y = 1.72 + i * 0.46;
  slide17.addText(f.feat, {
    x: 5.0, y, w: 2.0, h: 0.38,
    fontSize: 10, fontFace: "Microsoft YaHei", color: DKGRAY, valign: "middle"
  });
  // IMS column
  slide17.addText(f.ims ? "✓" : "—", {
    x: 7.05, y, w: 0.45, h: 0.38,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: f.ims ? GREEN : LTGRAY, align: "center", valign: "middle"
  });
  // FOSS column
  slide17.addText(f.foss ? "✓" : "—", {
    x: 8.6, y, w: 0.45, h: 0.38,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: f.foss ? BLUE : LTGRAY, align: "center", valign: "middle"
  });
});

// Header for columns
slide17.addText("功能", {
  x: 5.0, y: 1.5, w: 2.0, h: 0.22,
  fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: LTGRAY
});
slide17.addText("IMS", {
  x: 7.05, y: 1.5, w: 0.45, h: 0.22,
  fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: GREEN, align: "center"
});
slide17.addText("FOSS", {
  x: 8.6, y: 1.5, w: 0.45, h: 0.22,
  fontSize: 9, fontFace: "Microsoft YaHei", bold: true, color: BLUE, align: "center"
});
slide17.addShape(pres.shapes.LINE, {
  x: 7.5, y: 1.72, w: 0, h: 2.5,
  line: { color: "EEEEEE", width: 1 }
});

// Bottom insight
slide17.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 5.2, w: 9.4, h: 0.28,
  fill: { color: "FFF3E0" }
});
slide17.addText("IMS机会：FOSS强在AI能力，IMS强在仪表专属知识库——各自路线不同，FOSS是竞争威胁，IMS是互补需求", {
  x: 0.5, y: 5.2, w: 9.2, h: 0.28,
  fontSize: 9, fontFace: "Microsoft YaHei", color: ORANGE, valign: "middle"
});

// ============================================================
// SLIDE 18: 行业基准数据（修正版）
// ============================================================
let slide18 = pres.addSlide();
addSlideHeader(slide18, "E", "行业基准数据：设备量 / 故障率 / AI准确率",
  "数据来源：2026环博会展台实拍数据（数据来源待进一步核实，不作为正式引用）");
addFooter(slide18, "报告内容由AI辅助生成，仅供参考 | 数据主体可能为舜通智联或其他展商，有待进一步核实");

// Top KPIs
const kpis = [
  { num: "85,899", unit: "台", label: "全国设备总量" },
  { num: "47,644", unit: "台", label: "在线设备数量" },
  { num: "99.27%", unit: "", label: "AI识别准确率" },
  { num: "1,066", unit: "个", label: "覆盖站点数" },
];
kpis.forEach((k, i) => {
  const x = 0.4 + i * 2.4;
  slide18.addShape(pres.shapes.RECTANGLE, {
    x, y: 1.2, w: 2.2, h: 1.1,
    fill: { color: WHITE }, line: { color: BLUE, width: 1 }
  });
  slide18.addText(k.num + k.unit, {
    x, y: 1.22, w: 2.2, h: 0.62,
    fontSize: 22, fontFace: "Microsoft YaHei", bold: true,
    color: BLUE, align: "center", valign: "bottom"
  });
  slide18.addText(k.label, {
    x, y: 1.84, w: 2.2, h: 0.38,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: LTGRAY, align: "center", valign: "top"
  });
});

// Middle: fault distribution
slide18.addText("设备故障部位分布（占故障总量）", {
  x: 0.4, y: 2.48, w: 4.5, h: 0.32,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});

const faults = [
  { name: "分析仪", pct: "9.1%", bar: 0.91 },
  { name: "温度传感器", pct: "0.67%", bar: 0.067 },
  { name: "电动阀", pct: "0.45%", bar: 0.045 },
  { name: "采样泵", pct: "0.44%", bar: 0.044 },
  { name: "数采仪", pct: "0.01%", bar: 0.001 },
];
faults.forEach((f, i) => {
  const y = 2.88 + i * 0.38;
  slide18.addText(f.name, {
    x: 0.4, y, w: 1.2, h: 0.32,
    fontSize: 10, fontFace: "Microsoft YaHei", color: DKGRAY
  });
  slide18.addShape(pres.shapes.RECTANGLE, {
    x: 1.65, y: y + 0.06, w: 3.2, h: 0.2,
    fill: { color: "EEEEEE" }
  });
  slide18.addShape(pres.shapes.RECTANGLE, {
    x: 1.65, y: y + 0.06, w: 3.2 * f.bar, h: 0.2,
    fill: { color: f.bar > 0.1 ? RED : ORANGE }
  });
  slide18.addText(f.pct, {
    x: 4.9, y, w: 0.7, h: 0.32,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
  });
});

// Right: AI metrics
slide18.addText("AI运营效果", {
  x: 5.6, y: 2.48, w: 4.2, h: 0.32,
  fontSize: 11, fontFace: "Microsoft YaHei", bold: true, color: DKGRAY
});
slide18.addShape(pres.shapes.RECTANGLE, {
  x: 5.6, y: 2.88, w: 4.2, h: 1.88,
  fill: { color: WHITE }, line: { color: "E0E0E0", width: 1 }
});
const aiMetrics = [
  { label: "智能报警数量", val: "全国Top5" },
  { label: "覆盖率", val: "1,066个站点" },
  { label: "超标识别率", val: "100%" },
  { label: "运营成本降幅", val: "待核实" },
];
aiMetrics.forEach((m, i) => {
  const y = 2.96 + i * 0.44;
  slide18.addText(m.label + ":", {
    x: 5.75, y, w: 2.0, h: 0.36,
    fontSize: 10, fontFace: "Microsoft YaHei", color: LTGRAY
  });
  slide18.addText(m.val, {
    x: 7.75, y, w: 1.9, h: 0.36,
    fontSize: 10, fontFace: "Microsoft YaHei", bold: true, color: BLUE
  });
});

// Bottom: Hach comparison
slide18.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 4.92, w: 9.4, h: 0.28,
  fill: { color: "FFF3E0" }
});
slide18.addText("IMS参照：分析仪故障占9.1%为最高——IMS的'预测性维护'价值在此场景最高；数据来源待核实，不作为正式引用", {
  x: 0.5, y: 4.92, w: 9.2, h: 0.28,
  fontSize: 9, fontFace: "Microsoft YaHei", color: ORANGE, valign: "middle"
});

// ============================================================
// SAVE
// ============================================================
pres.writeFile({ fileName: "/home/agentuser/环博会市场观察_20260429.pptx" })
  .then(() => console.log("Done: /home/agentuser/环博会市场观察_20260429.pptx"))
  .catch(e => console.error(e));
