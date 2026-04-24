#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/agentuser/.hermes/scripts')
from send_email import send_email

subject = "彭永臻AOA工艺情报 | 来源说明与获取建议"

html_body = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: Arial, sans-serif; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
  h1 { color: #007EB5; border-bottom: 3px solid #007EB5; padding-bottom: 10px; font-size: 22px; }
  h2 { color: #007EB5; font-size: 15px; margin-top: 25px; }
  .section { background: #f9f9f9; border-left: 4px solid #007EB5; padding: 15px; margin: 15px 0; }
  .warning { border-left: 4px solid #E67E22; background: #FEF9E7; }
  .source { border-left: 4px solid #27AE60; background: #E8F8F5; }
  table { border-collapse: collapse; width: 100%; margin: 10px 0; }
  th { background: #007EB5; color: white; padding: 8px; text-align: left; }
  td { border: 1px solid #ddd; padding: 8px; }
  tr:nth-child(even) { background: #f2f2f2; }
  code { background: #eee; padding: 2px 5px; font-size: 13px; }
  .footer { color: #999; font-size: 11px; text-align: center; margin-top: 40px; border-top: 1px solid #eee; padding-top: 15px; }
</style>
</head>
<body>
<h1>彭永臻AOA工艺情报 | 来源说明</h1>

<div class="section">
<p><strong>信息渠道</strong>：中国水协2026年会综合大会（4月17日，深圳）<br>
<strong>整理时间</strong>：2026-04-22 06:05<br>
<strong>记录方式</strong>：网络实时追踪（搜狗搜索抓取）</p>
</div>

<h2>一、彭永臻报告要点（AOA污水处理新技术）</h2>

<div class="section">
<p><strong>人物背景</strong>：彭永臻，中国工程院院士，北京工业大学教授，中国水协战咨委委员</p>
<table>
  <tr><th width="25%">维度</th><th>内容</th></tr>
  <tr><td><strong>核心工艺</strong></td><td>AOA（Anaerobic-Oxic-Anoxic）新型污水处理工艺</td></tr>
  <tr><td><strong>关键数据</strong></td><td>14.3°C低温条件下，总氮（TN）稳定 &lt; 3.8 mg/L</td></tr>
  <tr><td><strong>对比AAO优势</strong></td><td>① 省曝气能耗；② 减污泥量；③ 降氧化亚氮（N₂O）碳排放</td></tr>
  <tr><td><strong>工艺控制关键</strong></td><td>好氧区曝气控制是减小N₂O排放的关键</td></tr>
  <tr><td><strong>已有试点</strong></td><td>北京高碑店、北京定福庄、合肥王小郢、天津张贵庄</td></tr>
</table>
</div>

<h2>二、IMS视角分析</h2>

<div class="section">
<table>
  <tr><th>分析维度</th><th>内容</th></tr>
  <tr><td><strong>竞争相关性</strong></td><td>非竞争。AOA是工艺段技术，Hach在线水质仪表（总氮、溶解氧、氨氮等）受益于深度脱氮需求。</td></tr>
  <tr><td><strong>产品机会</strong></td><td>① NT6800总氮在线监测仪直接受益于深度脱氮改造；② 好氧区曝气精确控制需要溶解氧仪表高频数据；③ N₂O减排监测或成新兴需求。</td></tr>
  <tr><td><strong>试点跟进建议</strong></td><td>北京/合肥/天津试点污水厂的仪表采购情况值得跟踪。</td></tr>
</table>
</div>

<h2>三、关于"原始论文"的说明</h2>

<div class="section warning">
<p><strong>⚠️ 当前文件 ≠ 原始学术论文</strong></p>
<p>以上内容来自中国水协2026年会网络追踪的速记式记录，是演讲现场抓取的要点，非彭永臻团队的正式发表论文。如需原始论文，建议通过以下渠道获取：</p>
<ol>
  <li><strong>中国知网（CNKI）</strong>：搜索"彭永臻 AOA 工艺"或"Anoxic-Oxic-Anoxic" —— 彭永臻团队近年发表多篇相关论文</li>
  <li><strong>北京工业大学环境与能源工程学院官网</strong>：彭永臻教授个人主页通常有论文列表</li>
  <li><strong>Water Research / Environmental Science &amp; Technology</strong>：彭永臻团队在英文期刊也有相关发表</li>
  <li><strong>中国水协</strong>：可联系<a href="mailto:ieexpo@mm-zm.com">ieexpo@mm-zm.com</a>获取演讲资料</li>
</ol>
</div>

<div class="section source">
<p><strong>信息来源</strong>：搜狗搜索抓取 · 中国水协官网 · 中新网 · 腾讯ima</p>
</div>

<div class="footer">本报告内容由AI辅助整理，仅供参考<br>Generated: 2026-04-22 · 水协2026年会监控脚本</div>
</body>
</html>"""

plain = """彭永臻AOA工艺情报 | 来源说明

信息渠道：中国水协2026年会综合大会（4月17日，深圳）
整理时间：2026-04-22

【报告要点】彭永臻（北京工业大学）- AOA污水处理新技术
- AOA工艺：中低温污水深度脱氮，14.3°C低温下总氮<3.8mg/L
- 对比传统AAO：省曝气能耗、减污泥量、降氧化亚氮（N2O）碳排放
- 已有试点：北京高碑店/定福庄、合肥王小郢、天津张贵庄
- 好氧区曝气控制是减小N2O排放关键

【IMS视角】
- 非竞争，工艺段技术，Hach在线仪表（NT6800总氮/溶解氧/氨氮）受益
- 深度脱氮改造驱动总氮在线监测需求上升
- 试点污水厂仪表采购情况值得跟踪

【重要说明】当前文件来自中国水协年会追踪速记，非彭永臻原始学术论文。
如需原始论文建议：
1. 中国知网（CNKI）搜索"彭永臻 AOA"
2. 北京工业大学官网彭永臻教授主页
3. Water Research / ES&amp;T 等英文期刊
4. 联系中国水协获取演讲资料

详见HTML版本。"""

result = send_email(subject, html_body, plain)
print(result)