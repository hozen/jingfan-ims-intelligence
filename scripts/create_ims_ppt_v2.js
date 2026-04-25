const pptxgen = require("pptxgenjs");

async function createPresentation() {
  let pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title = "IMS产品战略规划 - 2026环博会";
  pres.author = "哈希中国";

  // Color palette - professional blue/teal theme
  const colors = {
    primary: "003366",      // Deep blue
    secondary: "0066CC",    // Bright blue
    accent: "00A0B0",       // Teal
    dark: "1A1A2E",         // Dark navy
    light: "F5F7FA",        // Light gray
    white: "FFFFFF",
    text: "333333",
    lightText: "666666"
  };

  // Shadow factory
  const makeShadow = () => ({
    type: "outer", color: "000000",
    blur: 8, offset: 3, angle: 135, opacity: 0.12
  });

  // ========== SLIDE 1: Title Slide ==========
  let slide1 = pres.addSlide();
  slide1.background = { color: colors.dark };

  // Decorative shape - large circle
  slide1.addShape(pres.shapes.OVAL, {
    x: -2, y: -1, w: 6, h: 6,
    fill: { color: colors.secondary, transparency: 85 }
  });
  slide1.addShape(pres.shapes.OVAL, {
    x: 7, y: 3, w: 5, h: 5,
    fill: { color: colors.accent, transparency: 80 }
  });

  // Main title
  slide1.addText("IMS产品战略规划", {
    x: 0.8, y: 1.8, w: 8.5, h: 1.2,
    fontSize: 44, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true
  });

  // Subtitle
  slide1.addText("2026年第27届中国环博会", {
    x: 0.8, y: 3.0, w: 8.5, h: 0.6,
    fontSize: 24, fontFace: "Microsoft YaHei",
    color: colors.accent
  });

  // Event info bar
  slide1.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 4.4, w: 10, h: 1.2,
    fill: { color: colors.secondary, transparency: 30 }
  });
  slide1.addText("2026.04.13-15  |  上海新国际博览中心  |  哈希(HACH)", {
    x: 0.8, y: 4.6, w: 8.5, h: 0.8,
    fontSize: 16, fontFace: "Microsoft YaHei",
    color: colors.white, align: "left"
  });

  // ========== SLIDE 2: Market Overview ==========
  let slide2 = pres.addSlide();
  slide2.background = { color: colors.light };

  // Header bar
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.1,
    fill: { color: colors.primary }
  });
  slide2.addText("行业 overview", {
    x: 0.5, y: 0.25, w: 9, h: 0.6,
    fontSize: 28, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true, margin: 0
  });

  // Main content card
  slide2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.4, w: 9, h: 3.9,
    fill: { color: colors.white },
    rectRadius: 0.15,
    shadow: makeShadow()
  });

  // Title inside card
  slide2.addText("2026环保产业趋势", {
    x: 0.8, y: 1.6, w: 8.5, h: 0.5,
    fontSize: 20, fontFace: "Microsoft YaHei",
    color: colors.primary, bold: true
  });

  // Content points
  const marketPoints = [
    { text: "双碳目标驱动：2030碳达峰、2060碳中和政策加速落地", options: { bullet: true, breakLine: true } },
    { text: "水质监测市场年复合增长率预计超过12%", options: { bullet: true, breakLine: true } },
    { text: "智慧水务建设成为城市基础设施升级重点", options: { bullet: true, breakLine: true } },
    { text: "长三角、珠三角区域污水提标改造需求旺盛", options: { bullet: true, breakLine: true } },
    { text: "数字化、智能化监测设备国产替代加速", options: { bullet: true } }
  ];
  slide2.addText(marketPoints, {
    x: 0.8, y: 2.2, w: 8.4, h: 2.8,
    fontSize: 16, fontFace: "Microsoft YaHei",
    color: colors.text, paraSpaceAfter: 8
  });

  // ========== SLIDE 3: Expo Info ==========
  let slide3 = pres.addSlide();
  slide3.background = { color: colors.light };

  // Header
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.1,
    fill: { color: colors.primary }
  });
  slide3.addText("展会概览", {
    x: 0.5, y: 0.25, w: 9, h: 0.6,
    fontSize: 28, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true, margin: 0
  });

  // Left column - event details card
  slide3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.4, w: 4.3, h: 3.9,
    fill: { color: colors.white },
    rectRadius: 0.15,
    shadow: makeShadow()
  });

  slide3.addText("第27届中国环博会", {
    x: 0.7, y: 1.6, w: 4, h: 0.5,
    fontSize: 18, fontFace: "Microsoft YaHei",
    color: colors.primary, bold: true
  });

  const expoDetails = [
    { text: "时间", options: { bold: true, breakLine: true } },
    { text: "2026年4月13-15日", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "地点", options: { bold: true, breakLine: true } },
    { text: "上海新国际博览中心", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "主题", options: { bold: true, breakLine: true } },
    { text: "链接全球机遇，探索新兴动能", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "聚焦领域", options: { bold: true, breakLine: true } },
    { text: "资源化 · 循环化 · 低碳化", options: {} }
  ];
  slide3.addText(expoDetails, {
    x: 0.7, y: 2.2, w: 4, h: 3,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: colors.text
  });

  // Right column - Hach presence card
  slide3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 5.2, y: 1.4, w: 4.3, h: 3.9,
    fill: { color: colors.primary },
    rectRadius: 0.15,
    shadow: makeShadow()
  });

  slide3.addText("哈希展位亮点", {
    x: 5.4, y: 1.6, w: 4, h: 0.5,
    fontSize: 18, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true
  });

  const hachPresence = [
    { text: "展位规模：全面展示智能化水质监测解决方案", options: { bullet: true, breakLine: true } },
    { text: "新品发布：IMS智能监测平台重磅亮相", options: { bullet: true, breakLine: true } },
    { text: "技术专家：现场技术交流与方案定制", options: { bullet: true, breakLine: true } },
    { text: "行业论坛：参与高峰对话，分享洞察", options: { bullet: true } }
  ];
  slide3.addText(hachPresence, {
    x: 5.4, y: 2.2, w: 4, h: 2.8,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: colors.white, paraSpaceAfter: 10
  });

  // ========== SLIDE 4: Industry Challenges ==========
  let slide4 = pres.addSlide();
  slide4.background = { color: colors.light };

  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.1,
    fill: { color: colors.primary }
  });
  slide4.addText("变局特征与挑战", {
    x: 0.5, y: 0.25, w: 9, h: 0.6,
    fontSize: 28, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true, margin: 0
  });

  // Challenge cards - 2x2 grid
  const challenges = [
    { title: "政策波动", desc: "环保标准频繁更新，监测指标持续扩展，企业合规成本上升" },
    { title: "技术迭代", desc: "物联网、AI诊断、边缘计算重塑行业，技术路线选择难度增加" },
    { title: "市场竞争", desc: "国产厂商崛起，价格竞争加剧，高端市场被国际品牌占据" },
    { title: "客户需求", desc: "从单点监测向全流程智慧管理转型，一站式解决方案成刚需" }
  ];

  const cardW = 4.3, cardH = 1.7;
  const positions = [
    { x: 0.5, y: 1.4 }, { x: 5.2, y: 1.4 },
    { x: 0.5, y: 3.3 }, { x: 5.2, y: 3.3 }
  ];

  challenges.forEach((item, i) => {
    const pos = positions[i];
    slide4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: pos.x, y: pos.y, w: cardW, h: cardH,
      fill: { color: colors.white },
      rectRadius: 0.1,
      shadow: makeShadow()
    });
    // Number badge
    slide4.addShape(pres.shapes.OVAL, {
      x: pos.x + 0.15, y: pos.y + 0.15, w: 0.4, h: 0.4,
      fill: { color: colors.accent }
    });
    slide4.addText(String(i + 1), {
      x: pos.x + 0.15, y: pos.y + 0.15, w: 0.4, h: 0.4,
      fontSize: 14, fontFace: "Arial",
      color: colors.white, bold: true, align: "center", valign: "middle"
    });
    // Title
    slide4.addText(item.title, {
      x: pos.x + 0.65, y: pos.y + 0.15, w: 3.5, h: 0.4,
      fontSize: 16, fontFace: "Microsoft YaHei",
      color: colors.primary, bold: true, valign: "middle"
    });
    // Description
    slide4.addText(item.desc, {
      x: pos.x + 0.2, y: pos.y + 0.65, w: 3.9, h: 0.9,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: colors.text
    });
  });

  // ========== SLIDE 5: IMS Core Capabilities ==========
  let slide5 = pres.addSlide();
  slide5.background = { color: colors.dark };

  slide5.addText("IMS核心能力", {
    x: 0.5, y: 0.3, w: 9, h: 0.8,
    fontSize: 32, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true
  });

  slide5.addText("Intelligent Monitoring System — 智能化监测系统", {
    x: 0.5, y: 1.0, w: 9, h: 0.4,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: colors.accent
  });

  // Capability cards - 3 columns
  const capabilities = [
    {
      title: "端到端监测",
      points: ["在线分析仪全参数覆盖", "数据采集稳定性99.9%", "无人值守远程运维"]
    },
    {
      title: "智能分析",
      points: ["AI预警模型提前发现异常", "趋势预测指导运维决策", "故障诊断降低停机时间"]
    },
    {
      title: "平台整合",
      points: ["统一数据中台打破信息孤岛", "开放式API对接客户系统", "定制化报表满足管理需求"]
    }
  ];

  const capW = 2.9, capH = 3.2;
  capabilities.forEach((cap, i) => {
    const x = 0.5 + i * 3.15;
    slide5.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 1.6, w: capW, h: capH,
      fill: { color: colors.primary },
      rectRadius: 0.1
    });
    slide5.addText(cap.title, {
      x: x, y: 1.8, w: capW, h: 0.5,
      fontSize: 16, fontFace: "Microsoft YaHei",
      color: colors.accent, bold: true, align: "center"
    });
    const pts = cap.points.map((p, idx) => ({
      text: p,
      options: { bullet: true, breakLine: idx < cap.points.length - 1 }
    }));
    slide5.addText(pts, {
      x: x + 0.15, y: 2.4, w: capW - 0.3, h: 2.2,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: colors.white, paraSpaceAfter: 8
    });
  });

  // ========== SLIDE 6: Hach Advantages ==========
  let slide6 = pres.addSlide();
  slide6.background = { color: colors.light };

  slide6.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.1,
    fill: { color: colors.primary }
  });
  slide6.addText("哈希核心优势", {
    x: 0.5, y: 0.25, w: 9, h: 0.6,
    fontSize: 28, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true, margin: 0
  });

  // Left side - brand intro
  slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.4, w: 4.3, h: 3.9,
    fill: { color: colors.primary },
    rectRadius: 0.15,
    shadow: makeShadow()
  });

  slide6.addText("哈希(HACH)", {
    x: 0.7, y: 1.6, w: 4, h: 0.5,
    fontSize: 20, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true
  });

  const brandInfo = [
    { text: "Founded 1947 | 79年行业深耕", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Since 2023: Part of Veralto Group", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Global Leaders in Water Analysis", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "中国研发，世界标准", options: { bold: true } }
  ];
  slide6.addText(brandInfo, {
    x: 0.7, y: 2.2, w: 4, h: 2.8,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: colors.white
  });

  // Right side - advantages
  slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 5.2, y: 1.4, w: 4.3, h: 3.9,
    fill: { color: colors.white },
    rectRadius: 0.15,
    shadow: makeShadow()
  });

  slide6.addText("为什么选择哈希IMS", {
    x: 5.4, y: 1.6, w: 4, h: 0.5,
    fontSize: 16, fontFace: "Microsoft YaHei",
    color: colors.primary, bold: true
  });

  const advantages = [
    { text: "1947年专业积累，覆盖全参数水质监测", options: { bullet: true, breakLine: true } },
    { text: "中国20年本土研发，本地化定制能力", options: { bullet: true, breakLine: true } },
    { text: "多品牌矩阵 (Polymetron, Orbisphere等)", options: { bullet: true, breakLine: true } },
    { text: "全国服务网络，售后响应快", options: { bullet: true, breakLine: true } },
    { text: "全球100万+用户认可，品质可靠", options: { bullet: true } }
  ];
  slide6.addText(advantages, {
    x: 5.4, y: 2.2, w: 4, h: 2.8,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: colors.text, paraSpaceAfter: 8
  });

  // ========== SLIDE 7: Strategy ==========
  let slide7 = pres.addSlide();
  slide7.background = { color: colors.light };

  slide7.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.1,
    fill: { color: colors.primary }
  });
  slide7.addText("IMS战略定位", {
    x: 0.5, y: 0.25, w: 9, h: 0.6,
    fontSize: 28, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true, margin: 0
  });

  // Strategy diagram - horizontal flow
  const strategies = [
    { num: "01", title: "产品领先", desc: "聚焦高毛利细分市场，建立技术壁垒" },
    { num: "02", title: "方案赋能", desc: "从单品销售转向整体解决方案，提升客单价" },
    { num: "03", title: "服务增值", desc: "原厂服务+远程运维，打造持续收入模式" },
    { num: "04", title: "生态共建", desc: "对接智慧水务平台，融入客户数字化转型" }
  ];

  const stratW = 2.15;
  strategies.forEach((s, i) => {
    const x = 0.5 + i * 2.4;
    slide7.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 1.5, w: stratW, h: 2.8,
      fill: { color: colors.white },
      rectRadius: 0.1,
      shadow: makeShadow()
    });
    // Number
    slide7.addText(s.num, {
      x: x, y: 1.7, w: stratW, h: 0.6,
      fontSize: 28, fontFace: "Arial",
      color: colors.accent, bold: true, align: "center"
    });
    // Title
    slide7.addText(s.title, {
      x: x, y: 2.4, w: stratW, h: 0.5,
      fontSize: 16, fontFace: "Microsoft YaHei",
      color: colors.primary, bold: true, align: "center"
    });
    // Desc
    slide7.addText(s.desc, {
      x: x + 0.1, y: 3.0, w: stratW - 0.2, h: 1.1,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: colors.text, align: "center"
    });
    // Arrow (except last)
    if (i < 3) {
      slide7.addText("→", {
        x: x + stratW - 0.1, y: 2.5, w: 0.5, h: 0.5,
        fontSize: 24, color: colors.accent, align: "center"
      });
    }
  });

  // Bottom highlight box
  slide7.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 4.5, w: 9, h: 0.9,
    fill: { color: colors.secondary, transparency: 15 },
    rectRadius: 0.1
  });
  slide7.addText("🎯 目标：2026年环博会期间，IMS解决方案签约金额突破XXXX万元", {
    x: 0.7, y: 4.6, w: 8.6, h: 0.7,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: colors.primary, bold: true, valign: "middle"
  });

  // ========== SLIDE 8: Call to Action ==========
  let slide8 = pres.addSlide();
  slide8.background = { color: colors.dark };

  // Decorative shapes
  slide8.addShape(pres.shapes.OVAL, {
    x: 6, y: -2, w: 8, h: 8,
    fill: { color: colors.secondary, transparency: 85 }
  });
  slide8.addShape(pres.shapes.OVAL, {
    x: -3, y: 3, w: 6, h: 6,
    fill: { color: colors.accent, transparency: 85 }
  });

  slide8.addText("立即行动", {
    x: 0.5, y: 1.5, w: 9, h: 0.8,
    fontSize: 36, fontFace: "Microsoft YaHei",
    color: colors.white, bold: true
  });

  slide8.addText("携手哈希IMS，共赢环保新时代", {
    x: 0.5, y: 2.3, w: 9, h: 0.6,
    fontSize: 20, fontFace: "Microsoft YaHei",
    color: colors.accent
  });

  // Contact info
  const contactItems = [
    { text: "联系我们：400-686-8899 / 800-840-6026", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "官网：www.hach.com.cn", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "期待与您相聚2026环博会！", options: { bold: true } }
  ];
  slide8.addText(contactItems, {
    x: 0.5, y: 3.2, w: 9, h: 2,
    fontSize: 16, fontFace: "Microsoft YaHei",
    color: colors.white
  });

  // Save
  await pres.writeFile({ fileName: "/home/agentuser/IMS产品战略规划_2026环博会.pptx" });
  console.log("PPT created successfully!");
}

createPresentation().catch(console.error);
