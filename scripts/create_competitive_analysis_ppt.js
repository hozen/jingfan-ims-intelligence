const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "IMS竞争分析专家小组";
pres.title = "2026环博会竞争分析报告";

// 专家小组角色定义
const EXPERT_PANEL = {
    "战略分析专家": "负责整体竞争格局和战略定位",
    "产品技术专家": "负责产品功能和技术能力分析",
    "市场情报专家": "负责市场趋势和竞争对手动态",
    "商务模式专家": "负责定价策略和商业模式分析"
};

// 颜色系统 - 专业商务蓝
const COLORS = {
    "primary": "1A365D",      // 深海军蓝
    "secondary": "2B6CB0",    // 商务蓝
    "accent": "E53E3E",       // 警示红
    "success": "38A169",      // 增长绿
    "warning": "D69E2E",      // 预警黄
    "neutral": "718096",      // 中性灰
    "light": "EBF8FF",        // 浅蓝背景
    "white": "FFFFFF",
    "dark": "1A202C"
};

// =====================
// Slide 1: 封面
// =====================
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.primary };

// 装饰线条
slide1.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 2.2, w: 10, h: 0.02,
    fill: { color: COLORS.secondary }
});
slide1.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 3.8, w: 10, h: 0.02,
    fill: { color: COLORS.secondary }
});

slide1.addText("2026环博会竞争分析报告", {
    x: 0.5, y: 2.4, w: 9, h: 1.2,
    fontSize: 40, fontFace: "Arial",
    color: COLORS.white, bold: true, align: "center"
});

slide1.addText("IMS产品战略规划专家小组", {
    x: 0.5, y: 4.0, w: 9, h: 0.5,
    fontSize: 20, fontFace: "Arial",
    color: COLORS.light, align: "center"
});

slide1.addText("分析日期: 2026年4月18日  |  保密级别: 内部使用", {
    x: 0.5, y: 4.8, w: 9, h: 0.4,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.neutral, align: "center"
});

// =====================
// Slide 2: 分析框架说明
// =====================
let slide2 = pres.addSlide();
slide2.background = { color: COLORS.white };

// 顶部色带
slide2.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide2.addText("分析框架与方法论", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 四个专家角色卡片
const experts = [
    { role: "战略分析专家", focus: "竞争格局与战略定位", framework: "波特五力 + 价值链分析" },
    { role: "产品技术专家", focus: "产品功能与技术能力", framework: "功能对比矩阵 + 技术成熟度" },
    { role: "市场情报专家", focus: "市场趋势与竞争动态", framework: "SWOT + 趋势外推" },
    { role: "商务模式专家", focus: "定价策略与商业模式", framework: "LTV/CAC + 订阅制分析" }
];

experts.forEach((exp, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.8;
    const y = 1.2 + row * 2.0;
    
    // 卡片背景
    slide2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: x, y: y, w: 4.5, h: 1.7,
        fill: { color: COLORS.light },
        rectRadius: 0.1
    });
    
    // 角色名称
    slide2.addText(exp.role, {
        x: x + 0.2, y: y + 0.15, w: 4, h: 0.4,
        fontSize: 16, fontFace: "Arial",
        color: COLORS.primary, bold: true, margin: 0
    });
    
    // 关注领域
    slide2.addText("关注: " + exp.focus, {
        x: x + 0.2, y: y + 0.55, w: 4, h: 0.35,
        fontSize: 12, fontFace: "Arial",
        color: COLORS.dark, margin: 0
    });
    
    // 使用框架
    slide2.addText("框架: " + exp.framework, {
        x: x + 0.2, y: y + 0.95, w: 4, h: 0.35,
        fontSize: 11, fontFace: "Arial",
        color: COLORS.neutral, margin: 0
    });
});

slide2.addText("本报告综合四位专家的分析视角，确保竞争情报的全面性和战略建议的可操作性", {
    x: 0.5, y: 5.0, w: 9, h: 0.4,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.neutral, align: "center", italic: true
});

// =====================
// Slide 3: 环博会参展商全景
// =====================
let slide3 = pres.addSlide();
slide3.background = { color: COLORS.white };

slide3.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide3.addText("2026环博会水质监测参展商全景", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 重要发现标注
slide3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.0, w: 9, h: 0.7,
    fill: { color: "FEF3C7" },
    rectRadius: 0.05
});
slide3.addText("⚠ 重要发现: E+H (Endress+Hauser) 未出现在本届环博会参展商名单中", {
    x: 0.7, y: 1.15, w: 8.5, h: 0.4,
    fontSize: 14, fontFace: "Arial",
    color: "92400E", bold: true, margin: 0
});

// 参展商分类表格
const exhibitors = [
    ["类别", "公司名称", "核心产品", "目标市场"],
    ["国际巨头", "ABB", "Ability™ 工业物联网平台", "高端工业、跨国企业"],
    ["国际巨头", "Siemens", "MindSphere / Xcelerator", "工业4.0、政府基础设施"],
    ["国际巨头", "Yokogawa", "Aqualink™ 水质监测系统", "石化、电力、高端水处理"],
    ["国内一线", "聚光科技 FPI", "在线监测仪 + 智慧水务平台", "市政水务、污水处理"],
    ["国内一线", "雪迪龙 Skyray", "环境监测系统", "环保部门、污染源监测"],
    ["国内一线", "力合科技", "水质自动监测站", "市政、水利"],
    ["国内新锐", "先河环保", "网格化监测系统", "政府采购"],
    ["国内新锐", "科瑞达", "水质分析仪器", "工业用户"]
];

slide3.addTable(exhibitors, {
    x: 0.3, y: 1.9, w: 9.4,
    fontSize: 10,
    fontFace: "Arial",
    border: { pt: 0.5, color: "CBD5E0" },
    colW: [1.2, 1.8, 3.2, 3.2],
    rowH: 0.4,
    color: COLORS.dark,
    valign: "middle"
});

// 分类标签
slide3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 5.0, w: 1.2, h: 0.35,
    fill: { color: COLORS.accent },
    rectRadius: 0.05
});
slide3.addText("高威胁", {
    x: 0.5, y: 5.0, w: 1.2, h: 0.35,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.white, align: "center", valign: "middle", margin: 0
});

slide3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 1.8, y: 5.0, w: 1.2, h: 0.35,
    fill: { color: COLORS.warning },
    rectRadius: 0.05
});
slide3.addText("中威胁", {
    x: 1.8, y: 5.0, w: 1.2, h: 0.35,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.white, align: "center", valign: "middle", margin: 0
});

slide3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 3.1, y: 5.0, w: 1.2, h: 0.35,
    fill: { color: COLORS.success },
    rectRadius: 0.05
});
slide3.addText("低威胁", {
    x: 3.1, y: 5.0, w: 1.2, h: 0.35,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.white, align: "center", valign: "middle", margin: 0
});

// =====================
// Slide 4: E+H 深度分析 (SWOT)
// =====================
let slide4 = pres.addSlide();
slide4.background = { color: COLORS.white };

slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide4.addText("E+H (Endress+Hauser) 深度分析", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 标注E+H未参展
slide4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 6.5, y: 0.15, w: 3, h: 0.5,
    fill: { color: "FED7D7" },
    rectRadius: 0.05
});
slide4.addText("本届环博会未参展", {
    x: 6.5, y: 0.15, w: 3, h: 0.5,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.accent, align: "center", valign: "middle", margin: 0
});

// SWOT框架 - 2x2布局
const swotData = [
    {
        title: "S 优势 Strengths",
        color: "38A169",
        items: [
            "Memosens数字传感器技术 - 传感器内置自诊断和校准数据",
            "FieldEdge IIoT平台 - 远程设备管理和诊断",
            "完整的仪表生态系统 - 流量、液位、压力、分析全覆盖",
            "Heartbeat Technology - 预测性维护能力"
        ]
    },
    {
        title: "W 劣势 Weaknesses",
        color: "E53E3E",
        items: [
            "价格比国产贵3-5倍",
            "中国本土化功能响应慢 (微信/钉钉)",
            "系统集成能力弱 - 不如ABB/西门子",
            "软件平台非核心业务"
        ]
    },
    {
        title: "O 机会 Opportunities",
        color: "3182CE",
        items: [
            "中国高端工业市场持续增长",
            "传感器+软件订阅模式可复制",
            "国产替代背景下进口品牌反而受益",
            "石化/制药等行业对品质要求提升"
        ]
    },
    {
        title: "T 威胁 Threats",
        color: "D69E2E",
        items: [
            "ABB/Siemens软件平台整合能力更强",
            "国产仪表精度正在追赶",
            "贸易摩擦可能影响供应链",
            "客户越来越注重总体拥有成本(TCO)"
        ]
    }
];

swotData.forEach((quadrant, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.3 + col * 4.85;
    const y = 1.0 + row * 2.25;
    
    // 标题栏
    slide4.addShape(pres.shapes.RECTANGLE, {
        x: x, y: y, w: 4.65, h: 0.4,
        fill: { color: quadrant.color }
    });
    slide4.addText(quadrant.title, {
        x: x + 0.1, y: y, w: 4.4, h: 0.4,
        fontSize: 12, fontFace: "Arial",
        color: COLORS.white, bold: true, valign: "middle", margin: 0
    });
    
    // 内容区
    slide4.addShape(pres.shapes.RECTANGLE, {
        x: x, y: y + 0.4, w: 4.65, h: 1.7,
        fill: { color: "F7FAFC" },
        line: { color: quadrant.color, width: 1 }
    });
    
    // 要点列表
    slide4.addText(
        quadrant.items.map((item, idx) => ({
            text: item,
            options: { bullet: true, breakLine: idx < quadrant.items.length - 1 }
        })),
        {
            x: x + 0.1, y: y + 0.5, w: 4.4, h: 1.5,
            fontSize: 9, fontFace: "Arial",
            color: COLORS.dark, valign: "top"
        }
    );
});

// 战略启示
slide4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 5.1, w: 9.4, h: 0.45,
    fill: { color: COLORS.primary }
});
slide4.addText("战略启示: E+H的「传感器+软件」模式是IMS最大的威胁。即使E+H未参展环博会，其商业模式值得高度关注", {
    x: 0.5, y: 5.1, w: 9, h: 0.45,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.white, valign: "middle", margin: 0
});

// =====================
// Slide 5: 聚光科技 FPI 分析
// =====================
let slide5 = pres.addSlide();
slide5.background = { color: COLORS.white };

slide5.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide5.addText("国内劲敌: 聚光科技 (FPI)", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 公司概览
slide5.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 1.0, w: 4.5, h: 2.4,
    fill: { color: COLORS.light },
    rectRadius: 0.1
});

slide5.addText("公司概览", {
    x: 0.5, y: 1.1, w: 4, h: 0.35,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});

const fpiOverview = [
    ["总部", "杭州"],
    ["成立", "2002年"],
    ["上市", "深交所创业板"],
    ["定位", "高端仪器+解决方案"],
    ["优势", "国产分析仪领导者"],
    ["弱点", "软件平台相对薄弱"]
];

slide5.addTable(fpiOverview, {
    x: 0.5, y: 1.5, w: 4, h: 1.8,
    fontSize: 10,
    fontFace: "Arial",
    colW: [1.2, 2.8],
    rowH: 0.3,
    color: COLORS.dark,
    border: { pt: 0 },
    valign: "middle"
});

// 产品能力分析
slide5.addText("产品能力矩阵", {
    x: 5.0, y: 1.0, w: 4.5, h: 0.35,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});

const fpiProducts = [
    ["产品线", "能力评级", "备注"],
    ["水质在线监测", "★★★★☆", "COD/氨氮/总磷等"],
    ["挥发性有机物", "★★★★★", "国内领先"],
    ["智慧水务平台", "★★★☆☆", "集成能力待提升"],
    ["传感器技术", "★★★☆☆", "核心件依赖进口"],
    ["软件平台", "★★★☆☆", "功能较基础"]
];

slide5.addTable(fpiProducts, {
    x: 5.0, y: 1.4, w: 4.5,
    fontSize: 10,
    fontFace: "Arial",
    colW: [1.8, 1.2, 1.5],
    rowH: 0.35,
    border: { pt: 0.5, color: "CBD5E0" },
    color: COLORS.dark,
    valign: "middle"
});

// 威胁评估
slide5.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 3.6, w: 9.4, h: 1.0,
    fill: { color: "FEF3C7" },
    rectRadius: 0.1
});

slide5.addText("威胁评估: 聚光科技对哈希IMS的威胁程度", {
    x: 0.5, y: 3.7, w: 9, h: 0.35,
    fontSize: 12, fontFace: "Arial",
    color: "92400E", bold: true, margin: 0
});

slide5.addText([
    { text: "• 市政项目: ", options: { bold: true } },
    { text: "高威胁 - 价格低30-50%, 政府关系好", options: { breakLine: true } },
    { text: "• 高端工业: ", options: { bold: true } },
    { text: "中威胁 - VOC分析有优势, 但水质全参数能力不及哈希", options: { breakLine: true } },
    { text: "• 软件平台: ", options: { bold: true } },
    { text: "低威胁 - FPI软件能力弱, 这是IMS的差异化机会" }
], {
    x: 0.5, y: 4.05, w: 9, h: 0.5,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.dark
});

// 竞争策略
slide5.addText("IMS应对策略", {
    x: 0.3, y: 4.8, w: 9.4, h: 0.35,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.primary, bold: true, margin: 0
});

slide5.addText("不要在市政项目上与FPI价格战，而是在高端工业客户（半导体/制药）和软件平台能力上建立护城河", {
    x: 0.3, y: 5.1, w: 9.4, h: 0.4,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.neutral, italic: true, margin: 0
});

// =====================
// Slide 6: 波特五力分析
// =====================
let slide6 = pres.addSlide();
slide6.background = { color: COLORS.white };

slide6.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide6.addText("竞争环境分析: 波特五力模型", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 五力分析图示 - 中心圆
slide6.addShape(pres.shapes.OVAL, {
    x: 4, y: 2.3, w: 2, h: 2,
    fill: { color: COLORS.primary }
});
slide6.addText("IMS\n竞争强度", {
    x: 4, y: 2.8, w: 2, h: 1,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.white, bold: true, align: "center", valign: "middle", margin: 0
});

// 五个力量
const forces = [
    { 
        label: "供应商议价能力", 
        x: 4.2, y: 1.0, 
        threat: "中", 
        color: COLORS.warning,
        items: ["传感器核心部件供应商集中", "E+H垂直整合威胁"]
    },
    { 
        label: "买方议价能力", 
        x: 6.5, y: 2.5, 
        threat: "高", 
        color: COLORS.accent,
        items: ["大客户有议价能力", "市政项目招标压价"]
    },
    { 
        label: "新进入者威胁", 
        x: 4.2, y: 4.5, 
        threat: "高", 
        color: COLORS.accent,
        items: ["华为/阿里等跨界玩家", "软件公司切入硬件"]
    },
    { 
        label: "替代品威胁", 
        x: 1.5, y: 2.5, 
        threat: "中", 
        color: COLORS.warning,
        items: ["便携式监测设备", "无人机监测方案"]
    },
    { 
        label: "行业内竞争", 
        x: 0.5, y: 1.5, 
        threat: "高", 
        color: COLORS.accent,
        items: ["国产替代加速", "价格战苗头初现"]
    }
];

forces.forEach((force, i) => {
    // 标签框
    slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: force.x, y: force.y, w: 2.8, h: 1.5,
        fill: { color: "F7FAFC" },
        line: { color: force.color, width: 2 },
        rectRadius: 0.1
    });
    
    // 威胁等级
    slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: force.x + 1.9, y: force.y + 0.1, w: 0.8, h: 0.35,
        fill: { color: force.color },
        rectRadius: 0.05
    });
    slide6.addText(force.threat, {
        x: force.x + 1.9, y: force.y + 0.1, w: 0.8, h: 0.35,
        fontSize: 10, fontFace: "Arial",
        color: COLORS.white, align: "center", valign: "middle", bold: true, margin: 0
    });
    
    // 标题
    slide6.addText(force.label, {
        x: force.x + 0.1, y: force.y + 0.1, w: 1.7, h: 0.35,
        fontSize: 10, fontFace: "Arial",
        color: COLORS.primary, bold: true, margin: 0
    });
    
    // 要点
    slide6.addText(
        force.items.map((item, idx) => ({
            text: "• " + item,
            options: { breakLine: idx < force.items.length - 1 }
        })),
        {
            x: force.x + 0.1, y: force.y + 0.5, w: 2.6, h: 0.9,
            fontSize: 8, fontFace: "Arial",
            color: COLORS.dark
        }
    );
});

// 结论
slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 5.0, w: 9.4, h: 0.55,
    fill: { color: COLORS.light },
    rectRadius: 0.1
});
slide6.addText("结论: 水质监测行业竞争强度高且上升，IMS需要在软件平台和高价值客户两个维度建立护城河", {
    x: 0.5, y: 5.0, w: 9, h: 0.55,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.primary, valign: "middle", margin: 0
});

// =====================
// Slide 7: 竞争定位矩阵
// =====================
let slide7 = pres.addSlide();
slide7.background = { color: COLORS.white };

slide7.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide7.addText("竞争定位矩阵: 技术实力 vs 市场覆盖", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// 坐标轴
slide7.addShape(pres.shapes.LINE, {
    x: 1.5, y: 1.2, w: 0, h: 3.8,
    line: { color: COLORS.neutral, width: 1 }
});
slide7.addShape(pres.shapes.LINE, {
    x: 1.5, y: 5.0, w: 7.5, h: 0,
    line: { color: COLORS.neutral, width: 1 }
});

// 轴标签
slide7.addText("技术实力", {
    x: 0.3, y: 2.8, w: 1, h: 0.5,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.neutral, rotate: 270, align: "center", margin: 0
});
slide7.addText("市场覆盖范围", {
    x: 4.5, y: 5.1, w: 2, h: 0.4,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.neutral, align: "center", margin: 0
});

// 轴刻度
slide7.addText("高", {
    x: 0.3, y: 1.3, w: 0.5, h: 0.3,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.neutral, align: "center", margin: 0
});
slide7.addText("低", {
    x: 0.3, y: 4.5, w: 0.5, h: 0.3,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.neutral, align: "center", margin: 0
});
slide7.addText("国内", {
    x: 1.6, y: 5.1, w: 0.8, h: 0.4,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.neutral, align: "center", margin: 0
});
slide7.addText("全球", {
    x: 8.5, y: 5.1, w: 0.8, h: 0.4,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.neutral, align: "center", margin: 0
});

// 竞争对手位置
const competitors = [
    { name: "ABB", x: 7.5, y: 1.8, color: COLORS.secondary },
    { name: "Siemens", x: 8.0, y: 2.0, color: COLORS.secondary },
    { name: "E+H", x: 6.5, y: 2.3, color: COLORS.secondary },
    { name: "Yokogawa", x: 7.0, y: 2.5, color: COLORS.secondary },
    { name: "哈希 IMS", x: 5.5, y: 2.8, color: COLORS.accent },
    { name: "聚光科技", x: 3.5, y: 3.5, color: COLORS.warning },
    { name: "雪迪龙", x: 2.8, y: 3.8, color: COLORS.warning },
    { name: "力合科技", x: 2.5, y: 4.0, color: COLORS.success },
    { name: "先河环保", x: 2.2, y: 4.3, color: COLORS.success }
];

competitors.forEach(comp => {
    // 圆点
    slide7.addShape(pres.shapes.OVAL, {
        x: comp.x, y: comp.y, w: 0.35, h: 0.35,
        fill: { color: comp.color }
    });
    // 标签
    slide9_offset = comp.name === "哈希 IMS" ? 0 : 0;
    slide7.addText(comp.name, {
        x: comp.x + 0.4, y: comp.y, w: 1.2, h: 0.35,
        fontSize: 9, fontFace: "Arial",
        color: comp.color === COLORS.accent ? COLORS.accent : COLORS.dark,
        bold: comp.name === "哈希 IMS",
        valign: "middle", margin: 0
    });
});

// 象限标签
slide7.addText("高端工业", {
    x: 6.5, y: 4.7, w: 2, h: 0.3,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.secondary, align: "center", margin: 0
});
slide7.addText("市政水务", {
    x: 2.5, y: 4.7, w: 2, h: 0.3,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.warning, align: "center", margin: 0
});

// =====================
// Slide 8: 综合SWOT + 行动方案
// =====================
let slide8 = pres.addSlide();
slide8.background = { color: COLORS.white };

slide8.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.primary }
});
slide8.addText("IMS综合SWOT与战略行动方案", {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});

// SWOT汇总
const swotSummary = [
    { title: "优势 S", color: "38A169", items: ["哈希品牌在高端客户中的信任度", "传感器技术积累深厚", "Veralto集团资源支持"] },
    { title: "劣势 W", color: "E53E3E", items: ["软件平台能力薄弱", "本土化功能响应慢", "价格竞争力不足"] },
    { title: "机会 O", color: "3182CE", items: ["高端工业(半导体/制药)需求增长", "智慧水务平台整合需求", "订阅制商业模式转型机会"] },
    { title: "威胁 T", color: "D69E2E", items: ["国产替代加速", "E+H软件模式降维打击", "跨界玩家切入"] }
];

swotSummary.forEach((item, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.3 + col * 4.85;
    const y = 1.0 + row * 1.15;
    
    slide8.addShape(pres.shapes.RECTANGLE, {
        x: x, y: y, w: 4.65, h: 0.35,
        fill: { color: item.color }
    });
    slide8.addText(item.title, {
        x: x + 0.1, y: y, w: 4.4, h: 0.35,
        fontSize: 11, fontFace: "Arial",
        color: COLORS.white, bold: true, valign: "middle", margin: 0
    });
    
    slide8.addText(
        item.items.map((t, idx) => ({
            text: "• " + t,
            options: { breakLine: idx < item.items.length - 1 }
        })),
        {
            x: x + 0.1, y: y + 0.4, w: 4.4, h: 0.7,
            fontSize: 9, fontFace: "Arial",
            color: COLORS.dark
        }
    );
});

// SO战略
slide8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 3.4, w: 4.65, h: 1.1,
    fill: { color: "E6FFFA" },
    line: { color: "38A169", width: 2 },
    rectRadius: 0.1
});
slide8.addText("SO战略 (增长)", {
    x: 0.4, y: 3.5, w: 4.4, h: 0.3,
    fontSize: 11, fontFace: "Arial",
    color: "276749", bold: true, margin: 0
});
slide8.addText("聚焦高端工业客户，用IMS软件平台+哈希传感器的组合优势，拿下半导体、制药、新能源行业订单", {
    x: 0.4, y: 3.85, w: 4.4, h: 0.6,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.dark, margin: 0
});

// WT战略
slide8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 5.15, y: 3.4, w: 4.65, h: 1.1,
    fill: { color: "FFF5F5" },
    line: { color: "E53E3E", width: 2 },
    rectRadius: 0.1
});
slide8.addText("WT战略 (防御)", {
    x: 5.25, y: 3.5, w: 4.4, h: 0.3,
    fontSize: 11, fontFace: "Arial",
    color: "C53030", bold: true, margin: 0
});
slide8.addText("补齐软件短板，90天内完成FieldEdge对标物选型; 本土化功能优先级排序，2周内启动开发", {
    x: 5.25, y: 3.85, w: 4.4, h: 0.6,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.dark, margin: 0
});

// 立即行动
slide8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 4.7, w: 9.4, h: 0.85,
    fill: { color: COLORS.primary },
    rectRadius: 0.1
});
slide8.addText("90天内的三项关键行动", {
    x: 0.5, y: 4.8, w: 9, h: 0.3,
    fontSize: 12, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
});
slide8.addText("① 72小时内: 展会客户个性化跟进  |  ② 30天内: 本土化功能开发启动  |  ③ 90天内: 软件平台选型完成", {
    x: 0.5, y: 5.1, w: 9, h: 0.35,
    fontSize: 11, fontFace: "Arial",
    color: COLORS.light, margin: 0
});

// =====================
// Slide 9: 总结与下一步
// =====================
let slide9 = pres.addSlide();
slide9.background = { color: COLORS.primary };

slide9.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 2.0, w: 10, h: 0.02,
    fill: { color: COLORS.secondary }
});

slide9.addText("专家小组核心结论", {
    x: 0.5, y: 0.8, w: 9, h: 0.8,
    fontSize: 32, fontFace: "Arial",
    color: COLORS.white, bold: true, align: "center"
});

slide9.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 2.2, w: 10, h: 0.02,
    fill: { color: COLORS.secondary }
});

// 三个核心结论
const conclusions = [
    "1. E+H虽未参展，但其「传感器+软件订阅」模式是IMS最需要警惕的威胁",
    "2. 国产竞争对手在市政市场已形成规模，IMS的护城河在高端工业 + 软件能力",
    "3. 90天内必须完成软件平台选型和本土化功能开发，否则差距将进一步拉大"
];

conclusions.forEach((text, i) => {
    slide9.addText(text, {
        x: 0.8, y: 2.5 + i * 0.7, w: 8.4, h: 0.6,
        fontSize: 16, fontFace: "Arial",
        color: COLORS.light, valign: "middle"
    });
});

slide9.addText("—— IMS战略规划专家小组", {
    x: 0.5, y: 4.8, w: 9, h: 0.4,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.neutral, align: "center", italic: true
});

// 保存文件
pres.writeFile({ fileName: "/home/agentuser/IMS竞争分析报告_环博会_专家小组.pptx" })
    .then(() => console.log("PPT created successfully"))
    .catch(err => console.error("Error:", err));
