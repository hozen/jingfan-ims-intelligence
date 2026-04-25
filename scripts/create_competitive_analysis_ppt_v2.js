const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "IMS竞争分析专家小组";
pres.title = "2026环博会竞争分析报告v2";

// 专家小组角色定义
const EXPERT_PANEL = {
    "战略分析专家": "负责整体竞争格局和战略定位",
    "产品技术专家": "负责产品功能和技术能力分析",
    "市场情报专家": "负责市场趋势和竞争对手动态",
    "商务模式专家": "负责定价策略和商业模式分析"
};

// 颜色系统
const COLORS = {
    "primary": "1A365D",
    "secondary": "2B6CB0",
    "accent": "E53E3E",
    "success": "38A169",
    "warning": "D69E2E",
    "neutral": "718096",
    "light": "EBF8FF",
    "white": "FFFFFF",
    "dark": "1A202C"
};

// =====================
// Slide 1: 封面
// =====================
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.primary };

slide1.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 2.0, w: 10, h: 0.02,
    fill: { color: COLORS.secondary }
});
slide1.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 3.6, w: 10, h: 0.02,
    fill: { color: COLORS.secondary }
});

slide1.addText("IMS竞争分析报告 V2", {
    x: 0.5, y: 2.2, w: 9, h: 0.8,
    fontSize: 36, fontFace: "Arial",
    color: COLORS.white, bold: true, align: "center"
});

slide1.addText("扩展竞争分析：仪表 + 软件平台 + 系统集成商", {
    x: 0.5, y: 2.95, w: 9, h: 0.5,
    fontSize: 18, fontFace: "Arial",
    color: COLORS.light, align: "center"
});

slide1.addText("IMS产品战略规划专家小组", {
    x: 0.5, y: 3.8, w: 9, h: 0.5,
    fontSize: 16, fontFace: "Arial",
    color: COLORS.light, align: "center"
});

slide1.addText("分析日期: 2026年4月18日", {
    x: 0.5, y: 4.5, w: 9, h: 0.4,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.neutral, align: "center"
});

// =====================
// Slide 2: 扩展后的竞争全景
// =====================
let slide2 = pres.addSlide();
slide2.background = { color: COLORS.white };

slide2.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide2.addText("IMS扩展竞争全景：三层竞争威胁", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 三层威胁说明
const layers = [
    {
        title: "第一层：仪表/传感器竞争对手",
        desc: "传统硬件制造商，在传感器和分析仪层面竞争",
        color: COLORS.accent,
        y: 1.0,
        companies: "E+H, ABB, Yokogawa, 聚光科技, 雪迪龙, 力合科技, 先河环保, 科瑞达"
    },
    {
        title: "第二层：软件/平台竞争对手",
        desc: "工业软件和IoT平台厂商，可能取代IMS的软件层面",
        color: COLORS.warning,
        y: 2.3,
        companies: "AVEVA PI/Wonderware, Siemens MindSphere/Xcelerator, PTC ThingWorx, GE Digital, Rockwell"
    },
    {
        title: "第三层：系统集成/云平台竞争对手",
        desc: "智慧水务整体方案商，跨界打劫者",
        color: COLORS.success,
        y: 3.6,
        companies: "阿里云水务大脑, 华为云环境云, 北控水务数字化, 首创环保科技, 腾讯云水务"
    }
];

layers.forEach((layer, i) => {
    slide2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 0.5, y: layer.y, w: 9, h: 1.1,
        fill: { color: "F7FAFC" },
        line: { color: layer.color, width: 2 },
        rectRadius: 0.1
    });
    
    // 层级标签
    slide2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 0.7, y: layer.y + 0.1, w: 0.6, h: 0.35,
        fill: { color: layer.color },
        rectRadius: 0.05
    });
    slide2.addText("L" + (i + 1), {
        x: 0.7, y: layer.y + 0.1, w: 0.6, h: 0.35,
        fontSize: 11, fontFace: "Arial",
        color: COLORS.white, align: "center", valign: "middle", bold: true, margin: 0
    });
    
    slide2.addText(layer.title, {
        x: 1.4, y: layer.y + 0.1, w: 7.5, h: 0.35,
        fontSize: 14, fontFace: "Arial",
        color: COLORS.dark, bold: true, margin: 0
    });
    
    slide2.addText(layer.desc, {
        x: 1.4, y: layer.y + 0.45, w: 7.5, h: 0.3,
        fontSize: 11, fontFace: "Arial",
        color: COLORS.neutral, margin: 0
    });
    
    slide2.addText("代表: " + layer.companies, {
        x: 1.4, y: layer.y + 0.75, w: 7.8, h: 0.3,
        fontSize: 10, fontFace: "Arial",
        color: layer.color, margin: 0
    });
});

// 关键洞察
slide2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 4.9, w: 9, h: 0.6,
    fill: { color: "FEF3C7" },
    rectRadius: 0.1
});
slide2.addText("关键洞察: IMS最大的威胁可能不是仪表同行，而是来自软件平台和云服务商的跨界打劫", {
    x: 0.7, y: 4.9, w: 8.6, h: 0.6,
    fontSize: 12, fontFace: "Arial",
    color: "92400E", bold: true, valign: "middle", margin: 0
});

// =====================
// Slide 3: 第二层 - 软件平台竞争对手
// =====================
let slide3 = pres.addSlide();
slide3.background = { color: COLORS.white };

slide3.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.warning }
});
slide3.addText("第二层竞争对手：工业软件/IoT平台", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 软件平台竞争对手矩阵
const softwarePlayers = [
    {
        name: "AVEVA (剑维软件)",
        products: "PI System, Wonderware InTouch, AVEVA Operations Control",
        strength: "工业实时数据管理和可视化",
        waterFocus: "水务/污水处理",
        threat: "高",
        chinaPresence: "中国团队完善，水务项目多"
    },
    {
        name: "Siemens (Xcelerator)",
        products: "MindSphere, WinCC, COMOS",
        strength: "全生命周期数字化",
        waterFocus: "智慧水务",
        threat: "高",
        chinaPresence: "强大，政府关系好"
    },
    {
        name: "PTC",
        products: "ThingWorx, Vuforia, Kepware",
        strength: "IoT + AR",
        waterFocus: "工业IoT",
        threat: "中",
        chinaPresence: "一般"
    },
    {
        name: "GE Digital",
        products: "Predix, Proficy",
        strength: "工业互联网平台",
        waterFocus: "电力/水务",
        threat: "中",
        chinaPresence: "收缩中"
    },
    {
        name: "Rockwell",
        products: "FTPC, FactoryTalk",
        strength: "SCADA + MES",
        waterFocus: "流程工业",
        threat: "中",
        chinaPresence: "一般"
    },
    {
        name: "AVEVA PI System",
        products: "OSIsoft PI, Asset Framework",
        strength: "时序数据存储分析",
        waterFocus: "电力/石化/制药",
        threat: "高",
        chinaPresence: "强，案例丰富"
    }
];

// 表格
const tableData = [
    ["公司", "核心产品", "优势领域", "水务相关度", "威胁等级"]
];

softwarePlayers.forEach(p => {
    tableData.push([p.name, p.products, p.strength, p.waterFocus, p.threat]);
});

slide3.addTable(tableData, {
    x: 0.3, y: 1.0, w: 9.4,
    fontSize: 9,
    fontFace: "Arial",
    border: { pt: 0.5, color: "CBD5E0" },
    colW: [1.5, 2.5, 2.0, 1.5, 1.0],
    rowH: 0.5,
    color: COLORS.dark,
    valign: "middle"
});

// 威胁说明
slide3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 4.2, w: 9.4, h: 0.6,
    fill: { color: "FFF5F5" },
    rectRadius: 0.1
});
slide3.addText("AVEVA PI System: 威胁最大 - 在水务行业已有大量案例，能采集各类仪表数据并统一展示，可能取代IMS的数据展示层", {
    x: 0.5, y: 4.2, w: 9, h: 0.6,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.accent, valign: "middle", margin: 0
});

// 战略启示
slide3.addText("IMS应对策略", {
    x: 0.3, y: 4.95, w: 9.4, h: 0.35,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});
slide3.addText("不要与这些平台在通用数据管理层面竞争，而要在水文分析+行业专用算法上建立差异化的专业价值", {
    x: 0.3, y: 5.25, w: 9.4, h: 0.35,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.neutral, italic: true, margin: 0
});

// =====================
// Slide 4: 第三层 - 云平台/系统集成商
// =====================
let slide4 = pres.addSlide();
slide4.background = { color: COLORS.white };

slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.success }
});
slide4.addText("第三层竞争对手：云平台 + 系统集成商", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 云平台和系统集成商
const cloudPlayers = [
    {
        category: "云厂商水务方案",
        companies: [
            { name: "阿里云", product: "阿里云水务大脑/环境云", threat: "极高", desc: "ET大脑+IoT+AI能力，可快速构建智慧水务平台" },
            { name: "华为云", product: "华为云环境云", threat: "极高", desc: "FusionPlant工业互联网平台，水务行业解决方案" },
            { name: "腾讯云", product: "腾讯云水务", threat: "高", desc: "微信生态 + 企业微信，水务运营管理" },
            { name: "百度智能云", product: "百度水务AI", threat: "高", desc: "AI算法优势，故障预测和诊断" }
        ]
    },
    {
        category: "水务集团数字化公司",
        companies: [
            { name: "北控水务集团", product: "北控水务数字化", threat: "高", desc: "水务运营经验 + 数字化，但技术整合能力待验证" },
            { name: "首创环保", product: "首创数字科技", threat: "中", desc: "环保板块整合，数字化转型" },
            { name: "中国水务投资", product: "智慧水务平台", threat: "中", desc: "区域水务整合，数字化升级" }
        ]
    },
    {
        category: "系统集成商",
        companies: [
            { name: "启迪环境", product: "智慧环境平台", threat: "中", desc: "环境综合治理方案" },
            { name: "桑德环境", product: "桑德云平台", threat: "中", desc: "固废处理 + 智慧环境" },
            { name: "博天环境", product: "博天水务信息化", threat: "低", desc: "工业水处理专业" }
        ]
    }
];

let yPos = 1.0;
cloudPlayers.forEach((cat, catIdx) => {
    slide4.addText(cat.category, {
        x: 0.3, y: yPos, w: 9.4, h: 0.35,
        fontSize: 12, fontFace: "Arial",
        color: COLORS.primary, bold: true, margin: 0
    });
    yPos += 0.35;
    
    cat.companies.forEach((comp, i) => {
        const xBase = 0.3 + (i % 2) * 4.7;
        const yBase = yPos + Math.floor(i / 2) * 0.85;
        
        slide4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
            x: xBase, y: yBase, w: 4.5, h: 0.75,
            fill: { color: "F7FAFC" },
            line: { color: comp.threat === "极高" || comp.threat === "高" ? COLORS.accent : COLORS.warning, width: 1 },
            rectRadius: 0.08
        });
        
        slide4.addText(comp.name, {
            x: xBase + 0.1, y: yBase + 0.05, w: 1.5, h: 0.3,
            fontSize: 11, fontFace: "Arial",
            color: COLORS.dark, bold: true, margin: 0
        });
        
        slide4.addText(comp.product, {
            x: xBase + 1.6, y: yBase + 0.05, w: 2.8, h: 0.3,
            fontSize: 9, fontFace: "Arial",
            color: COLORS.neutral, margin: 0
        });
        
        slide4.addText(comp.desc, {
            x: xBase + 0.1, y: yBase + 0.38, w: 4.3, h: 0.32,
            fontSize: 9, fontFace: "Arial",
            color: COLORS.dark, margin: 0
        });
    });
    
    yPos += 2.0;
});

// 关键洞察
slide4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 4.85, w: 9.4, h: 0.7,
    fill: { color: "FEF3C7" },
    rectRadius: 0.1
});
slide4.addText("跨界威胁: 阿里云/华为云正在用水务大脑概念拿下智慧水务项目——他们不生产仪表，但能连接所有仪表。这是IMS最需要警惕的威胁模式。", {
    x: 0.5, y: 4.9, w: 9, h: 0.6,
    fontSize: 11, fontFace: "Arial",
    color: "92400E", valign: "middle", margin: 0
});

// =====================
// Slide 5: 三层竞争者对比分析
// =====================
let slide5 = pres.addSlide();
slide5.background = { color: COLORS.white };

slide5.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide5.addText("三层竞争对手综合对比", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 对比表格
const comparisonData = [
    ["维度", "L1: 仪表厂商", "L2: 软件平台", "L3: 云/系统集成"],
    ["核心能力", "传感器/分析仪精度", "数据管理/可视化", "平台整合/AI能力"],
    ["对IMS的威胁点", "硬件参数竞争", "软件层面替代", "整体方案替代"],
    ["IMS的相对优势", "传感器技术积累", "水文分析专业性", "行业Know-how"],
    ["威胁时效性", "即时威胁", "2-3年内", "3-5年后"],
    ["应对策略", "差异化参数", "深耕专业分析", "借力云平台"]
];

slide5.addTable(comparisonData, {
    x: 0.3, y: 1.0, w: 9.4,
    fontSize: 11,
    fontFace: "Arial",
    border: { pt: 1, color: "CBD5E0" },
    colW: [2.0, 2.5, 2.5, 2.4],
    rowH: 0.55,
    color: COLORS.dark,
    valign: "middle"
});

// 竞争优先级矩阵
slide5.addText("竞争优先级矩阵", {
    x: 0.3, y: 4.5, w: 9.4, h: 0.35,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});

// 四个象限
const quadrants = [
    { x: 0.5, y: 4.95, label: "立即应对", companies: "聚光/FPI(价格), AVEVA PI(数据层)", priority: "极高" },
    { x: 2.8, y: 4.95, label: "短期关注", companies: "阿里云/华为云(水务大脑)", priority: "高" },
    { x: 5.1, y: 4.95, label: "中期关注", companies: "Siemens Xcelerator, E+H FieldEdge", priority: "中" },
    { x: 7.4, y: 4.95, label: "长期关注", companies: "北控/首创数字化", priority: "低" }
];

quadrants.forEach(q => {
    slide5.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: q.x, y: q.y, w: 2.2, h: 0.55,
        fill: { color: q.priority === "极高" ? COLORS.accent : q.priority === "高" ? COLORS.warning : q.priority === "中" ? COLORS.secondary : COLORS.neutral },
        rectRadius: 0.08
    });
    slide5.addText(q.label, {
        x: q.x, y: q.y + 0.05, w: 2.2, h: 0.2,
        fontSize: 10, fontFace: "Arial",
        color: COLORS.white, bold: true, align: "center", margin: 0
    });
    slide5.addText(q.companies, {
        x: q.x, y: q.y + 0.28, w: 2.2, h: 0.22,
        fontSize: 7, fontFace: "Arial",
        color: COLORS.white, align: "center", margin: 0
    });
});

// =====================
// Slide 6: E+H深度分析 (扩展版)
// =====================
let slide6 = pres.addSlide();
slide6.background = { color: COLORS.white };

slide6.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide6.addText("E+H 深度分析 (SWOT) - 仪表层最大威胁", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 7.5, y: 0.15, w: 2, h: 0.5,
    fill: { color: "FED7D7" },
    rectRadius: 0.05
});
slide6.addText("环博会未参展", {
    x: 7.5, y: 0.15, w: 2, h: 0.5,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.accent, align: "center", valign: "middle", margin: 0
});

// E+H产品线分析
slide6.addText("E+H核心产品线", {
    x: 0.3, y: 1.0, w: 4.5, h: 0.35,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});

const ehProducts = [
    ["产品类别", "代表产品", "IMS对应竞争"],
    ["数字传感器", "Memosens系列", "直接竞争"],
    ["分析仪表", "Liquiline系列", "高度竞争"],
    ["IIoT平台", "FieldEdge", "替代威胁"],
    ["流量计", "Promass/Promag", "一般竞争"],
    ["液位测量", "Micropilot雷达", "一般竞争"]
];

slide6.addTable(ehProducts, {
    x: 0.3, y: 1.4, w: 4.5,
    fontSize: 9,
    fontFace: "Arial",
    border: { pt: 0.5, color: "CBD5E0" },
    colW: [1.2, 1.8, 1.5],
    rowH: 0.35,
    color: COLORS.dark,
    valign: "middle"
});

// SWOT
const swotData = [
    {
        title: "S 优势",
        color: "38A169",
        items: ["Memosens数字传感器技术成熟", "FieldEdge IIoT平台完善", "传感器生态完整", "全球品牌信任度高"]
    },
    {
        title: "W 劣势",
        color: "E53E3E",
        items: ["价格高 (比国产贵3-5倍)", "中国本土化功能慢", "系统集成能力弱", "非软件原生公司"]
    },
    {
        title: "O 机会",
        color: "3182CE",
        items: ["中国高端工业增长", "订阅制模式可复制", "进口品牌在高端市场受益"]
    },
    {
        title: "T 威胁",
        color: "D69E2E",
        items: ["ABB/Siemens软件整合更强", "国产精度正在追赶", "TCO概念深入人心"]
    }
];

swotData.forEach((quadrant, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 5.1 + col * 2.45;
    const y = 1.0 + row * 1.55;
    
    slide6.addShape(pres.shapes.RECTANGLE, {
        x: x, y: y, w: 2.3, h: 0.35,
        fill: { color: quadrant.color }
    });
    slide6.addText(quadrant.title, {
        x: x + 0.1, y: y, w: 2.1, h: 0.35,
        fontSize: 10, fontFace: "Arial",
        color: COLORS.white, bold: true, valign: "middle", margin: 0
    });
    
    slide6.addShape(pres.shapes.RECTANGLE, {
        x: x, y: y + 0.35, w: 2.3, h: 1.1,
        fill: { color: "F7FAFC" },
        line: { color: quadrant.color, width: 1 }
    });
    
    slide6.addText(
        quadrant.items.map((item, idx) => ({
            text: "• " + item,
            options: { breakLine: idx < quadrant.items.length - 1 }
        })),
        {
            x: x + 0.1, y: y + 0.4, w: 2.1, h: 1.0,
            fontSize: 8, fontFace: "Arial",
            color: COLORS.dark
        }
    );
});

// E+H对IMS的威胁总结
slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 4.3, w: 9.4, h: 0.6,
    fill: { color: "FFF5F5" },
    rectRadius: 0.1
});
slide6.addText("E+H的核心威胁: 不是硬件，而是「传感器+FieldEdge软件订阅」的整体方案——买E+H传感器，送数据管理服务", {
    x: 0.5, y: 4.3, w: 9, h: 0.6,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.accent, bold: true, valign: "middle", margin: 0
});

// 应对策略
slide6.addText("IMS应对策略", {
    x: 0.3, y: 5.0, w: 9.4, h: 0.3,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});
slide6.addText("与E+H避免价格战，聚焦「IMS软件平台+哈希分析传感器」的组合优势，在半导体/制药等高端行业建立差异化", {
    x: 0.3, y: 5.25, w: 9.4, h: 0.3,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.neutral, italic: true, margin: 0
});

// =====================
// Slide 7: AVEVA PI深度分析
// =====================
let slide7 = pres.addSlide();
slide7.background = { color: COLORS.white };

slide7.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.warning }
});
slide7.addText("AVEVA PI System - 软件层最大威胁", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// AVEVA PI介绍
slide7.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 1.0, w: 4.5, h: 2.2,
    fill: { color: COLORS.light },
    rectRadius: 0.1
});

slide7.addText("AVEVA PI System 是什么?", {
    x: 0.5, y: 1.1, w: 4, h: 0.35,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});

slide7.addText([
    { text: "工业实时数据 historian", options: { breakLine: true } },
    { text: "全球应用最广的工业时序数据库", options: { breakLine: true } },
    { text: "可连接任何厂商的仪表和控制系统", options: { breakLine: true } },
    { text: "提供统一的数据展示和分析平台", options: { breakLine: true } },
    { text: "在水务/电力/石化行业有大量案例" }
], {
    x: 0.5, y: 1.5, w: 4, h: 1.6,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.dark
});

// 对IMS的威胁
slide7.addText("对IMS的威胁分析", {
    x: 5.1, y: 1.0, w: 4.5, h: 0.35,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.accent, bold: true, margin: 0
});

const piThreats = [
    { threat: "数据层面替代", desc: "客户可能选择PI System统一管理所有仪表数据，IMS变成数据源之一" },
    { threat: "平台化整合", desc: "AVEVA能连接各类仪表，不依赖特定品牌，IMS被管道化" },
    { threat: "客户议价能力增强", desc: "客户有替代方案后，对IMS的议价能力增强" }
];

piThreats.forEach((t, i) => {
    slide7.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 5.1, y: 1.4 + i * 0.65, w: 4.5, h: 0.55,
        fill: { color: "FFF5F5" },
        line: { color: COLORS.accent, width: 1 },
        rectRadius: 0.08
    });
    slide7.addText(t.threat, {
        x: 5.2, y: 1.45 + i * 0.65, w: 4.3, h: 0.25,
        fontSize: 10, fontFace: "Arial",
        color: COLORS.accent, bold: true, margin: 0
    });
    slide7.addText(t.desc, {
        x: 5.2, y: 1.7 + i * 0.65, w: 4.3, h: 0.25,
        fontSize: 9, fontFace: "Arial",
        color: COLORS.dark, margin: 0
    });
});

// SWOT for AVEVA PI
slide7.addText("AVEVA PI SWOT", {
    x: 0.3, y: 3.4, w: 9.4, h: 0.35,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});

const piSwot = [
    { title: "S优势", color: "38A169", items: ["品牌认可度高", "生态完善", "案例丰富"] },
    { title: "W劣势", color: "E53E3E", items: ["价格昂贵", "非行业专用", "部署复杂"] },
    { title: "O机会", color: "3182CE", items: ["数字化转型", "数据上云需求", "标准制定者"] },
    { title: "T威胁", color: "D69E2E", items: ["开源替代", "云原生平台", "国产化要求"] }
];

piSwot.forEach((q, i) => {
    const x = 0.3 + i * 2.4;
    slide7.addShape(pres.shapes.RECTANGLE, {
        x: x, y: 3.8, w: 2.25, h: 0.3,
        fill: { color: q.color }
    });
    slide7.addText(q.title, {
        x: x + 0.1, y: 3.8, w: 2.0, h: 0.3,
        fontSize: 10, fontFace: "Arial",
        color: COLORS.white, bold: true, valign: "middle", margin: 0
    });
    slide7.addText(
        q.items.map((item, idx) => ({
            text: "• " + item,
            options: { breakLine: idx < q.items.length - 1 }
        })),
        {
            x: x + 0.1, y: 4.15, w: 2.1, h: 0.7,
            fontSize: 9, fontFace: "Arial",
            color: COLORS.dark
        }
    );
});

// IMS应对策略
slide7.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 5.0, w: 9.4, h: 0.55,
    fill: { color: COLORS.primary },
    rectRadius: 0.1
});
slide7.addText("IMS应对策略: 不要与AVEVA PI在通用数据管理层面竞争，要在「IMS专属的水质分析算法+预警模型」上建立不可替代的专业价值", {
    x: 0.5, y: 5.0, w: 9, h: 0.55,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.white, valign: "middle", margin: 0
});

// =====================
// Slide 8: 阿里云/华为云分析
// =====================
let slide8 = pres.addSlide();
slide8.background = { color: COLORS.white };

slide8.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.success }
});
slide8.addText("阿里云 & 华为云 - 跨界打劫者", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 阿里云
slide8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 1.0, w: 4.5, h: 3.0,
    fill: { color: "FFF7ED" },
    line: { color: "EA580C", width: 2 },
    rectRadius: 0.1
});

slide8.addText("阿里云 - 水务大脑", {
    x: 0.5, y: 1.1, w: 4, h: 0.35,
    fontSize: 14, fontFace: "Arial",
    color: "EA580C", bold: true, margin: 0
});

const aliProducts = [
    "ET大脑 - 城市/环境解决方案",
    "阿里云IoT平台 - 设备连接",
    "DataV - 数据可视化",
    "PAI - 机器学习平台",
    "钉钉 - 协同办公集成"
];

slide8.addText(
    aliProducts.map((item, idx) => ({
        text: "• " + item,
        options: { breakLine: idx < aliProducts.length - 1 }
    })),
    {
        x: 0.5, y: 1.5, w: 4, h: 1.5,
        fontSize: 10, fontFace: "Arial",
        color: COLORS.dark
    }
);

slide8.addText("威胁: 极高", {
    x: 0.5, y: 3.0, w: 4, h: 0.3,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.accent, bold: true, margin: 0
});
slide8.addText("模式: 不做仪表，但能连接所有仪表，用平台和AI能力拿走智慧水务项目", {
    x: 0.5, y: 3.3, w: 4, h: 0.6,
    fontSize: 9, fontFace: "Arial",
    color: COLORS.dark, margin: 0
});

// 华为云
slide8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 5.2, y: 1.0, w: 4.5, h: 3.0,
    fill: { color: "F0F9FF" },
    line: { color: "0369A1", width: 2 },
    rectRadius: 0.1
});

slide8.addText("华为云 - 环境云", {
    x: 5.4, y: 1.1, w: 4, h: 0.35,
    fontSize: 14, fontFace: "Arial",
    color: "0369A1", bold: true, margin: 0
});

const huaweiProducts = [
    "FusionPlant - 工业互联网平台",
    "Huawei Cloud IoT - 设备接入",
    "ROMA - 应用集成平台",
    "ModelArts - AI开发平台",
    "WeLink - 企业协同"
];

slide8.addText(
    huaweiProducts.map((item, idx) => ({
        text: "• " + item,
        options: { breakLine: idx < huaweiProducts.length - 1 }
    })),
    {
        x: 5.4, y: 1.5, w: 4, h: 1.5,
        fontSize: 10, fontFace: "Arial",
        color: COLORS.dark
    }
);

slide8.addText("威胁: 极高", {
    x: 5.4, y: 3.0, w: 4, h: 0.3,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.accent, bold: true, margin: 0
});
slide8.addText("模式: ict基础设施+行业解决方案，与水务集团/政府合作，拿下智慧水务项目", {
    x: 5.4, y: 3.3, w: 4, h: 0.6,
    fontSize: 9, fontFace: "Arial",
    color: COLORS.dark, margin: 0
});

// 对比总结
slide8.addText("云厂商 vs IMS: 不同的价值主张", {
    x: 0.3, y: 4.2, w: 9.4, h: 0.35,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});

const comparison = [
    ["维度", "阿里云/华为云", "IMS"],
    ["核心价值", "通用平台 + AI能力", "水文分析 + 专业算法"],
    ["数据来源", "连接所有仪表", "专注于哈希传感器数据"],
    ["客户关系", "ict基础设施", "工艺/运营层面"],
    ["IMS的机会", "与云厂商合作，而非竞争", "成为云平台的专业数据供应商"]
];

slide8.addTable(comparison, {
    x: 0.3, y: 4.6, w: 9.4,
    fontSize: 10,
    fontFace: "Arial",
    border: { pt: 0.5, color: "CBD5E0" },
    colW: [2.0, 3.7, 3.7],
    rowH: 0.35,
    color: COLORS.dark,
    valign: "middle"
});

// =====================
// Slide 9: 综合战略行动方案
// =====================
let slide9 = pres.addSlide();
slide9.background = { color: COLORS.white };

slide9.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide9.addText("IMS战略行动方案 - 三层防御体系", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 三层防御
const defenseLayers = [
    {
        layer: "防御第一层: 硬件差异化",
        focus: "vs 仪表厂商 (E+H, FPI)",
        actions: [
            "深耕哈希传感器技术优势 (精度/稳定性)",
            "开发专属IMS的水质分析算法",
            "针对高端工业客户(半导体/制药)定制方案",
            "建立哈希在特定参数上的技术壁垒"
        ],
        timeline: "立即开始，持续"
    },
    {
        layer: "防御第二层: 软件护城河",
        focus: "vs 软件平台 (AVEVA PI, Siemens)",
        actions: [
            "开发IMS专属的行业分析模块",
            "建立「IMS数据+专业算法」的不可替代性",
            "与AVEVA等平台合作而非竞争",
            "突出IMS在水质预警/异常检测的专业性"
        ],
        timeline: "90天内启动软件平台选型"
    },
    {
        layer: "防御第三层: 生态位占领",
        focus: "vs 云厂商 (阿里云/华为云)",
        actions: [
            "将IMS定位为云平台的「专业水质数据供应商」",
            "开发IMS与主流云平台的接口/集成",
            "建立「哈希云+IMS」联合方案",
            "在智慧水务项目中找到IMS的专属位置"
        ],
        timeline: "6个月内完成云集成方案"
    }
];

defenseLayers.forEach((d, i) => {
    const y = 1.0 + i * 1.45;
    
    slide9.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 0.3, y: y, w: 9.4, h: 1.35,
        fill: { color: "F7FAFC" },
        line: { color: COLORS.primary, width: 1 },
        rectRadius: 0.1
    });
    
    slide9.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 0.5, y: y + 0.1, w: 0.5, h: 0.35,
        fill: { color: COLORS.primary },
        rectRadius: 0.05
    });
    slide9.addText("L" + (i + 1), {
        x: 0.5, y: y + 0.1, w: 0.5, h: 0.35,
        fontSize: 11, fontFace: "Arial",
        color: COLORS.white, bold: true, align: "center", valign: "middle", margin: 0
    });
    
    slide9.addText(d.layer, {
        x: 1.1, y: y + 0.1, w: 6, h: 0.35,
        fontSize: 13, fontFace: "Arial",
        color: COLORS.primary, bold: true, margin: 0
    });
    
    slide9.addText(d.focus, {
        x: 7.2, y: y + 0.1, w: 2.3, h: 0.35,
        fontSize: 10, fontFace: "Arial",
        color: COLORS.neutral, margin: 0
    });
    
    slide9.addText(
        d.actions.map((a, idx) => ({
            text: "• " + a,
            options: { breakLine: idx < d.actions.length - 1 }
        })),
        {
            x: 0.5, y: y + 0.5, w: 7, h: 0.8,
            fontSize: 9, fontFace: "Arial",
            color: COLORS.dark
        }
    );
    
    slide9.addText(d.timeline, {
        x: 7.5, y: y + 0.5, w: 2, h: 0.4,
        fontSize: 9, fontFace: "Arial",
        color: COLORS.warning, bold: true, margin: 0
    });
});

// =====================
// Slide 10: 总结
// =====================
let slide10 = pres.addSlide();
slide10.background = { color: COLORS.primary };

slide10.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 1.8, w: 10, h: 0.02,
    fill: { color: COLORS.secondary }
});

slide10.addText("专家小组核心结论 V2", {
    x: 0.5, y: 0.8, w: 9, h: 0.8,
    fontSize: 32, fontFace: "Arial",
    color: COLORS.white, bold: true, align: "center"
});

slide10.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 2.0, w: 10, h: 0.02,
    fill: { color: COLORS.secondary }
});

// 四个核心结论
const conclusions = [
    { num: "1", text: "IMS面临三层竞争威胁，仪表只是第一层，软件平台和云厂商是更危险的跨界打劫者" },
    { num: "2", text: "AVEVA PI System是软件层最大威胁，IMS必须建立「水文分析专业算法」的不可替代价值" },
    { num: "3", text: "阿里云/华为云用平台思维做水务，IMS应借力而非硬抗，成为其专业数据供应商" },
    { num: "4", text: "90天内必须完成软件平台选型，否则在「数据管理层面」被替代的风险将变成现实" }
];

conclusions.forEach((c, i) => {
    slide10.addShape(pres.shapes.OVAL, {
        x: 0.8, y: 2.3 + i * 0.75, w: 0.4, h: 0.4,
        fill: { color: COLORS.secondary }
    });
    slide10.addText(c.num, {
        x: 0.8, y: 2.3 + i * 0.75, w: 0.4, h: 0.4,
        fontSize: 14, fontFace: "Arial",
        color: COLORS.white, bold: true, align: "center", valign: "middle", margin: 0
    });
    
    slide10.addText(c.text, {
        x: 1.4, y: 2.3 + i * 0.75, w: 8, h: 0.5,
        fontSize: 14, fontFace: "Arial",
        color: COLORS.light, valign: "middle"
    });
});

slide10.addText("—— IMS战略规划专家小组 V2", {
    x: 0.5, y: 5.0, w: 9, h: 0.4,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.neutral, align: "center", italic: true
});

// 保存
pres.writeFile({ fileName: "/home/agentuser/IMS竞争分析报告v2_扩展版.pptx" })
    .then(() => console.log("PPT V2 created successfully"))
    .catch(err => console.error("Error:", err));
