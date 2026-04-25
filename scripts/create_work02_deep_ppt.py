#!/usr/bin/env python3
"""Work-02 Deep Research PPT — 中国水协2026年会深度市场研究"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree
import copy

PYTHON = "/tmp/ocr_env/bin/python"
OUTPUT = "/home/agentuser/Work-02_中国水协2026年会_深度版.pptx"

BLUE = RGBColor(0, 126, 181)
DARK = RGBColor(77, 77, 77)
LIGHT = RGBColor(153, 153, 153)
WHITE = RGBColor(255, 255, 255)

def add_textbox(slide, left, top, width, height, texts, font_sizes, colors=None, bold=False, align=PP_ALIGN.LEFT):
    """Add a textbox with multiple paragraphs."""
    from pptx.util import Pt
    from pptx.dml.color import RGBColor
    
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    
    for i, text in enumerate(texts):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = text
        run.font.name = "Microsoft YaHei"
        fs = font_sizes[i] if i < len(font_sizes) else font_sizes[-1]
        run.font.size = Pt(fs)
        run.font.bold = bold if isinstance(bold, bool) else (bold[i] if i < len(bold) else False)
        clr = colors[i] if colors and i < len(colors) else DARK
        run.font.color.rgb = clr
    return txBox

def blue_bar(slide, height=Inches(0.08)):
    """Add a thin blue bar at top."""
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    bar = slide.shapes.add_shape(1, 0, 0, Inches(13.33), height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

def section_num(slide, num):
    """Add a large section number."""
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(1), Inches(0.8))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = num
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = BLUE
    run.font.name = "Microsoft YaHei"

def divider_slide(prs, section_title, section_num_text):
    """Create a divider slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    bar = slide.shapes.add_shape(1, 0, 0, Inches(13.33), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()
    
    txBox = slide.shapes.add_textbox(Inches(0.6), Inches(2.6), Inches(4), Inches(1.2))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = section_num_text
    run.font.size = Pt(80)
    run.font.bold = True
    run.font.color.rgb = BLUE
    run.font.name = "Microsoft YaHei"
    
    txBox2 = slide.shapes.add_textbox(Inches(0.6), Inches(3.8), Inches(11), Inches(1.2))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    run2 = p2.add_run()
    run2.text = section_title
    run2.font.size = Pt(32)
    run2.font.color.rgb = DARK
    run2.font.name = "Microsoft YaHei"

def bullet_table(slide, left, top, width, height, headers, rows, col_widths=None):
    """Add a simple table."""
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.oxml.ns import qn
    
    rows_count = len(rows) + 1  # +1 for header
    cols_count = len(headers)
    
    table = slide.shapes.add_table(rows_count, cols_count, left, top, width, height).table
    
    # Set column widths
    if col_widths:
        for ci, cw in enumerate(col_widths):
            table.columns[ci].width = cw
    
    # Header row
    for ci, h in enumerate(headers):
        cell = table.cell(0, ci)
        cell.text = h
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = "Microsoft YaHei"
        p.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLUE
    
    # Data rows
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = table.cell(ri + 1, ci)
            cell.text = str(val)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.name = "Microsoft YaHei"
            p.font.color.rgb = DARK
            if ci == 0:
                p.font.bold = True
    
    return table

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # ─── SLIDE 1: Cover ──────────────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide, Inches(0.12))
    
    add_textbox(slide, Inches(0.6), Inches(1.8), Inches(12), Inches(1.2),
                ["中国水协2026年会", "深度市场研究报告"],
                [44, 28], [DARK, DARK], [True, False])
    
    add_textbox(slide, Inches(0.6), Inches(3.1), Inches(8), Inches(0.6),
                ["2026年4月15-19日 · 深圳国际会展中心"],
                [18], [LIGHT])
    
    add_textbox(slide, Inches(0.6), Inches(3.8), Inches(10), Inches(0.5),
                ["数据来源：百度搜索（4月21-22日） + 媒体报道汇总 | Hach中国IMS产品线"],
                [13], [LIGHT])
    
    # Source note at bottom
    add_textbox(slide, Inches(0.6), Inches(6.5), Inches(12), Inches(0.5),
                ["研究框架类比Work-01环博会报告 · 覆盖：政策信号 / AI落地 / 竞争格局 / Hach机会"],
                [12], [LIGHT])
    
    # ─── SLIDE 2: 执行摘要 ─────────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide)
    section_num(slide, "00")
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(8), Inches(0.6),
                ["执行摘要"], [22], [DARK], [True])
    
    bullets = [
        "① AI+水务已从概念进入落地：深圳「深水云脑2.0」99%数字化覆盖，运维效率提升30%，客户满意率97%",
        "② 仪表竞争格局已变：宁水集团、汉威科技、威铭能源等国内厂商以「AI+传感+平台」全链条方案全面亮相",
        "③ Hach机会在于数据层：水务大模型需要高质量传感器数据；仪表精度是AI决策的基础",
        "④ 深圳样板全国推广信号：住建部明确广东「为全国提供示范」，章林伟提「推广国货精品」",
        "⑤ 章林伟三大战略：数字化赋能 / 价格机制改革 / 培育龙头企业（规模化、集约化）",
    ]
    for i, b in enumerate(bullets):
        add_textbox(slide, Inches(0.6), Inches(1.0 + i * 1.1), Inches(12), Inches(1),
                    [b], [14], [DARK])

    # ─── SLIDE 3: 政策背景：十五五定调 ────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide)
    section_num(slide, "01")
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.6),
                ["政策背景：「十五五」水务定调"], [22], [DARK], [True])
    
    add_textbox(slide, Inches(0.6), Inches(1.0), Inches(5.8), Inches(5.5),
                ["住建部2026年四项重点工作",
                 "",
                 "① 供水安全",
                 "   贯彻新修订《供水条例》",
                 "",
                 "② 排水防涝",
                 "   统筹硬软件建设，加快北方补短板",
                 "",
                 "③ 污水治理",
                 "   推进管网改造和再生水利用",
                 "",
                 "④ 行业支撑",
                 "   完善法规标准，推动智慧化升级和人才培养"],
                [14, 8, 13, 11, 8, 13, 11, 8, 13, 11, 8, 13, 11],
                [DARK, WHITE, BLUE, DARK, DARK, BLUE, DARK, DARK, BLUE, DARK, DARK, BLUE, DARK],
                [True, False, True, False, False, True, False, False, True, False, False, True, False])
    
    add_textbox(slide, Inches(6.8), Inches(1.0), Inches(6), Inches(5.5),
                ["章林伟（中国水协会长）三大战略方向",
                 "",
                 "① 数字化赋能",
                 "   推动AI与供排水全场景深度融合",
                 "   搭建水务AI数据库",
                 "   加快老旧设施改造",
                 "",
                 "② 价格机制改革",
                 "   推动自来水价格听证制度改革",
                 "   污水处理费收费机制转型",
                 "",
                 "③ 培育龙头企业",
                 "   探索产业整合，提升集中度",
                 "   (推广国货精品-国产化信号)",
               ],
                [14,8,13,11,11,11,8,13,11,11,8,13,11,11],
                [DARK, WHITE, BLUE, DARK, DARK, DARK, DARK, BLUE, DARK, DARK, DARK, BLUE, DARK, DARK],
                [True, False, True, False, False, False, False, True, False, False, False, True, False, False])
    
    # Bottom note
    add_textbox(slide, Inches(0.6), Inches(6.8), Inches(12), Inches(0.4),
                ["《供水条例》2026年6月1日正式施行 | 来源：住建部城市建设司综合大会发言"],
                [11], [LIGHT])
    
    # ─── SLIDE 4: AI落地现状 ──────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide)
    section_num(slide, "02")
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.6),
                ["AI+水务：从概念到落地"], [22], [DARK], [True])
    
    # 深水云脑2.0 data
    add_textbox(slide, Inches(0.6), Inches(1.0), Inches(5.8), Inches(0.5),
                ["深水云脑2.0 — 深圳环水集团实测数据（龚利民主讲）"],
                [13], [BLUE], [True])
    
    data_items = [
        ("数字化覆盖率", "超99%"),
        ("运维效率提升", "30%"),
        ("水管家客户满意率", "97%"),
        ("管网漏损率", "5%以下（国际领先）"),
    ]
    for i, (label, val) in enumerate(data_items):
        col = i % 2
        row = i // 2
        x = Inches(0.6 + col * 2.9)
        y = Inches(1.6 + row * 1.5)
        add_textbox(slide, x, y, Inches(2.6), Inches(1.2),
                    [val, label], [28, 12], [BLUE, DARK], [True, False])
    
    add_textbox(slide, Inches(0.6), Inches(4.8), Inches(5.8), Inches(0.4),
                ["已建成：近零碳水厂 | 全地下水质净化厂 | 智能装备出口海外 | 布局开源鸿蒙生态"],
                [11], [LIGHT])
    
    # Right: 技术路线
    add_textbox(slide, Inches(6.8), Inches(1.0), Inches(6), Inches(0.5),
                ["任南琪（哈工大）数字孪生技术架构"],
                [13], [BLUE], [True])
    
    tech_items = [
        "(天-空-地-水)一体化数据感知体系",
        "数字孪生",
        "多模态水质数据融合模型",
        "图像识别原后生动物智能诊断",
    ]
    for i, t in enumerate(tech_items):
        add_textbox(slide, Inches(6.8), Inches(1.6 + i * 0.9), Inches(6), Inches(0.8),
                    [t], [14], [DARK if i % 2 == 0 else LIGHT], [True if i % 2 == 0 else False])
    
    add_textbox(slide, Inches(6.8), Inches(5.3), Inches(6), Inches(1.2),
                ["三大核心制约（亟需国产化替代）：",
                 "• 源代码开发与应用桡梏",
                 "• 行业软件与平台开发框架约束",
                 "• 仪器仪表开发"],
                [12, 11, 11, 11], [DARK, DARK, DARK, DARK])

    # ─── SLIDE 5: AOA污水处理新技术 ────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide)
    section_num(slide, "03")
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.6),
                ["技术亮点：AOA污水处理新技术"], [22], [DARK], [True])
    
    add_textbox(slide, Inches(0.6), Inches(0.95), Inches(12), Inches(0.5),
                ["彭永臻（北京工业大学/中国工程院院士）"],
                [13], [BLUE], [True])
    
    # Key stat
    add_textbox(slide, Inches(0.6), Inches(1.6), Inches(5), Inches(1.5),
                ["14.3°C", "低温下总氮 < 3.8mg/L"],
                [52, 16], [BLUE, DARK], [True, False])
    
    add_textbox(slide, Inches(5.8), Inches(1.6), Inches(7), Inches(1.5),
                ["对比传统AAO工艺优势：",
                 "• 省曝气能耗",
                 "• 减污泥量",
                 "• 降氧化亚氮（N₂O）碳排放"],
                [14, 13, 13, 13], [DARK, DARK, DARK, DARK], [True, False, False, False])
    
    add_textbox(slide, Inches(0.6), Inches(3.4), Inches(6), Inches(0.5),
                ["已有试点工程"],
                [14], [DARK], [True])
    
    pilots = ["北京高碑店水厂", "北京定福庄水厂", "合肥王小郢水厂", "天津张贵庄水厂"]
    for i, p in enumerate(pilots):
        col = i % 2
        row = i // 2
        add_textbox(slide, Inches(0.6 + col * 3), Inches(4.0 + row * 0.9), Inches(2.8), Inches(0.8),
                    [p], [13], [DARK])
    
    add_textbox(slide, Inches(0.6), Inches(5.8), Inches(12), Inches(0.5),
                ["关键结论：好氧区曝气控制是减小N₂O排放的关键 — Hach在线仪表（溶解氧/氨氮/总氮）是SCADA数据基础"],
                [12], [LIGHT])
    
    # Hach关联
    add_textbox(slide, Inches(6.8), Inches(3.4), Inches(6), Inches(2),
                ["Hach关联",
                 "AOA工艺深度脱氮要求：",
                 "• 在线氨氮监测（精度要求↑）",
                 "• 在线溶解氧控制（曝气优化）",
                 "• 在线总氮分析（数据反馈）",
                 "→ SCADA平台数据的重要应用场景"],
                [14, 12, 11, 11, 11, 12],
                [BLUE, DARK, DARK, DARK, DARK, DARK],
                [True, True, False, False, False, False])

    # ─── SLIDE 6: 参展商竞争格局 ──────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide)
    section_num(slide, "04")
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.6),
                ["参展商竞争格局：仪表已经不只是仪表"], [22], [DARK], [True])
    
    add_textbox(slide, Inches(0.6), Inches(0.95), Inches(12), Inches(0.4),
                ["180余家参展 | 5万平米 | 展会主题：精细化 / 智能化 / 绿色化"],
                [12], [LIGHT])
    
    # Table
    headers = ["展商", "赛道/产品", "竞争威胁"]
    rows = [
        ["宁水集团", "AI摄像水表 + 超声波 + 电磁水表 · 管网全链方案", "🔴 高"],
        ["万朗集团", "AI+智慧水务整体方案 · 二供AI大脑", "🟠 中高"],
        ["威铭能源", "智慧水务全场景（威胜信息旗下）", "🟠 中"],
        ["汉威科技", "传感技术（水务传感解决方案）", "🟡 中"],
        ["舜禹股份", "智慧水务全链条（水源→用户→再生水）", "🟡 中"],
        ["博铭维", "管网机器人 + 鸿蒙系统监测模块", "🟢 低"],
        ["开发科技", "水计量自主知识产权", "🟢 低"],
        ["三川智慧", "超声波/电磁水表（已获华为技术认证）", "🟡 中"],
    ]
    
    bullet_table(slide, Inches(0.5), Inches(1.4), Inches(12.3), Inches(5),
                 headers, rows,
                 col_widths=[Inches(2.2), Inches(7.8), Inches(2.3)])
    
    add_textbox(slide, Inches(0.6), Inches(6.7), Inches(12), Inches(0.4),
                ["关键观察：国内厂商已从(单品仪表)→(传感+通信+平台+AI分析)全链条方案；外资单品优势被逐渐稀释"],
                [11], [LIGHT])
    
    # ─── SLIDE 7: 宁水集团深度分析 ─────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide)
    section_num(slide, "05")
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.6),
                ["重点展商：宁水集团 — 最直接竞争威胁"], [22], [DARK], [True])
    
    add_textbox(slide, Inches(0.6), Inches(0.95), Inches(6), Inches(0.5),
                ["宁波水表（集团）股份有限公司 | 常务理事单位 | 国家级制造业单项冠军企业"],
                [12], [LIGHT])
    
    # Left column: 产品
    add_textbox(slide, Inches(0.6), Inches(1.5), Inches(5.5), Inches(0.5),
                ["核心产品矩阵"], [14], [BLUE], [True])
    
    products = [
        ("AI摄像水表", "摄像+AI识别，无需人工读表，替代机械水表趋势明显"),
        ("超声波水表", "工业/商业管网计量主品"),
        ("电磁水表", "高精度大口径水表"),
        ("管网精细化运维方案", "从仪表向平台延伸"),
    ]
    for i, (name, desc) in enumerate(products):
        add_textbox(slide, Inches(0.6), Inches(2.1 + i * 1.2), Inches(5.5), Inches(1.0),
                    [name, desc], [13, 11], [DARK, LIGHT], [True, False])
    
    # Right column: 威胁本质
    add_textbox(slide, Inches(6.8), Inches(1.5), Inches(6), Inches(0.5),
                ["Hach竞争威胁评估"], [14], [BLUE], [True])
    
    threats = [
        ("替代威胁", "🔴 高", "AI摄像水表直接替代传统机械水表；Hach机械表产品线受冲击"),
        ("平台延伸", "🟠 中高", "从仪表向智慧水务平台延伸，与Hach SCADA直接竞争"),
        ("国产化", "🟠 中高", "章林伟明确提出(推广国货精品)，政策有利国产"),
        ("价格竞争", "🟡 中", "国产价格普遍低于Hach，中小水务优先考虑性价比"),
    ]
    for i, (name, level, desc) in enumerate(threats):
        add_textbox(slide, Inches(6.8), Inches(2.1 + i * 1.2), Inches(6), Inches(1.0),
                    [f"{name} {level}", desc], [12, 11], [DARK, LIGHT], [True, False])
    
    add_textbox(slide, Inches(0.6), Inches(6.7), Inches(12), Inches(0.4),
                ["建议：立即对标宁水集团AI摄像水表核心参数，制定差异化竞争策略"],
                [12], [LIGHT])

    # ─── SLIDE 8: Hach机会 ─────────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide)
    section_num(slide, "06")
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.6),
                ["Hach机会矩阵：威胁与机会并存"], [22], [DARK], [True])
    
    add_textbox(slide, Inches(0.6), Inches(0.95), Inches(12), Inches(0.4),
                ["IMS视角判断：仪表竞争威胁是真实的，但AI时代对高质量数据的需求也在放大Hach的核心价值"],
                [12], [LIGHT])
    
    # Threat side
    add_textbox(slide, Inches(0.6), Inches(1.5), Inches(5.8), Inches(0.5),
                ["🔴 竞争威胁"], [15], [DARK], [True])
    
    threat_items = [
        "宁水集团AI摄像水表：直接替代机械表品",
        "威铭/万朗/舜禹全链条：SCADA平台替代",
        "鸿蒙生态锁定：无接入能力面临投标出局",
        "价格竞争：国产仪表成本优势明显",
    ]
    for i, t in enumerate(threat_items):
        add_textbox(slide, Inches(0.6), Inches(2.1 + i * 0.85), Inches(5.8), Inches(0.75),
                    [t], [12], [DARK])
    
    # Opportunity side
    add_textbox(slide, Inches(6.8), Inches(1.5), Inches(6), Inches(0.5),
                ["🟢 Hach机会"], [15], [BLUE], [True])
    
    opp_items = [
        "AI大模型依赖高质量传感器数据（精度即壁垒）",
        "AOA等新工艺对在线仪表提出更高要求",
        "老旧设施改造：仪表更新换代需求（章林伟明确提出）",
        "深圳样板全国推广：配套采购释放",
    ]
    for i, t in enumerate(opp_items):
        add_textbox(slide, Inches(6.8), Inches(2.1 + i * 0.85), Inches(6), Inches(0.75),
                    [t], [12], [DARK])
    
    add_textbox(slide, Inches(0.6), Inches(5.6), Inches(12), Inches(0.5),
                ["核心判断：AI时代仪表的核心价值不是(替代人)，而是(喂给AI的数据源头)——Hach仪表精度是AI决策的基础"],
                [13], [BLUE], [True])
    
    # Shenzhen sample
    add_textbox(slide, Inches(0.6), Inches(6.2), Inches(12), Inches(0.5),
                ["深圳信号：深圳住建局明确提出(为全国提供示范)；香港水务署黄恩诺出席综合大会（深圳=全国样板）"],
                [11], [LIGHT])

    # ─── SLIDE 9: 行动建议 ─────────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide)
    section_num(slide, "07")
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.6),
                ["Hach行动建议"], [22], [DARK], [True])
    
    add_textbox(slide, Inches(0.6), Inches(0.95), Inches(12), Inches(0.4),
                ["基于本次年会情报整理，后续行动优先级排序"],
                [12], [LIGHT])
    
    # Phase 1
    add_textbox(slide, Inches(0.6), Inches(1.5), Inches(12), Inches(0.5),
                ["立即行动（0-3个月）"], [14], [BLUE], [True])
    
    phase1 = [
        ("1. 对标宁水集团AI摄像水表", "获取产品规格书，与Hach产品参数逐项对比，明确差距"),
        ("2. 了解深水云脑2.0数据接口", "联系深圳水务科技（马丹红团队），确认仪表/SCADA对接规格"),
        ("3. 联系深圳水务龚利民团队", "了解仪表采购规格要求，评估Hach入围可能性"),
    ]
    for i, (title, desc) in enumerate(phase1):
        add_textbox(slide, Inches(0.6), Inches(2.1 + i * 0.95), Inches(12), Inches(0.85),
                    [title, desc], [13, 11], [DARK, LIGHT], [True, False])
    
    # Phase 2
    add_textbox(slide, Inches(0.6), Inches(5.0), Inches(12), Inches(0.5),
                ["中期（3-12个月）"], [14], [BLUE], [True])
    
    phase2 = [
        ("1. 围绕《供水条例》6月1日施行", "梳理Hach合规优势，编制合规产品手册"),
        ("2. 建立与国内智慧水务平台合作", "威铭/万朗/舜禹——仪表作为数据采集端被集成"),
        ("3. 制定老旧设施改造专项方案", "抓住(加快老旧设施改造)政策窗口"),
    ]
    for i, (title, desc) in enumerate(phase2):
        add_textbox(slide, Inches(0.6), Inches(5.5 + i * 0.65), Inches(12), Inches(0.6),
                    [title, desc], [12, 11], [DARK, LIGHT], [True, False])

    # ─── SLIDE 10: 数据来源 ─────────────────────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    blue_bar(slide)
    section_num(slide, "08")
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.6),
                ["数据来源"], [22], [DARK], [True])
    
    sources = [
        "人民网深圳4月19日电（刘森君）— 综合大会报道",
        "中新网广州4月19日电（记者 王坚）— 综合大会报道",
        "百度百科 — 中国水协2026年会条目",
        "南方+新闻（2026-04-17）",
        "深圳政府在线 — 新闻发布会（2026-04-14）",
        "水业圈公众号（cuwa_org_cn）— 展会动态",
        "宁水集团参展信息（2026-04-18）",
        "汉威科技参展信息（2026-04-18）",
        "威铭能源参展信息（2026-04-16）",
        "开发科技参展信息（2026-04-16）",
        "万朗集团参展信息（2026-04-14）",
        "央视网 — 深圳南山水厂报道",
        "深圳特区报数字报",
        "住建部城市建设司 — 综合大会发言",
        "中国水协官网 cuwa.org.cn",
    ]
    
    for i, s in enumerate(sources):
        add_textbox(slide, Inches(0.6), Inches(1.0 + i * 0.42), Inches(12), Inches(0.38),
                    [s], [10], [DARK])
    
    add_textbox(slide, Inches(0.6), Inches(7.1), Inches(12), Inches(0.3),
                ["数据截至2026年4月22日 | 结论仅供参考，不构成投资建议"],
                [10], [LIGHT])

    # Save
    prs.save(OUTPUT)
    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    create_presentation()
