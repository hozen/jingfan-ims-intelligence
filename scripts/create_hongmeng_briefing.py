from pptx import Presentation
from pptx.util import Pt, Inches, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import copy

# Colors
BLUE = RGBColor(0, 126, 181)
DARK_GRAY = RGBColor(77, 77, 77)
LIGHT_GRAY = RGBColor(153, 153, 153)
WHITE = RGBColor(255, 255, 255)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

def add_title_slide(prs, title, subtitle=""):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    # White background - no fill needed (default is white)

    # Title
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.5), Inches(1.2))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.font.name = "Microsoft YaHei"

    # Subtitle
    if subtitle:
        txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(11.5), Inches(0.8))
        tf2 = txBox2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = subtitle
        p2.font.size = Pt(20)
        p2.font.color.rgb = DARK_GRAY
        p2.font.name = "Microsoft YaHei"

    # Date
    txBox3 = slide.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.5), Inches(0.5))
    tf3 = txBox3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "2026年4月20日"
    p3.font.size = Pt(14)
    p3.font.color.rgb = LIGHT_GRAY
    p3.font.name = "Microsoft YaHei"

    return slide

def add_content_slide(prs, title, bullet_points, note=""):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Title
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.5), Inches(0.8))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.font.name = "Microsoft YaHei"

    # Blue line under title
    line = slide.shapes.add_shape(1, Inches(0.8), Inches(1.2), Inches(2.0), Pt(3))
    line.fill.solid()
    line.fill.fore_color.rgb = BLUE
    line.line.fill.background()

    # Bullets
    txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.5), Inches(5.0))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    for i, point in enumerate(bullet_points):
        if i == 0:
            p = tf2.paragraphs[0]
        else:
            p = tf2.add_paragraph()
        p.text = "• " + point
        p.font.size = Pt(18)
        p.font.color.rgb = DARK_GRAY
        p.font.name = "Microsoft YaHei"
        p.space_after = Pt(12)

    # Note at bottom
    if note:
        txBox3 = slide.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.5), Inches(0.4))
        tf3 = txBox3.text_frame
        p3 = tf3.paragraphs[0]
        p3.text = note
        p3.font.size = Pt(12)
        p3.font.color.rgb = LIGHT_GRAY
        p3.font.italic = True
        p3.font.name = "Microsoft YaHei"

    return slide

def add_two_column_slide(prs, title, left_title, left_points, right_title, right_points, note=""):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Title
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.5), Inches(0.8))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.font.name = "Microsoft YaHei"

    # Blue line
    line = slide.shapes.add_shape(1, Inches(0.8), Inches(1.2), Inches(2.0), Pt(3))
    line.fill.solid()
    line.fill.fore_color.rgb = BLUE
    line.line.fill.background()

    # Left column title
    ltx = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.5), Inches(0.5))
    ltf = ltx.text_frame
    lp = ltf.paragraphs[0]
    lp.text = left_title
    lp.font.size = Pt(18)
    lp.font.bold = True
    lp.font.color.rgb = DARK_GRAY
    lp.font.name = "Microsoft YaHei"

    # Left column content
    ltx2 = slide.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.5), Inches(4.0))
    ltf2 = ltx2.text_frame
    ltf2.word_wrap = True
    for i, point in enumerate(left_points):
        if i == 0:
            p = ltf2.paragraphs[0]
        else:
            p = ltf2.add_paragraph()
        p.text = "• " + point
        p.font.size = Pt(16)
        p.font.color.rgb = DARK_GRAY
        p.font.name = "Microsoft YaHei"
        p.space_after = Pt(8)

    # Right column title
    rtx = slide.shapes.add_textbox(Inches(6.8), Inches(1.5), Inches(5.5), Inches(0.5))
    rtf = rtx.text_frame
    rp = rtf.paragraphs[0]
    rp.text = right_title
    rp.font.size = Pt(18)
    rp.font.bold = True
    rp.font.color.rgb = DARK_GRAY
    rp.font.name = "Microsoft YaHei"

    # Right column content
    rtx2 = slide.shapes.add_textbox(Inches(6.8), Inches(2.1), Inches(5.5), Inches(4.0))
    rtf2 = rtx2.text_frame
    rtf2.word_wrap = True
    for i, point in enumerate(right_points):
        if i == 0:
            p = rtf2.paragraphs[0]
        else:
            p = rtf2.add_paragraph()
        p.text = "• " + point
        p.font.size = Pt(16)
        p.font.color.rgb = DARK_GRAY
        p.font.name = "Microsoft YaHei"
        p.space_after = Pt(8)

    if note:
        txBox3 = slide.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.5), Inches(0.4))
        tf3 = txBox3.text_frame
        p3 = tf3.paragraphs[0]
        p3.text = note
        p3.font.size = Pt(12)
        p3.font.color.rgb = LIGHT_GRAY
        p3.font.italic = True
        p3.font.name = "Microsoft YaHei"

    return slide


# ============ SLIDES ============

# Slide 1: Title
add_title_slide(
    prs,
    "华为鸿蒙生态水质仪表市场情报简报",
    "Hach中国IMS产品线 · 环博会特别版"
)

# Slide 2: 源头驱动
add_content_slide(
    prs,
    "深圳环水 × 华为：战略合作的驱动力",
    [
        "深圳环水集团 × 华为技术：2025-01-23 坂田基地签约",
        "深圳环水需要：数字化转型、国产化背书、智慧水务标杆",
        "华为需要：水务关键场景落地鸿蒙生态",
        "双方互需 → 战略合作 → 加速推进鸿蒙水务落地",
        "",
        "关键人物：龚利民（深圳环水总裁）× 李俊风（华为公共事业军团总裁）",
        "技术落地执行：马丹红（深圳水务科技自控工程部部长）",
        "",
        "深圳已有多个落地案例：",
        "  - 章阁净水厂（2025-12）：全国首座鸿蒙水厂",
        "  - 五指耙水厂（2026-03）：30万吨/天，全国首座鸿蒙智慧水厂",
        "  - 大沙河流域（2026-03）",
        "  - 荷坳水厂（2026-03招标中）",
    ],
    "数据来源：深圳政府在线、南方都市报、21世纪经济报道"
)

# Slide 3: 竞争格局
add_two_column_slide(
    prs,
    "竞争格局：谁已接入 / 传言接入",
    "已验证接入",
    [
        "三川智慧（超声波/电磁水表）：华为技术认证，对接华为云IoT",
        "博铭维（管网机器人）：全链路鸿蒙生态，年会有主题论坛",
        "尚易科技：鸿蒙边缘网关合作方，IPC3528已验证",
        "深圳10余家仪表厂商：五指耙水厂项目，通过网关方案接入",
    ],
    "传言接入（未公开证实）",
    [
        "吉林光大分析技术：主营二次供水多参数监测仪（非工业水厂）",
        "  → 产品定位：民用Residential二次供水，与Hach不同赛道",
        "  → 鸿蒙认证：全网无公开证据，但消息来源较明确",
        "  → 判断：可能有内部测试认证，未对外公开",
        "",
        "汉威科技：有水质在线检测设备，水协年会有展示，鸿蒙关系不明",
    ],
    "IMS视角：Hach核心竞品——吉林光大（非直接竞争但影响市场认知）、汉威科技（直接竞争）"
)

# Slide 4: 技术路径
add_content_slide(
    prs,
    "技术路径：五指耙水厂实证分析",
    [
        "项目背景：",
        "  深圳深水宝安水务集团五指耙水厂改扩建工程（30万吨/天）",
        "  原有8类具身智能机器人 + 智能井盖 + 摄像头 + 消火栓等终端",
        "  来自10余厂商，协议不兼容，数据孤岛严重",
        "",
        "技术方案：水鸿WaterHMOS分布式架构",
        "  核心定位：打破多厂商设备协议壁垒，统一数据调度",
        "  不是要求每家仪表厂商单独接入，而是系统集成层统一消化",
        "  接入方式：鸿蒙边缘网关（IPC3528/RK3568）+ B-LINK近场连接",
        "",
        "具体接入架构：",
        "  仪表设备（MODBUS RTU/TCP） → 鸿蒙边缘网关 → 华为云IoT → WaterHMOS平台",
        "  华为云IoT提供设备接入和数据汇聚，WaterHMOS做统一调度",
        "",
        "接入效果：运维效率提升30%+，误报率降低30%",
        "",
        "对Hach的启示：深圳水务接受网关方案，仪表厂只需保证MODBUS输出，无需单独认证",
    ],
    "数据来源：深圳水务科技公司、中国水网(h2o-china.com) 2024-12报道"
)

# Slide 5: Hach切入路径
add_content_slide(
    prs,
    "Hach切入路径：行动建议",
    [
        "立即行动（0-3个月）：",
        "  1. 联系尚易科技：了解Hach + IPC3528网关集成可行性",
        "  2. 联系深圳水务科技马丹红团队：了解仪表接入具体要求",
        "  3. Hach仪表MODBUS数据通过网关测试：验证数据上传",
        "",
        "中期（3-6个月）：",
        "  4. 成为深圳水务鸿蒙生态合作伙伴",
        "  5. 与华为云IoT完成兼容性测试",
        "  6. 数据手册标注「支持鸿蒙生态接入」",
        "",
        "风险提示：",
        "  若深圳市场实质门槛形成（Hach尚未接入）→ 短期内无法在深投标",
        "  时间差 = 竞争对手抢单窗口期",
        "",
        "IMS建议：以网关方案快速切入深圳市场，同步布局华为云IoT认证",
    ],
    "IMS视角：转化率20%是核心痛点——接入鸿蒙生态可直接提升深圳项目竞争力"
)

# Slide 6: 关键未知项
add_content_slide(
    prs,
    "关键未知项与下一步",
    [
        "需即时关注：",
        "  ❓ 吉林光大认证传言的具体来源：是否光大官方宣传？",
        "  ❓ 深圳是否有明确文件要求仪表必须支持鸿蒙接入",
        "  ❓ 另外两个试点城市（销售提到4个城市：深圳 + 成都 + ？）",
        "",
        "例行监控：",
        "  ○ 水协2026年会后续报道：马丹红演讲全文、参展商名单",
        "  ○ 深圳水务鸿蒙生态合作伙伴名单更新",
        "  ○ 华为云IoT水务行业合作伙伴名单",
        "",
        "下一步：",
        "  → 向销售确认吉林光大消息来源",
        "  → 联系尚易科技（网关合作方）获取技术规格",
        "  → 接触深圳水务科技（马丹红团队）",
    ],
    "情报截止：2026-04-20 | 持续跟踪中"
)

# Save
output_path = "/home/agentuser/wiki/projects/hongmeng-water-instrument/briefing.pptx"
prs.save(output_path)
print(f"Saved: {output_path}")
