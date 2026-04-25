# -*- coding: utf-8 -*-
"""
Work-06: Taylor AI分享启动会PPT
11 slides
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

# colors
NAVY     = RGBColor(0x1A, 0x2B, 0x4A)
TEAL     = RGBColor(0x0D, 0x94, 0x88)
AMBER    = RGBColor(0xF5, 0x9E, 0x0B)
LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
DARK     = RGBColor(0x1E, 0x29, 0x3B)
GRAY     = RGBColor(0x64, 0x74, 0x8B)
LGRAY    = RGBColor(0xE2, 0xE8, 0xF0)
CARD_BG  = RGBColor(0xF1, 0xF5, 0xF9)
NAVY2    = RGBColor(0x2D, 0x3E, 0x5C)
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
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    else:
        sh.fill.background()
    if line:
        sh.line.color.rgb = line
        if lw:
            sh.line.width = lw
    else:
        sh.line.fill.background()
    return sh

def txt(slide, l, t, w, h, text, fs=14, bold=False, color=DARK,
        align=PP_ALIGN.LEFT, name="Microsoft YaHei", italic=False):
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

def tag(slide, label, l, t, bg=TEAL, fg=WHITE, w=None, h=Inches(0.32)):
    if w is None:
        w = Inches(len(label) * 0.14 + 0.3)
    rect(slide, l, t, w, h, fill=bg)
    tb = slide.shapes.add_textbox(l, t, w, h)
    tb.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    p = tb.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = label
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = fg
    run.font.name = "Microsoft YaHei"

def keyinfo(slide, text):
    tb = txt(slide, Inches(0.5), SLIDE_H - Inches(0.7),
              SLIDE_W - Inches(1), Inches(0.4),
              text=text, fs=13, color=TEAL, italic=True)

def card(slide, l, t, w, h, fill=CARD_BG, line=LGRAY, lw=Pt(1)):
    sh = rect(slide, l, t, w, h, fill=fill, line=line, lw=lw)
    try:
        spPr = sh._sp.spPr
        pg = spPr.find(qn('a:prstGeom'))
        if pg is not None:
            pg.set('prst', 'roundRect')
            av = pg.find(qn('a:avLst'))
            if av is None:
                av = etree.SubElement(pg, qn('a:avLst'))
            gd = av.find(qn('a:gd'))
            if gd is None:
                gd = etree.SubElement(av, qn('a:gd'))
            gd.set('name', 'adj')
            gd.set('fmla', 'val 10000')
    except:
        pass
    return sh

def light_slide():
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, fill=LIGHT_BG)
    return s

def dark_slide():
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, fill=NAVY)
    return s


# ============================================================
# Slide 1: Cover
# ============================================================
s1 = dark_slide()
rect(s1, 0, 0, SLIDE_W, Inches(0.08), fill=TEAL)

txt(s1, Inches(0.8), Inches(2.2), Inches(11.5), Inches(1.2),
    "在使用中学习 AI", fs=44, bold=True, color=WHITE)
txt(s1, Inches(0.8), Inches(3.4), Inches(9), Inches(0.6),
    "三个月实践 / 真实案例 / 诚实的踩坑", fs=20, color=TEAL)
txt(s1, Inches(0.8), Inches(4.2), Inches(10), Inches(0.5),
    "Taylor | Hach China iMS业务负责人 & China AI技术联系人 | 2026",
    fs=14, color=RGBColor(0x94, 0xA3, 0xB8))

tags = [("开场打破认知", TEAL), ("四个业务场景", TEAL),
        ("诚实的部分", AMBER), ("附录学习资源", GRAY)]
for i, (t, c) in enumerate(tags):
    x = Inches(0.8 + i * 2.9)
    rect(s1, x, Inches(6.3), Inches(2.6), Inches(0.45),
         fill=RGBColor(0x2D, 0x3E, 0x5C), line=c, lw=Pt(1))
    tb = s1.shapes.add_textbox(x, Inches(6.3), Inches(2.6), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = t
    run.font.size = Pt(11); run.font.bold = True
    run.font.color.rgb = c; run.font.name = "Microsoft YaHei"


# ============================================================
# Slide 2: Opening story
# ============================================================
s2 = light_slide()
tag(s2, "开场", Inches(0.5), Inches(0.35))
txt(s2, Inches(0.5), Inches(0.75), Inches(12), Inches(0.7),
    "打破认知：过年三天，做出一个App", fs=32, bold=True, color=NAVY)

card(s2, Inches(0.5), Inches(1.55), Inches(5.8), Inches(4.3))
txt(s2, Inches(0.7), Inches(1.7), Inches(5.4), Inches(0.4),
    "真实故事", fs=13, bold=True, color=TEAL)
story = [
    "  * 春节放假在家, Claude Code刚上线",
    "  * 目标: 把多年培训视频和资料做成一个App",
    "  * 结果: 类YouTube界面 + 文档 + 记忆卡片",
    "  * 两三天上线, 同事直呼不可思议",
]
for i, line in enumerate(story):
    txt(s2, Inches(0.7), Inches(2.15) + Inches(0.45*i),
        Inches(5.4), Inches(0.45), line, fs=13, color=DARK)

card(s2, Inches(6.7), Inches(1.55), Inches(6.0), Inches(4.3),
     fill=NAVY, line=NAVY)
txt(s2, Inches(6.9), Inches(1.75), Inches(5.6), Inches(0.4),
    "传统原生开发 vs AI辅助开发", fs=13, bold=True, color=TEAL)
rows = [
    ("传统原生开发", "AI辅助开发", True),
    ("专人开发", "非专业人员", False),
    ("6-12个月", "2-3天", False),
    ("成本极高", "零额外成本", False),
]
for i, (l, r, hdr) in enumerate(rows):
    y = Inches(2.25) + Inches(0.52*i)
    fc = WHITE if hdr else RGBColor(0x94, 0xA3, 0xB8)
    txt(s2, Inches(6.9), y, Inches(2.6), Inches(0.45),
        l, fs=13, bold=hdr, color=fc)
    txt(s2, Inches(9.6), y, Inches(2.8), Inches(0.45),
        r, fs=13, bold=hdr, color=TEAL)

rect(s2, Inches(9.5), Inches(2.2), Inches(0.04), Inches(2.2), fill=LGRAY)
keyinfo(s2, "AI不只是辅助写作, 它让不可能变得可能")


# ============================================================
# Slide 3: Scene 1 - Competitive Intelligence
# ============================================================
s3 = light_slide()
tag(s3, "场景一", Inches(0.5), Inches(0.35))
txt(s3, Inches(0.5), Inches(0.75), Inches(12), Inches(0.65),
    "竞品情报收集", fs=32, bold=True, color=NAVY)
txt(s3, Inches(0.5), Inches(1.35), Inches(4), Inches(0.35),
    "适用部门: 市场 / 服务 / 销售", fs=12, color=GRAY)

card(s3, Inches(0.5), Inches(1.8), Inches(5.9), Inches(4.5))
txt(s3, Inches(0.7), Inches(1.95), Inches(5.5), Inches(0.4),
    "环博会 2026 (上海浦东)", fs=14, bold=True, color=NAVY)
steps_l = ["1. 录音笔录制讲座", "2. AI自动转文字", "3. AI搜索整理信息", "4. 生成竞品分析PPT"]
for i, s in enumerate(steps_l):
    txt(s3, Inches(0.7), Inches(2.45) + Inches(0.48*i),
        Inches(5.5), Inches(0.42), s, fs=13, color=DARK)
txt(s3, Inches(0.7), Inches(4.45), Inches(5.5), Inches(0.4),
    "覆盖100+参展企业, 包含技术趋势分析",
    fs=11, italic=True, color=GRAY)

card(s3, Inches(6.8), Inches(1.8), Inches(6.0), Inches(4.5))
txt(s3, Inches(7.0), Inches(1.95), Inches(5.6), Inches(0.4),
    "水协2026年会 (远程跟踪)", fs=14, bold=True, color=NAVY)
steps_r = ["1. 设置定时爬取任务", "2. 每6小时自动运行", "3. 整理最新发布信息", "4. 邮件推送到本人"]
for i, s in enumerate(steps_r):
    txt(s3, Inches(7.0), Inches(2.45) + Inches(0.48*i),
        Inches(5.6), Inches(0.42), s, fs=13, color=DARK)
txt(s3, Inches(7.0), Inches(4.45), Inches(5.6), Inches(0.4),
    "即使不在现场, 也能接近身临其境",
    fs=11, italic=True, color=GRAY)

keyinfo(s3, "AI是信息密度的放大器, 不是替代判断的工具")


# ============================================================
# Slide 4: Scene 2 - Document Workflow
# ============================================================
s4 = light_slide()
tag(s4, "场景二", Inches(0.5), Inches(0.35))
txt(s4, Inches(0.5), Inches(0.75), Inches(12), Inches(0.65),
    "文档工作流", fs=32, bold=True, color=NAVY)
txt(s4, Inches(0.5), Inches(1.35), Inches(4), Inches(0.35),
    "适用部门: 市场 / 财务 / 法务 / 所有人", fs=12, color=GRAY)

steps = [
    ("步骤1", "起草", "人写模板\n和思路", NAVY),
    ("步骤2", "生成", "AI按模板\n填充初稿", TEAL),
    ("步骤3", "审核", "人工Review\n修正细节", TEAL),
    ("步骤4", "输出", "文档完成\n直接生成PPT", NAVY),
]
for i, (step, name, desc, sc) in enumerate(steps):
    x = Inches(0.7) + Inches(i * 3.1)
    rect(s4, x, Inches(1.85), Inches(2.6), Inches(1.6), fill=sc)
    txt(s4, x, Inches(1.9), Inches(2.6), Inches(0.45),
        step, fs=11, bold=True,
        color=TEAL if sc == NAVY else WHITE, align=PP_ALIGN.CENTER)
    txt(s4, x, Inches(2.25), Inches(2.6), Inches(0.5),
        name, fs=18, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    txt(s4, x, Inches(2.75), Inches(2.6), Inches(0.55),
        desc, fs=11,
        color=RGBColor(0xCB, 0xD5, 0xE1) if sc == NAVY else WHITE,
        align=PP_ALIGN.CENTER)
    if i < 3:
        txt(s4, x + Inches(2.6), Inches(2.35), Inches(0.5), Inches(0.4),
            "->", fs=22, color=TEAL, align=PP_ALIGN.CENTER)

card(s4, Inches(0.5), Inches(3.75), Inches(12.3), Inches(1.35),
     fill=CARD_BG, line=TEAL, lw=Pt(2))
txt(s4, Inches(0.7), Inches(3.9), Inches(2.5), Inches(0.35),
    "真实案例", fs=12, bold=True, color=TEAL)
txt(s4, Inches(0.7), Inches(4.25), Inches(11.8), Inches(0.65),
    "产品经理陈涛: 以往写一份授权文档需要数天反复修改; "
    "现在思路清晰时, 半天到一个晚上完成文档, 再直接生成PPT, "
    "两三次确认即可发给客户。", fs=13, color=DARK)

keyinfo(s4, "人定方向, AI填内容 - 这个分工适用于所有部门")


# ============================================================
# Slide 5: Scene 3 - Agent & Quality Control
# ============================================================
s5 = light_slide()
tag(s5, "场景三", Inches(0.5), Inches(0.35))
txt(s5, Inches(0.5), Inches(0.75), Inches(12), Inches(0.65),
    "自主Agent与质量管控", fs=32, bold=True, color=NAVY)
txt(s5, Inches(0.5), Inches(1.35), Inches(5), Inches(0.35),
    "适用部门: IT / 法务 - 了解AI如何被管理", fs=12, color=GRAY)

card(s5, Inches(0.5), Inches(1.8), Inches(5.9), Inches(4.5), fill=NAVY, line=NAVY)
txt(s5, Inches(0.7), Inches(1.95), Inches(5.5), Inches(0.4),
    "Agent工作方式", fs=14, bold=True, color=TEAL)
agent = [
    "* 每4小时自动运行一次",
    "* 覆盖线索扫描 + 竞品监控",
    "* 串行执行, 一次只做一件事",
    "* 仅推送到dev分支, 经审核才合并主线",
    "* 每次运行留下审计日志",
]
for i, item in enumerate(agent):
    txt(s5, Inches(0.7), Inches(2.45) + Inches(0.45*i),
        Inches(5.5), Inches(0.42), item, fs=13, color=WHITE)

card(s5, Inches(6.8), Inches(1.8), Inches(6.0), Inches(4.5))
txt(s5, Inches(7.0), Inches(1.95), Inches(5.6), Inches(0.4),
    "质量门控机制", fs=14, bold=True, color=NAVY)
qa = [
    "+ 数据完整性审计: 17个问题识别并修复",
    "+ 置信度强制标注: 高 / 中 / 低 三级",
    "+ 信息源类型标注: 官方 / 媒体 / 推断",
    "+ 人工审核节点: Taylor每轮审核确认",
]
for i, item in enumerate(qa):
    txt(s5, Inches(7.0), Inches(2.45) + Inches(0.50*i),
        Inches(5.6), Inches(0.42), item, fs=13, color=DARK)

keyinfo(s5, "AI系统不是黑箱 - 可以被设计、被审计、被管理")


# ============================================================
# Slide 6: Scene 4 - Data Analysis
# ============================================================
s6 = light_slide()
tag(s6, "场景四", Inches(0.5), Inches(0.35))
txt(s6, Inches(0.5), Inches(0.75), Inches(12), Inches(0.65),
    "数据分析与预测", fs=32, bold=True, color=NAVY)
txt(s6, Inches(0.5), Inches(1.35), Inches(5), Inches(0.35),
    "案例: 居家桥水厂 / 传感器数据分析", fs=12, color=GRAY)

card(s6, Inches(0.5), Inches(1.8), Inches(6.5), Inches(4.5))
findings = [
    "1. 分析6个月传感器数据, 发现5个人工看不见的异常",
    "2. 核心发现: FreeNH4可提前3-7天预警试剂瓶故障",
    "3. 两次历史故障均成功回测, 150天无误报",
    "4. 检测规则自动激活, 无需客户手动配置",
]
for i, f in enumerate(findings):
    txt(s6, Inches(0.7), Inches(2.0) + Inches(0.55*i),
        Inches(6.1), Inches(0.5), f, fs=13, color=DARK)

card(s6, Inches(7.4), Inches(1.8), Inches(5.4), Inches(2.0), fill=TEAL, line=TEAL)
txt(s6, Inches(7.4), Inches(1.95), Inches(5.4), Inches(0.35),
    "提前预警周期", fs=12, color=WHITE, align=PP_ALIGN.CENTER)
txt(s6, Inches(7.4), Inches(2.25), Inches(5.4), Inches(0.9),
    "3-7天", fs=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s6, Inches(7.4), Inches(3.1), Inches(5.4), Inches(0.35),
    "居家桥水厂实测", fs=11, color=TEAL_L, align=PP_ALIGN.CENTER)

card(s6, Inches(7.4), Inches(4.05), Inches(5.4), Inches(2.0), fill=NAVY, line=NAVY)
txt(s6, Inches(7.4), Inches(4.2), Inches(5.4), Inches(0.35),
    "150天内误报次数", fs=12, color=TEAL, align=PP_ALIGN.CENTER)
txt(s6, Inches(7.4), Inches(4.5), Inches(5.4), Inches(0.9),
    "0次", fs=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s6, Inches(7.4), Inches(5.35), Inches(5.4), Inches(0.35),
    "FreeNH4传感器规则", fs=11, color=RGBColor(0x94, 0xA3, 0xB8),
    align=PP_ALIGN.CENTER)

keyinfo(s6, "AI发现人看不见的规律, 但验证和决策仍由人完成")


# ============================================================
# Slide 7: Pitfalls
# ============================================================
s7 = light_slide()
tag(s7, "诚实的部分", Inches(0.5), Inches(0.35), bg=AMBER, fg=WHITE)
txt(s7, Inches(0.5), Inches(0.75), Inches(12), Inches(0.65),
    "我踩过的坑", fs=32, bold=True, color=NAVY)

card(s7, Inches(0.5), Inches(1.8), Inches(6.1), Inches(4.5),
     fill=RGBColor(0xFF, 0xFB, 0xEB), line=AMBER, lw=Pt(2))
txt(s7, Inches(0.7), Inches(1.95), Inches(5.7), Inches(0.4),
    "踩坑案例: 客户联系人数据收集", fs=13, bold=True, color=AMBER)
pitfalls = [
    "1. AI返回了一批联系人数据",
    "2. 要求说明来源 -> 称来自搜索引擎缓存页",
    "3. 去验证 -> 找不到缓存页面入口",
    "4. 数据真实性无法确认",
]
for i, p in enumerate(pitfalls):
    txt(s7, Inches(0.7), Inches(2.4) + Inches(0.48*i),
        Inches(5.7), Inches(0.42), p, fs=13, color=DARK)
rect(s7, Inches(0.7), Inches(4.3), Inches(5.7), Inches(0.05), fill=AMBER)
txt(s7, Inches(0.7), Inches(4.4), Inches(5.7), Inches(0.5),
    "结论: AI幻觉在数据领域真实存在, 不能盲目信任",
    fs=12, bold=True, color=RGBColor(0xB4, 0x53, 0x0C))

card(s7, Inches(6.9), Inches(1.8), Inches(5.9), Inches(4.5), fill=NAVY, line=NAVY)
txt(s7, Inches(7.1), Inches(1.95), Inches(5.5), Inches(0.4),
    "我的工作原则", fs=13, bold=True, color=AMBER)
principles = [
    "+ 只用公开数据与外部AI交互",
    "+ 内部文件 / 客户数据绝不上传外部AI",
    "+ AI负责初稿, 人负责验证和决策",
    "+ 结果由使用者本人负责",
]
for i, pr in enumerate(principles):
    txt(s7, Inches(7.1), Inches(2.45) + Inches(0.52*i),
        Inches(5.5), Inches(0.42), pr, fs=13, color=WHITE)

keyinfo(s7, "AI幻觉是真实存在的 - 人的判断永远不能被绕过")


# ============================================================
# Slide 8: Legal Conclusion
# ============================================================
s8 = light_slide()
tag(s8, "给法务的结论", Inches(0.5), Inches(0.35), bg=NAVY)
txt(s8, Inches(0.5), Inches(0.75), Inches(12), Inches(0.65),
    "今天所有案例的共同底线", fs=32, bold=True, color=NAVY)

rect(s8, Inches(0.5), Inches(1.6), Inches(12.3), Inches(1.1), fill=TEAL)
txt(s8, Inches(0.7), Inches(1.72), Inches(11.9), Inches(0.9),
    "今天分享的所有案例, 使用的都是互联网公开数据和本人的判断。"
    "没有任何内部文件或客户数据上传给外部AI工具。",
    fs=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

recs = [
    ("底线工具", "微软工具是安全底线: 公司已批准, 先把它用好;"
     "功能比本土产品弱, 但培训后完全够用"),
    ("用法规", "公开数据 + 个人判断 = 可接受;"
     "内部文件 + 外部AI = 红线"),
    ("对外发布", "AI生成内容对外发布需确认版权归属和准确性;"
     "不能直接以公司名义发布未经审核的内容"),
]
for i, (title, body) in enumerate(recs):
    x = Inches(0.5) + Inches(i * 4.17)
    card(s8, x, Inches(2.95), Inches(3.95), Inches(1.9))
    txt(s8, x + Inches(0.15), Inches(3.1), Inches(3.65), Inches(0.35),
        title, fs=12, bold=True, color=TEAL)
    txt(s8, x + Inches(0.15), Inches(3.45), Inches(3.65), Inches(1.2),
        body, fs=12, color=DARK)

# external reference card
card(s8, Inches(0.5), Inches(5.05), Inches(12.3), Inches(1.7),
     fill=RGBColor(0xFF, 0xFB, 0xEB), line=AMBER, lw=Pt(2))
rect(s8, Inches(11.3), Inches(5.1), Inches(1.4), Inches(0.32), fill=AMBER)
tb = s8.shapes.add_textbox(Inches(11.3), Inches(5.1), Inches(1.4), Inches(0.32))
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "外部案例"
run.font.size = Pt(10); run.font.bold = True
run.font.color.rgb = WHITE; run.font.name = "Microsoft YaHei"

txt(s8, Inches(0.7), Inches(5.15), Inches(10.4), Inches(0.35),
    "行业参考: Anthropic法务团队的实践", fs=13, bold=True, color=AMBER)
txt(s8, Inches(0.7), Inches(5.5), Inches(11.8), Inches(0.28),
    "来源: Mark Pike, Anthropic Associate General Counsel (公开视频, 非Taylor案例, 非Hach内部实践)",
    fs=10, color=GRAY)
txt(s8, Inches(0.7), Inches(5.8), Inches(11.8), Inches(0.65),
    "* 营销材料合规审查: 周期从数天缩短到数小时    "
    "* AI做风险分级, 律师只复核高风险    "
    "* 人永远在审核链里, AI是过滤器, 不是决策者",
    fs=12, color=DARK)


# ============================================================
# Slide 9: Viewpoint
# ============================================================
s9 = light_slide()
tag(s9, "观点", Inches(0.5), Inches(0.35), bg=NAVY)
txt(s9, Inches(0.5), Inches(0.75), Inches(12), Inches(0.65),
    "AI时代, 人的竞争力在哪里?", fs=32, bold=True, color=NAVY)

card(s9, Inches(0.5), Inches(1.8), Inches(5.9), Inches(4.4))
txt(s9, Inches(0.7), Inches(1.95), Inches(5.5), Inches(0.4),
    "不能只说乐观的那面", fs=14, bold=True, color=NAVY)
honest = [
    "* AI创造新工作, 但转型有时间成本 - "
    "历史上以十年计, 现在以月计",
    "* 这次最先冲击的不是蓝领, "
    "是文字、分析、初级文件处理",
    "* 提升AI能力对有些人是真实可行的, "
    "对有些人代价很高",
]
for i, h in enumerate(honest):
    txt(s9, Inches(0.7), Inches(2.45) + Inches(0.58*i),
        Inches(5.5), Inches(0.55), h, fs=12, color=DARK)

card(s9, Inches(6.8), Inches(1.8), Inches(5.9), Inches(4.4), fill=TEAL, line=TEAL)
txt(s9, Inches(7.0), Inches(1.95), Inches(5.5), Inches(0.4),
    "真正的竞争力", fs=14, bold=True, color=WHITE)
comp = [
    ("判断力", "知道AI什么时候是对的, 什么时候在胡说"),
    ("提问力", "能把复杂问题拆解清楚, 告诉AI去做什么"),
    ("行业积累", "这两种能力, 有丰富经验的人天然更强"),
]
for i, (title, desc) in enumerate(comp):
    txt(s9, Inches(7.0), Inches(2.5) + Inches(0.72*i),
        Inches(5.5), Inches(0.35), title, fs=13, bold=True, color=WHITE)
    txt(s9, Inches(7.0), Inches(2.85) + Inches(0.72*i),
        Inches(5.5), Inches(0.35), desc, fs=12, color=TEAL_L)

rect(s9, Inches(0.5), Inches(6.35), Inches(12.3), Inches(0.05), fill=TEAL)
txt(s9, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.55),
    "工具在变, 判断力和提问力是你自己的 - "
    "而这两样东西, 恰恰需要真实的行业经验才能建立。",
    fs=13, italic=True, color=TEAL, align=PP_ALIGN.CENTER)


# ============================================================
# Slide 10: Appendix - Resources
# ============================================================
s10 = light_slide()
tag(s10, "附录", Inches(0.5), Inches(0.35), bg=GRAY, fg=WHITE)
txt(s10, Inches(0.5), Inches(0.75), Inches(12), Inches(0.65),
    "推荐学习资源", fs=32, bold=True, color=NAVY)

resources = [
    ("4D AI Fluency框架", "Claude.ai官方课程",
     "Delegation(委派) / Description(描述) /\nDiscernment(辨别) / Diligence(尽责)",
     "AI工作流的结果由使用者本人负责, 不是AI, 不是工具"),
    ("Andrew Ng AI课程", "DeepLearning.AI / Coursera",
     "AI Agent原理与设计、LLM应用开发",
     "免费+付费课程均有, 系统性学习"),
    ("Andrej Karpathy", "YouTube / GitHub / Blog",
     "Vibe Coding / LLM Wiki / 2025年度回顾(必读)",
     "2025年出现的东西好好串联, 可以强大10倍 (1400万次浏览)"),
]
for i, (title, source, content, footnote) in enumerate(resources):
    x = Inches(0.5) + Inches(i * 4.17)
    card(s10, x, Inches(1.7), Inches(3.95), Inches(3.9))
    txt(s10, x + Inches(0.15), Inches(1.85), Inches(3.65), Inches(0.4),
        title, fs=13, bold=True, color=NAVY)
    txt(s10, x + Inches(0.15), Inches(2.25), Inches(3.65), Inches(0.3),
        source, fs=10, color=GRAY)
    rect(s10, x + Inches(0.15), Inches(2.6), Inches(3.65), Inches(0.04), fill=TEAL)
    txt(s10, x + Inches(0.15), Inches(2.7), Inches(3.65), Inches(1.4),
        content, fs=12, color=DARK)
    txt(s10, x + Inches(0.15), Inches(4.25), Inches(3.65), Inches(0.8),
        footnote, fs=10, italic=True, color=TEAL)

rect(s10, Inches(0.5), Inches(5.85), Inches(12.3), Inches(0.05), fill=LGRAY)
txt(s10, Inches(0.5), Inches(6.0), Inches(12.3), Inches(0.55),
    "AI变化太快, 唯一有效的学习方式是在使用中学习",
    fs=14, bold=True, color=NAVY, align=PP_ALIGN.CENTER)


# ============================================================
# Slide 11: Closing
# ============================================================
s11 = dark_slide()
rect(s11, 0, 0, SLIDE_W, Inches(0.08), fill=TEAL)

txt(s11, Inches(1.5), Inches(2.0), Inches(10.5), Inches(2.2),
    "工具每天都在变\n判断力和提问力\n才是你自己的",
    fs=38, bold=True, color=WHITE)
txt(s11, Inches(1.5), Inches(5.3), Inches(10.5), Inches(0.45),
    "-- Andrej Karpathy, 2025年12月",
    fs=14, color=TEAL)


# ============================================================
# Save
# ============================================================
out = "/home/agentuser/wiki/projects/work-06-ai-sharing/Taylor_AI分享_启动会.pptx"
prs.save(out)
print("Saved:", out)
