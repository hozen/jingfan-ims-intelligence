const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// Icons from react-icons
const { 
  FaChartLine, FaCogs, FaGlobeAsia, FaLightbulb, FaUsers, FaRocket,
  FaExclamationTriangle, FaCheckCircle, FaArrowUp, FaArrowRight, FaSyncAlt,
  FaIndustry, FaMicrochip, FaCloud, FaShieldAlt, FaChartBar
} = require("react-icons/fa");

// Helper function to render icon to PNG base64
function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// Color palette - Ocean Gradient theme for environmental/tech feel
const COLORS = {
  primary: "0D4F8B",      // Deep ocean blue
  secondary: "1A7BB9",    // Medium blue
  accent: "2DD4BF",       // Teal/mint accent
  dark: "0A2540",         // Very dark blue
  light: "F0F9FF",        // Light blue-white
  text: "1E293B",         // Dark slate
  textLight: "64748B",    // Muted slate
  white: "FFFFFF",
  success: "10B981",      // Green
  warning: "F59E0B",      // Amber
};

async function createPresentation() {
  let pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  pres.title = 'IMS产品与2026环博会机遇分析';
  pres.author = 'IMS产品团队';

  // ========== Slide 1: Title Slide ==========
  let slide1 = pres.addSlide();
  slide1.background = { color: COLORS.dark };
  
  // Decorative shape - top accent bar
  slide1.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: COLORS.accent }
  });
  
  // Main title
  slide1.addText("IMS产品战略规划", {
    x: 0.5, y: 1.8, w: 9, h: 1.2,
    fontSize: 48, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, align: "center"
  });
  
  // Subtitle
  slide1.addText("如何在快速变化期中制胜", {
    x: 0.5, y: 3.0, w: 9, h: 0.7,
    fontSize: 28, fontFace: "Microsoft YaHei",
    color: COLORS.accent, align: "center"
  });
  
  // Event tag
  slide1.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 3.2, y: 3.9, w: 3.6, h: 0.55,
    fill: { color: COLORS.secondary, transparency: 30 },
    rectRadius: 0.1
  });
  slide1.addText("2026环博会机遇分析", {
    x: 3.2, y: 3.9, w: 3.6, h: 0.55,
    fontSize: 16, fontFace: "Microsoft YaHei",
    color: COLORS.white, align: "center", valign: "middle"
  });
  
  // Bottom decorative line
  slide1.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.35, w: 10, h: 0.08,
    fill: { color: COLORS.accent }
  });
  
  // Footer
  slide1.addText("哈希靖帆IMS产品团队", {
    x: 0.5, y: 5.1, w: 9, h: 0.4,
    fontSize: 12, fontFace: "Microsoft YaHei",
    color: COLORS.textLight, align: "center"
  });

  // ========== Slide 2: Agenda ==========
  let slide2 = pres.addSlide();
  slide2.background = { color: COLORS.white };
  
  // Header bar
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.9,
    fill: { color: COLORS.primary }
  });
  slide2.addText("内容概览", {
    x: 0.5, y: 0.2, w: 9, h: 0.5,
    fontSize: 28, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, margin: 0
  });

  const agendaItems = [
    { num: "01", title: "2026环博会概览", desc: "展会规模、主题与行业趋势" },
    { num: "02", title: "环境行业发展洞察", desc: "双碳目标下的市场机遇与挑战" },
    { num: "03", title: "IMS产品现状分析", desc: "核心竞争力与市场定位" },
    { num: "04", title: "快速变化期的应对策略", desc: "产品优化与市场策略建议" },
  ];

  agendaItems.forEach((item, i) => {
    const yPos = 1.3 + i * 1.05;
    
    // Number circle
    slide2.addShape(pres.shapes.OVAL, {
      x: 0.8, y: yPos, w: 0.7, h: 0.7,
      fill: { color: COLORS.accent }
    });
    slide2.addText(item.num, {
      x: 0.8, y: yPos, w: 0.7, h: 0.7,
      fontSize: 18, fontFace: "Arial", bold: true,
      color: COLORS.dark, align: "center", valign: "middle"
    });
    
    // Title and description
    slide2.addText(item.title, {
      x: 1.7, y: yPos + 0.05, w: 7, h: 0.4,
      fontSize: 20, fontFace: "Microsoft YaHei", bold: true,
      color: COLORS.text
    });
    slide2.addText(item.desc, {
      x: 1.7, y: yPos + 0.4, w: 7, h: 0.35,
      fontSize: 14, fontFace: "Microsoft YaHei",
      color: COLORS.textLight
    });
  });

  // ========== Slide 3: 2026环博会概览 ==========
  let slide3 = pres.addSlide();
  slide3.background = { color: COLORS.white };
  
  // Header
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.9,
    fill: { color: COLORS.primary }
  });
  slide3.addText("2026环博会概览", {
    x: 0.5, y: 0.2, w: 9, h: 0.5,
    fontSize: 28, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, margin: 0
  });

  // Left column - key facts
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.2, w: 4.3, h: 4.1,
    fill: { color: COLORS.light }
  });
  
  slide3.addText("展会基本信息", {
    x: 0.7, y: 1.35, w: 4, h: 0.45,
    fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.primary
  });
  
  const expoFacts = [
    { label: "展会名称", value: "IFAT China 2026" },
    { label: "时间", value: "2026年4月" },
    { label: "地点", value: "上海新国际博览中心" },
    { label: "主题", value: "绿色低碳 · 智能未来" },
    { label: "预计规模", value: "2,200+ 参展商" },
    { label: "观众", value: "80,000+ 专业观众" },
  ];
  
  expoFacts.forEach((fact, i) => {
    const yPos = 1.9 + i * 0.52;
    slide3.addText(fact.label, {
      x: 0.7, y: yPos, w: 1.5, h: 0.4,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: COLORS.textLight
    });
    slide3.addText(fact.value, {
      x: 2.2, y: yPos, w: 2.4, h: 0.4,
      fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
      color: COLORS.text
    });
  });

  // Right column - trends
  slide3.addText("本届亮点趋势", {
    x: 5.1, y: 1.35, w: 4.5, h: 0.45,
    fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.primary
  });
  
  const trends = [
    "数智化转型加速，AIoT解决方案成焦点",
    "双碳目标驱动，碳核算与减排技术受关注",
    "水资源保护与再生利用持续升温",
    "智慧环保监测设备更新迭代",
    "新能源与绿色制造跨界融合"
  ];
  
  slide3.addText(
    trends.map((t, i) => ({
      text: t,
      options: { bullet: true, breakLine: i < trends.length - 1 }
    })),
    {
      x: 5.1, y: 1.9, w: 4.5, h: 3.2,
      fontSize: 14, fontFace: "Microsoft YaHei",
      color: COLORS.text, paraSpaceAfter: 8
    }
  );

  // ========== Slide 4: 行业洞察 ==========
  let slide4 = pres.addSlide();
  slide4.background = { color: COLORS.white };
  
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.9,
    fill: { color: COLORS.primary }
  });
  slide4.addText("环境行业发展洞察", {
    x: 0.5, y: 0.2, w: 9, h: 0.5,
    fontSize: 28, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, margin: 0
  });

  // Three columns layout
  const insights = [
    {
      title: "市场机遇",
      color: COLORS.success,
      items: ["政策持续加码，十四五规划深入推进", "万亿级环保投资持续释放", "中小企业数字化需求旺盛"]
    },
    {
      title: "面临挑战",
      color: COLORS.warning,
      items: ["国际供应链波动影响", "技术迭代速度加快", "行业竞争日趋激烈"]
    },
    {
      title: "关键趋势",
      color: COLORS.secondary,
      items: ["AIoT深度赋能环保产业", "系统集成化程度提高", "服务化转型加速"]
    }
  ];

  insights.forEach((insight, i) => {
    const xPos = 0.5 + i * 3.1;
    
    // Card background
    slide4.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: 1.15, w: 2.9, h: 4.2,
      fill: { color: COLORS.white },
      line: { color: "E2E8F0", width: 1 },
      shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.08 }
    });
    
    // Accent top bar
    slide4.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: 1.15, w: 2.9, h: 0.08,
      fill: { color: insight.color }
    });
    
    // Title
    slide4.addText(insight.title, {
      x: xPos, y: 1.4, w: 2.9, h: 0.5,
      fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
      color: insight.color, align: "center"
    });
    
    // Items
    slide4.addText(
      insight.items.map((item, j) => ({
        text: item,
        options: { bullet: true, breakLine: j < insight.items.length - 1 }
      })),
      {
        x: xPos + 0.15, y: 2.0, w: 2.6, h: 3.0,
        fontSize: 12, fontFace: "Microsoft YaHei",
        color: COLORS.text, paraSpaceAfter: 10
      }
    );
  });

  // ========== Slide 5: IMS核心能力 ==========
  let slide5 = pres.addSlide();
  slide5.background = { color: COLORS.white };
  
  slide5.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.9,
    fill: { color: COLORS.primary }
  });
  slide5.addText("IMS核心能力分析", {
    x: 0.5, y: 0.2, w: 9, h: 0.5,
    fontSize: 28, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, margin: 0
  });

  // IMS value proposition cards
  const capabilities = [
    { title: "智能管理平台", desc: "一站式综合管理，降低运营复杂度", icon: "FaCogs" },
    { title: "数据洞察能力", desc: "实时采集分析，驱动科学决策", icon: "FaChartBar" },
    { title: "系统集成优势", desc: "灵活对接多类设备与系统", icon: "FaSyncAlt" },
    { title: "行业know-how", desc: "深耕行业多年，深度理解客户需求", icon: "FaIndustry" },
  ];

  capabilities.forEach((cap, i) => {
    const xPos = 0.5 + (i % 2) * 4.7;
    const yPos = 1.2 + Math.floor(i / 2) * 2.1;
    
    // Card
    slide5.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: yPos, w: 4.4, h: 1.85,
      fill: { color: COLORS.white },
      line: { color: "E2E8F0", width: 1 },
      shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.08 }
    });
    
    // Left accent
    slide5.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: yPos, w: 0.08, h: 1.85,
      fill: { color: COLORS.accent }
    });
    
    // Title
    slide5.addText(cap.title, {
      x: xPos + 0.25, y: yPos + 0.2, w: 4, h: 0.5,
      fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
      color: COLORS.text
    });
    
    // Description
    slide5.addText(cap.desc, {
      x: xPos + 0.25, y: yPos + 0.7, w: 4, h: 0.9,
      fontSize: 14, fontFace: "Microsoft YaHei",
      color: COLORS.textLight
    });
  });

  // ========== Slide 6: 快速变化期分析 ==========
  let slide6 = pres.addSlide();
  slide6.background = { color: COLORS.dark };
  
  slide6.addText("快速变化期的特征", {
    x: 0.5, y: 0.4, w: 9, h: 0.6,
    fontSize: 28, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white
  });

  const changeFeatures = [
    { title: "技术迭代加速", desc: "AI、大数据、IoT技术快速渗透传统环保领域" },
    { title: "客户需求分化", desc: "大型企业与中小企业需求差异明显" },
    { title: "竞争格局重塑", desc: "跨界进入者增多，原有竞争边界模糊" },
    { title: "政策标准更新", desc: "环保法规和行业标准持续完善升级" },
  ];

  changeFeatures.forEach((feature, i) => {
    const xPos = 0.5 + (i % 2) * 4.7;
    const yPos = 1.3 + Math.floor(i / 2) * 2.0;
    
    // Number indicator
    slide6.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: yPos, w: 0.5, h: 0.5,
      fill: { color: COLORS.accent }
    });
    slide6.addText(String(i + 1), {
      x: xPos, y: yPos, w: 0.5, h: 0.5,
      fontSize: 18, fontFace: "Arial", bold: true,
      color: COLORS.dark, align: "center", valign: "middle"
    });
    
    // Title
    slide6.addText(feature.title, {
      x: xPos + 0.7, y: yPos, w: 3.8, h: 0.5,
      fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
      color: COLORS.accent
    });
    
    // Description
    slide6.addText(feature.desc, {
      x: xPos + 0.7, y: yPos + 0.55, w: 3.8, h: 1.2,
      fontSize: 14, fontFace: "Microsoft YaHei",
      color: COLORS.white
    });
  });

  // ========== Slide 7: 策略建议 ==========
  let slide7 = pres.addSlide();
  slide7.background = { color: COLORS.white };
  
  slide7.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.9,
    fill: { color: COLORS.primary }
  });
  slide7.addText("应对策略与建议", {
    x: 0.5, y: 0.2, w: 9, h: 0.5,
    fontSize: 28, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, margin: 0
  });

  const strategies = [
    {
      num: "01",
      title: "产品差异化",
      desc: "强化IMS智能分析能力，打造不可替代的核心价值"
    },
    {
      num: "02",
      title: "客户分层运营",
      desc: "针对不同客户群体提供差异化解决方案"
    },
    {
      num: "03",
      title: "生态合作共建",
      desc: "与设备厂商、系统集成商建立战略合作"
    },
    {
      num: "04",
      title: "服务能力升级",
      desc: "从产品交付向服务运营转型，提升客户粘性"
    },
  ];

  strategies.forEach((strat, i) => {
    const yPos = 1.2 + i * 1.05;
    
    // Number box
    slide7.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: yPos, w: 0.8, h: 0.8,
      fill: { color: COLORS.primary }
    });
    slide7.addText(strat.num, {
      x: 0.5, y: yPos, w: 0.8, h: 0.8,
      fontSize: 20, fontFace: "Arial", bold: true,
      color: COLORS.white, align: "center", valign: "middle"
    });
    
    // Title
    slide7.addText(strat.title, {
      x: 1.5, y: yPos + 0.05, w: 8, h: 0.4,
      fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
      color: COLORS.text
    });
    
    // Description
    slide7.addText(strat.desc, {
      x: 1.5, y: yPos + 0.45, w: 8, h: 0.45,
      fontSize: 14, fontFace: "Microsoft YaHei",
      color: COLORS.textLight
    });
  });

  // ========== Slide 8: 行动呼吁 ==========
  let slide8 = pres.addSlide();
  slide8.background = { color: COLORS.primary };
  
  // Decorative elements
  slide8.addShape(pres.shapes.OVAL, {
    x: -2, y: -2, w: 6, h: 6,
    fill: { color: COLORS.secondary, transparency: 70 }
  });
  slide8.addShape(pres.shapes.OVAL, {
    x: 7, y: 3, w: 5, h: 5,
    fill: { color: COLORS.accent, transparency: 80 }
  });
  
  slide8.addText("立即行动", {
    x: 0.5, y: 1.5, w: 9, h: 0.8,
    fontSize: 40, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, align: "center"
  });
  
  slide8.addText("2026环博会将是我们展示实力、洞察市场的最佳舞台", {
    x: 0.5, y: 2.5, w: 9, h: 0.6,
    fontSize: 20, fontFace: "Microsoft YaHei",
    color: COLORS.white, align: "center"
  });
  
  // CTA buttons
  slide8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 2.5, y: 3.5, w: 2.2, h: 0.7,
    fill: { color: COLORS.white },
    rectRadius: 0.1
  });
  slide8.addText("准备参展方案", {
    x: 2.5, y: 3.5, w: 2.2, h: 0.7,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.primary, align: "center", valign: "middle"
  });
  
  slide8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 5.3, y: 3.5, w: 2.2, h: 0.7,
    fill: { color: COLORS.accent },
    rectRadius: 0.1
  });
  slide8.addText("细化产品策略", {
    x: 5.3, y: 3.5, w: 2.2, h: 0.7,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.dark, align: "center", valign: "middle"
  });
  
  slide8.addText("IMS产品团队", {
    x: 0.5, y: 4.8, w: 9, h: 0.4,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: COLORS.white, align: "center"
  });

  // Save presentation
  await pres.writeFile({ fileName: "/home/agentuser/IMS产品战略规划_2026环博会.pptx" });
  console.log("PPT created successfully!");
}

createPresentation().catch(console.error);
