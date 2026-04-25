# -*- coding: utf-8 -*-
"""
Work-06 v2: Taylor AI分享 - Senior设计版
重新设计: 留白优先, 层级分明, 减少色块堆积
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

# ── 颜色 ──────────────────────────────────────────────
NAVY     = RGBColor(0x1A, 0x2B, 0x4A)
TEAL     = RGBColor(0x0D, 0x94, 0x88)
AMBER    = RGBColor(0xF5, 0x9E, 0x0B)
LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
DARK     = RGBColor(0x1E, 0x29, 0x3B)
GRAY     = RGBColor(0x64, 0x74, 0x8B)
LGRAY    = RGBColor(0xE2, 0xE8, 0xF0)
TEAL_L   = RGBColor(0xCC, 0xE8, 0xE5)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H
BLANK = prs.slide_layouts[6]


def rect(slide, l, t, w, h, fill=None, line=None, lw=None):
    sh = slide.shapes.add_shape(1, l, t, w, h)
    if fill:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    else:
        sh.fill.background()
    if line:
        sh.line.color.rgb = line
        if lw: sh.line.width = lw
    else:
        sh.line.fill.background()
    return sh

def txt(slide, l, t, w, h, text, fs=14, bold=False, color=DARK,
        align=PP_ALIGN.LEFT, italic=False, name="Microsoft YaHei"):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tb.word_wrap = True
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(fs)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = name
    return tb

def tag(slide, label, l, t, bg=NAVY, fg=WHITE, w=None, h=Inches(0.28)):
    if w is None:
        w = Inches(len(label) * 0.13 + 0.3)
    rect(slide, l, t, w, h, fill=bg)
    tb = slide.shapes.add_textbox(l, t, w, h)
    p = tb.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = label
    run.font.size = Pt(10); run.font.bold = True
    run.font.color.rgb = fg; run.font.name = "Microsoft YaHei"
    return tb

def keyinfo(slide, text):
    txt(slide, Inches(0.7), SLIDE_H - Inches(0.65),
        SLIDE_W - Inches(1.4), Inches(0.4),
        text=text, fs=12, color=TEAL, italic=True)

def light_slide():
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, fill=LIGHT_BG)
    return s

def dark_slide():
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, fill=NAVY)
    return s

def slide_header(slide, label_text, main_title, subtitle=None):
    """简洁的顶部布局: 标签 + 大标题 + 可选副标题"""
    tag(slide, label_text, Inches(0.7), Inches(0.5))
    txt(slide, Inches(0.7), Inches(0.88), Inches(11.5), Inches(0.75),
        main_title, fs=30, bold=True, color=NAVY)
    if subtitle:
        txt(slide, Inches(0.7), Inches(1.55), Inches(11), Inches(0.35),
            subtitle, fs=12, color=GRAY)


# ============================================================
# Slide 1: Cover - 极简
# ============================================================
s1 = dark_slide()
rect(s1, 0, 0, SLIDE_W, Inches(0.06), fill=TEAL)

# 左上角标签
tag(s1, "INTERNAL", Inches(0.7), Inches(0.6), bg=RGBColor(0x2D, 0x3E, 0x5C), fg=TEAL)

# 大标题, 靠左, 留大量空白
txt(s1, Inches(0.7), Inches(2.0), Inches(10), Inches(1.6),
    "在使用中学习 AI", fs=48, bold=True, color=WHITE)

# 副标题
txt(s1, Inches(0.7), Inches(3.6), Inches(8), Inches(0.5),
    "三个月实践 / 真实案例 / 诚实的踩坑", fs=18, color=TEAL)

# 细线分隔
rect(s1, Inches(0.7), Inches(4.3), Inches(4), Inches(0.025), fill=TEAL)

# 演讲者信息
txt(s1, Inches(0.7), Inches(4.5), Inches(8), Inches(0.4),
    "Taylor  |  Hach China iMS业务负责人 & China AI技术联系人  |  2026",
    fs=13, color=RGBColor(0x94, 0xA3, 0xB8))

# 底部议程标签
txt(s1, Inches(0.7), Inches(6.4), Inches(2), Inches(0.35),
    "Agenda", fs=11, bold=True, color=GRAY)
agenda = ["开场打破认知", "四个业务场景", "诚实的部分", "附录"]
agenda_colors = [TEAL, TEAL, AMBER, GRAY]
for i, (a, c) in enumerate(zip(agenda, agenda_colors)):
    x = Inches(0.7 + i * 2.8)
    rect(s1, x, Inches(6.8), Inches(2.5), Inches(0.03), fill=c)
    txt(s1, x, Inches(6.85), Inches(2.5), Inches(0.3),
        a, fs=11, color=c)


# ============================================================
# Slide 2: Opening Story
# ============================================================
s2 = light_slide()
slide_header(s2, "开场", "打破认知: 过年三天, 做出一个App")

# 左侧: 故事, 用细线分隔
txt(s2, Inches(0.7), Inches(2.2), Inches(5.5), Inches(0.4),
    "真实故事", fs=12, bold=True, color=TEAL)
rect(s2, Inches(0.7), Inches(2.58), Inches(1.2), Inches(0.02), fill=TEAL)

story = [
    "春节假期, Claude Code刚上线",
    "目标: 把多年培训视频和资料做成一个App",
    "结果: 类YouTube界面 + 文档 + 记忆卡片",
    "两三天上线, 同事直呼不可思议",
]
for i, s in enumerate(story):
    txt(s2, Inches(0.7), Inches(2.75) + Inches(0.5*i),
        Inches(5.5), Inches(0.45), s, fs=14, color=DARK)

# 右侧: 对比表格, 干净线条
txt(s2, Inches(7.0), Inches(2.2), Inches(5.5), Inches(0.4),
    "对比", fs=12, bold=True, color=GRAY)
rect(s2, Inches(7.0), Inches(2.58), Inches(0.6), Inches(0.02), fill=LGRAY)

rows = [
    ("传统原生开发",    "AI辅助开发",     True),
    ("专人专职",        "非专业人员",      False),
    ("6-12个月",        "2-3天",         False),
    ("成本极高",        "零额外成本",      False),
]
for i, (l, r, hdr) in enumerate(rows):
    y = Inches(2.75) + Inches(0.55*i)
    rect(s2, Inches(7.0), y - Inches(0.08), Inches(5.3), Inches(0.01), fill=LGRAY)
    c1 = GRAY if hdr else DARK
    c2 = TEAL if not hdr else TEAL
    txt(s2, Inches(7.0), y, Inches(2.5), Inches(0.4),
        l, fs=13, bold=hdr, color=c1)
    txt(s2, Inches(9.6), y, Inches(2.7), Inches(0.4),
        r, fs=13, bold=hdr, color=c2)

keyinfo(s2, "AI最大的价值不是帮你写得更快, 而是让你能做以前根本做不到的事")


# ============================================================
# Slide 3: Scene 1 - 竞品情报
# ============================================================
s3 = light_slide()
slide_header(s3, "场景一", "竞品情报收集", "市场 / 服务 / 销售")

# 左案例
txt(s3, Inches(0.7), Inches(2.25), Inches(5.5), Inches(0.35),
    "环博会 2026, 上海浦东", fs=14, bold=True, color=NAVY)
rect(s3, Inches(0.7), Inches(2.6), Inches(5.5), Inches(0.02), fill=LGRAY)
steps = [
    ("1", "录音笔录制讲座"),
    ("2", "AI自动转文字"),
    ("3", "AI搜索整理信息"),
    ("4", "生成竞品分析PPT"),
]
for i, (num, desc) in enumerate(steps):
    y = Inches(2.75) + Inches(0.5*i)
    rect(s3, Inches(0.7), y + Inches(0.05), Inches(0.35), Inches(0.35), fill=TEAL)
    txt(s3, Inches(0.7), y + Inches(0.05), Inches(0.35), Inches(0.35),
        num, fs=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s3, Inches(1.2), y, Inches(4.8), Inches(0.4), desc, fs=13, color=DARK)

txt(s3, Inches(0.7), Inches(4.85), Inches(5.5), Inches(0.35),
    "覆盖100+参展企业, 包含技术趋势分析",
    fs=11, italic=True, color=GRAY)

# 右案例
txt(s3, Inches(7.2), Inches(2.25), Inches(5.5), Inches(0.35),
    "水协2026年会, 远程跟踪", fs=14, bold=True, color=NAVY)
rect(s3, Inches(7.2), Inches(2.6), Inches(5.5), Inches(0.02), fill=LGRAY)
steps2 = [
    ("1", "设置定时爬取任务"),
    ("2", "每6小时自动运行"),
    ("3", "整理最新发布信息"),
    ("4", "邮件推送到本人"),
]
for i, (num, desc) in enumerate(steps2):
    y = Inches(2.75) + Inches(0.5*i)
    rect(s3, Inches(7.2), y + Inches(0.05), Inches(0.35), Inches(0.35), fill=NAVY)
    txt(s3, Inches(7.2), y + Inches(0.05), Inches(0.35), Inches(0.35),
        num, fs=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s3, Inches(7.7), y, Inches(4.8), Inches(0.4), desc, fs=13, color=DARK)

txt(s3, Inches(7.2), Inches(4.85), Inches(5.5), Inches(0.35),
    "即使不在现场, 也能接近身临其境",
    fs=11, italic=True, color=GRAY)

keyinfo(s3, "AI是信息密度的放大器, 不是替代判断的工具")


# ============================================================
# Slide 4: Document Workflow
# ============================================================
s4 = light_slide()
slide_header(s4, "场景二", "文档工作流", "市场 / 财务 / 法务 / 所有人")

# 流程: 4步骤横向排列, 简洁线条
step_x = [Inches(0.7), Inches(3.6), Inches(6.5), Inches(9.4)]
step_labels = ["起草", "生成", "审核", "输出"]
step_sub    = ["人写模板和思路", "AI按模板填充初稿", "人工Review修正", "文档直接生成PPT"]

for i, (x, label, sub) in enumerate(zip(step_x, step_labels, step_sub)):
    # 圆点
    rect(s4, x, Inches(2.5), Inches(0.22), Inches(0.22),
         fill=TEAL if i % 2 == 0 else NAVY)
    # 标签
    txt(s4, x + Inches(0.35), Inches(2.45), Inches(2.5), Inches(0.35),
        label, fs=16, bold=True, color=NAVY)
    txt(s4, x + Inches(0.35), Inches(2.82), Inches(2.5), Inches(0.35),
        sub, fs=12, color=GRAY)
    # 连接线
    if i < 3:
        rect(s4, x + Inches(2.65), Inches(2.58), Inches(0.7), Inches(0.015), fill=LGRAY)

# 案例卡片, 简洁
rect(s4, Inches(0.7), Inches(4.2), Inches(12.0), Inches(0.02), fill=TEAL)
txt(s4, Inches(0.7), Inches(4.35), Inches(2), Inches(0.35),
    "案例", fs=11, bold=True, color=TEAL)
txt(s4, Inches(0.7), Inches(4.7), Inches(11.5), Inches(0.7),
    "产品经理陈涛: 以往写一份授权文档需要数天反复修改; "
    "现在思路清晰时, 半天到一个晚上完成文档, 再直接生成PPT, 两三次确认即可发给客户。",
    fs=14, color=DARK)

keyinfo(s4, "人定方向, AI填内容 - 这个分工适用于所有部门")


# ============================================================
# Slide 5: Agent & Quality Control
# ============================================================
s5 = light_slide()
slide_header(s5, "场景三", "自主Agent与质量管控", "IT / 法务")

# 左列: Agent工作方式
txt(s5, Inches(0.7), Inches(2.2), Inches(5.5), Inches(0.35),
    "Agent工作方式", fs=13, bold=True, color=NAVY)
rect(s5, Inches(0.7), Inches(2.55), Inches(1.0), Inches(0.02), fill=TEAL)
agent = [
    "每4小时自动运行一次",
    "覆盖线索扫描 + 竞品监控",
    "串行执行, 一次只做一件事",
    "仅推送到dev分支, 经审核才合并主线",
    "每次运行留下审计日志",
]
for i, item in enumerate(agent):
    rect(s5, Inches(0.7), Inches(2.75) + Inches(0.52*i),
         Inches(0.08), Inches(0.08), fill=TEAL if i % 2 == 0 else NAVY)
    txt(s5, Inches(0.95), Inches(2.7) + Inches(0.52*i),
        Inches(5.2), Inches(0.45), item, fs=13, color=DARK)

# 右列: 质量门控
txt(s5, Inches(7.2), Inches(2.2), Inches(5.5), Inches(0.35),
    "质量门控机制", fs=13, bold=True, color=NAVY)
rect(s5, Inches(7.2), Inches(2.55), Inches(1.0), Inches(0.02), fill=TEAL)
qa = [
    "数据完整性审计: 17个问题识别并修复",
    "置信度强制标注: 高 / 中 / 低 三级",
    "信息源类型标注: 官方 / 媒体 / 推断",
    "人工审核节点: Taylor每轮审核确认",
]
for i, item in enumerate(qa):
    rect(s5, Inches(7.2), Inches(2.75) + Inches(0.52*i),
         Inches(0.08), Inches(0.08), fill=TEAL if i % 2 == 0 else NAVY)
    txt(s5, Inches(7.45), Inches(2.7) + Inches(0.52*i),
        Inches(5.3), Inches(0.45), item, fs=13, color=DARK)

keyinfo(s5, "AI系统不是黑箱 - 可以被设计、被审计、被管理")


# ============================================================
# Slide 6: Data Analysis
# ============================================================
s6 = light_slide()
slide_header(s6, "场景四", "数据分析与预测", "居家桥水厂 / 传感器数据分析")

# 左侧发现
txt(s6, Inches(0.7), Inches(2.2), Inches(6.5), Inches(0.35),
    "核心发现", fs=13, bold=True, color=NAVY)
rect(s6, Inches(0.7), Inches(2.55), Inches(0.8), Inches(0.02), fill=TEAL)

findings = [
    "分析6个月传感器数据, 发现5个人工看不见的异常",
    "FreeNH4可提前3-7天预警试剂瓶故障",
    "两次历史故障均成功回测, 150天无误报",
    "检测规则自动激活, 无需客户手动配置",
]
for i, f in enumerate(findings):
    txt(s6, Inches(0.7), Inches(2.72) + Inches(0.58*i),
        Inches(6.2), Inches(0.52), f, fs=13, color=DARK)

# 右侧大数字
txt(s6, Inches(8.0), Inches(2.2), Inches(4.5), Inches(0.35),
    "实测数据", fs=13, bold=True, color=GRAY)
rect(s6, Inches(8.0), Inches(2.55), Inches(0.6), Inches(0.02), fill=LGRAY)

# 数字卡片1
rect(s6, Inches(8.0), Inches(2.75), Inches(4.5), Inches(1.7),
     fill=NAVY, line=NAVY)
txt(s6, Inches(8.0), Inches(2.9), Inches(4.5), Inches(0.35),
    "提前预警周期", fs=12, color=TEAL, align=PP_ALIGN.CENTER)
txt(s6, Inches(8.0), Inches(3.2), Inches(4.5), Inches(0.9),
    "3-7天", fs=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s6, Inches(8.0), Inches(4.0), Inches(4.5), Inches(0.3),
    "居家桥水厂", fs=11, color=GRAY, align=PP_ALIGN.CENTER)

# 数字卡片2
rect(s6, Inches(8.0), Inches(4.7), Inches(4.5), Inches(1.5),
     fill=TEAL, line=TEAL)
txt(s6, Inches(8.0), Inches(4.85), Inches(4.5), Inches(0.3),
    "150天内误报次数", fs=12, color=WHITE, align=PP_ALIGN.CENTER)
txt(s6, Inches(8.0), Inches(5.1), Inches(4.5), Inches(0.8),
    "0次", fs=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

keyinfo(s6, "AI发现人看不见的规律, 但验证和决策仍由人完成")


# ============================================================
# Slide 7: Pitfalls - 琥珀黄点缀
# ============================================================
s7 = light_slide()
slide_header(s7, "诚实的部分", "我踩过的坑")

# 左: 踩坑
txt(s7, Inches(0.7), Inches(2.2), Inches(5.5), Inches(0.35),
    "踩坑案例: 客户联系人数据收集", fs=13, bold=True, color=AMBER)
rect(s7, Inches(0.7), Inches(2.55), Inches(1.2), Inches(0.02), fill=AMBER)

pitfalls = [
    "AI返回了一批联系人数据",
    "要求说明来源 -> 称来自搜索引擎缓存页",
    "去验证 -> 找不到缓存页面入口",
    "数据真实性无法确认",
]
for i, p in enumerate(pitfalls):
    txt(s7, Inches(0.7), Inches(2.75) + Inches(0.52*i),
        Inches(5.5), Inches(0.45),
        f"{'①' if i==0 else '②' if i==1 else '③' if i==2 else '④'}  {p}",
        fs=13, color=DARK)

rect(s7, Inches(0.7), Inches(4.9), Inches(5.5), Inches(0.02), fill=AMBER)
txt(s7, Inches(0.7), Inches(5.0), Inches(5.5), Inches(0.5),
    "结论: AI幻觉在数据领域真实存在, 不能盲目信任",
    fs=12, bold=True, color=RGBColor(0xB4, 0x53, 0x0C))

# 右: 工作原则
txt(s7, Inches(7.2), Inches(2.2), Inches(5.5), Inches(0.35),
    "我的工作原则", fs=13, bold=True, color=NAVY)
rect(s7, Inches(7.2), Inches(2.55), Inches(1.0), Inches(0.02), fill=LGRAY)

principles = [
    "只用公开数据与外部AI交互",
    "内部文件 / 客户数据绝不上传外部AI",
    "AI负责初稿, 人负责验证和决策",
    "结果由使用者本人负责",
]
for i, pr in enumerate(principles):
    rect(s7, Inches(7.2), Inches(2.75) + Inches(0.52*i),
         Inches(0.08), Inches(0.08), fill=TEAL)
    txt(s7, Inches(7.45), Inches(2.7) + Inches(0.52*i),
        Inches(5.3), Inches(0.45), pr, fs=13, color=DARK)

keyinfo(s7, "AI幻觉是真实存在的 - 人的判断永远不能被绕过")


# ============================================================
# Slide 8: Legal
# ============================================================
s8 = light_slide()
slide_header(s8, "给法务的结论", "今天所有案例的共同底线")

# 醒目声明
rect(s8, Inches(0.7), Inches(2.3), Inches(12.0), Inches(0.85), fill=NAVY)
txt(s8, Inches(0.9), Inches(2.45), Inches(11.6), Inches(0.6),
    "今天分享的所有案例, 使用的都是互联网公开数据和本人的判断。"
    "没有任何内部文件或客户数据上传给外部AI工具。",
    fs=15, bold=True, color=WHITE)

# 三栏建议
recs = [
    ("底线工具",
     "微软工具是安全底线: 公司已批准, 先把它用好;"
     "功能比本土产品弱, 但培训后完全够用"),
    ("用法规",
     "公开数据 + 个人判断 = 可接受;"
     "内部文件 + 外部AI = 红线"),
    ("对外发布",
     "AI生成内容对外发布需确认版权归属和准确性;"
     "不能直接以公司名义发布未经审核的内容"),
]
for i, (title, body) in enumerate(recs):
    x = Inches(0.7 + i * 4.17)
    rect(s8, x, Inches(3.45), Inches(3.9), Inches(0.02), fill=LGRAY)
    txt(s8, x, Inches(3.55), Inches(3.9), Inches(0.35),
        title, fs=14, bold=True, color=NAVY)
    txt(s8, x, Inches(3.95), Inches(3.9), Inches(0.9),
        body, fs=12, color=GRAY)

# 外部案例 - 琥珀黄边框
rect(s8, Inches(0.7), Inches(5.1), Inches(12.0), Inches(1.55),
     fill=RGBColor(0xFF, 0xFB, 0xEB),
     line=AMBER, lw=Pt(1.5))
# 标签
rect(s8, Inches(11.0), Inches(5.15), Inches(1.5), Inches(0.28), fill=AMBER)
tb = s8.shapes.add_textbox(Inches(11.0), Inches(5.15), Inches(1.5), Inches(0.28))
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "外部案例"
run.font.size = Pt(9); run.font.bold = True
run.font.color.rgb = WHITE; run.font.name = "Microsoft YaHei"

txt(s8, Inches(0.9), Inches(5.2), Inches(9.8), Inches(0.35),
    "行业参考: Anthropic法务团队的实践", fs=13, bold=True, color=AMBER)
txt(s8, Inches(0.9), Inches(5.55), Inches(11.5), Inches(0.28),
    "来源: Mark Pike, Anthropic Associate General Counsel (公开视频, 非Taylor案例, 非Hach内部实践)",
    fs=10, color=GRAY)
txt(s8, Inches(0.9), Inches(5.85), Inches(11.5), Inches(0.55),
    "* 营销材料合规审查: 周期从数天->数小时    "
    "* AI做风险分级, 律师只复核高风险    "
    "* 人永远在审核链里, AI是过滤器, 不是决策者",
    fs=12, color=DARK)


# ============================================================
# Slide 9: Viewpoint
# ============================================================
s9 = light_slide()
slide_header(s9, "观点", "AI时代, 人的竞争力在哪里?")

# 左栏
txt(s9, Inches(0.7), Inches(2.2), Inches(5.5), Inches(0.35),
    "不能只说乐观的那面", fs=13, bold=True, color=NAVY)
rect(s9, Inches(0.7), Inches(2.55), Inches(1.0), Inches(0.02), fill=LGRAY)

honest = [
    "AI创造新工作, 但转型有时间成本 - "
    "历史上以十年计, 现在以月计",
    "这次最先冲击的不是蓝领, "
    "是文字、分析、初级文件处理",
    "提升AI能力对有些人是真实可行的, "
    "对有些人代价很高",
]
for i, h in enumerate(honest):
    txt(s9, Inches(0.7), Inches(2.72) + Inches(0.58*i),
        Inches(5.8), Inches(0.55), h, fs=12, color=DARK)

# 右栏
txt(s9, Inches(7.2), Inches(2.2), Inches(5.5), Inches(0.35),
    "真正的竞争力", fs=13, bold=True, color=NAVY)
rect(s9, Inches(7.2), Inches(2.55), Inches(1.0), Inches(0.02), fill=TEAL)

comp = [
    ("判断力", "知道AI什么时候是对的, 什么时候在胡说"),
    ("提问力", "能把复杂问题拆解清楚, 告诉AI去做什么"),
    ("行业积累", "这两种能力, 有丰富经验的人天然更强"),
]
for i, (title, desc) in enumerate(comp):
    txt(s9, Inches(7.2), Inches(2.75) + Inches(0.65*i),
        Inches(5.5), Inches(0.35), title, fs=14, bold=True, color=TEAL)
    txt(s9, Inches(7.2), Inches(3.1) + Inches(0.65*i),
        Inches(5.5), Inches(0.35), desc, fs=12, color=GRAY)

# 底部结论
rect(s9, Inches(0.7), Inches(6.3), Inches(12.0), Inches(0.02), fill=TEAL)
txt(s9, Inches(0.7), Inches(6.45), Inches(12.0), Inches(0.5),
    "工具在变, 判断力和提问力是你自己的 - "
    "而这两样东西, 恰恰需要真实的行业经验才能建立。",
    fs=13, italic=True, color=TEAL, align=PP_ALIGN.CENTER)


# ============================================================
# Slide 10: Appendix
# ============================================================
s10 = light_slide()
slide_header(s10, "附录", "推荐学习资源")

resources = [
    ("4D AI Fluency", "Claude.ai官方课程",
     "Delegation(委派) / Description(描述) / Discernment(辨别) / Diligence(尽责)",
     "AI工作流的结果由使用者本人负责, 不是AI, 不是工具"),
    ("Andrew Ng AI课程", "DeepLearning.AI / Coursera",
     "AI Agent原理与设计、LLM应用开发",
     "免费+付费课程均有, 系统性学习"),
    ("Andrej Karpathy", "YouTube / GitHub / Blog",
     "Vibe Coding / LLM Wiki / 2025年度回顾(必读)",
     "2025年出现的东西好好串联, 可以强大10倍 (1400万次浏览)"),
]
for i, (title, source, content, footnote) in enumerate(resources):
    x = Inches(0.7 + i * 4.17)
    txt(s10, x, Inches(2.25), Inches(3.9), Inches(0.35),
        title, fs=15, bold=True, color=NAVY)
    txt(s10, x, Inches(2.6), Inches(3.9), Inches(0.3),
        source, fs=10, color=GRAY)
    rect(s10, x, Inches(2.92), Inches(3.9), Inches(0.02), fill=LGRAY)
    txt(s10, x, Inches(3.0), Inches(3.9), Inches(1.0),
        content, fs=12, color=DARK)
    txt(s10, x, Inches(4.15), Inches(3.9), Inches(0.6),
        footnote, fs=10, italic=True, color=TEAL)

rect(s10, Inches(0.7), Inches(5.8), Inches(12.0), Inches(0.02), fill=LGRAY)
txt(s10, Inches(0.7), Inches(5.95), Inches(12.0), Inches(0.5),
    "AI变化太快, 唯一有效的学习方式是在使用中学习",
    fs=14, bold=True, color=NAVY, align=PP_ALIGN.CENTER)


# ============================================================
# Slide 11: Closing
# ============================================================
s11 = dark_slide()
rect(s11, 0, 0, SLIDE_W, Inches(0.06), fill=TEAL)

txt(s11, Inches(1.5), Inches(2.2), Inches(10.5), Inches(2.0),
    "工具每天都在变\n判断力和提问力\n才是你自己的",
    fs=42, bold=True, color=WHITE)

rect(s11, Inches(1.5), Inches(5.0), Inches(5), Inches(0.025), fill=TEAL)
txt(s11, Inches(1.5), Inches(5.15), Inches(10), Inches(0.45),
    "-- Andrej Karpathy, 2025年12月", fs=14, color=TEAL)


# ── Save ──────────────────────────────────────────────
out = "/home/agentuser/wiki/projects/work-06-ai-sharing/Taylor_AI分享_启动会.pptx"
prs.save(out)
print("Saved:", out)
