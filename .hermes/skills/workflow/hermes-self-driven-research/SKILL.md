---
name: hermes-self-driven-research
description: Hermes姐姐自驱动研究轮循工作流——每30分钟cron运行，检查邮箱，有新邮件则处理，无新邮件则轮循一个work项目继续研究，并汇报给巴菲特。
---

# 自驱动研究工作流

## 触发条件

每30分钟cron自动运行，检查3位发件人（乔布斯、李录、巴菲特）的新邮件。

## 标准工作流

### 第一步：检查邮箱（POP3）
```python
import poplib, email as email_lib, json
from email.header import decode_header

mail = poplib.POP3_SSL('pop.163.com', 995)
mail.user('hozen@163.com')
mail.pass_('QUYwrhcrUN4Bi4ez')

# Get UIDL mapping
response = mail.uidl()
uidl_map = {}
for line in response[1]:
    parts = line.decode().split()
    if len(parts) >= 2:
        uidl_map[int(parts[0])] = parts[1]

# Load processed UIDs (正确路径!)
processed = set(json.load(open('/tmp/processed_emails.json')))
server_uids = set(uidl_map.values())
new_uids = server_uids - processed

# Save updated UIDs immediately
json.dump(list(server_uids), open('/tmp/processed_emails.json', 'w'))
```

**关键点**：
- 用UIDL字符串跟踪已处理邮件，不是顺序号
- 处理完立即保存processed UIDs到`/tmp/processed_emails.json`（注意：不是`_163.json`！）
- 163邮箱用`mail.retr(seq_num)`按顺序号读取，不能用`mail.top(uid)`
- **去重处理**：如果同一个发件人发来多封内容相同的邮件，只处理seq_num最大的那封（最新的），避免重复回复

### 第二步：有新邮件则处理并汇报

**处理优先级**：
1. **李录** — 投资相关，跟进
2. **巴菲特** — 工作指令、问题，跟进并回复
3. **乔布斯** — review请求，记录并回复review意见

**发邮件（SMTP SSL）**：
```python
import smtplib
from email.mime.text import MIMEText
from email.header import Header

msg = MIMEText(body, 'plain', 'utf-8')
msg['From'] = 'hozen@163.com'
msg['To'] = to_addr
msg['Subject'] = Header(subject, 'utf-8')

server = smtplib.SMTP_SSL('smtp.163.com', 465)
server.login('hozen@163.com', 'QUYwrhcrUN4Bi4ez')
server.sendmail('hozen@163.com', to_addr, msg.as_string())
server.quit()
```

**发件目标**：
- 乔布斯 → 279235@qq.com
- 李录 → 69870728@qq.com
- 巴菲特 → hozenshi@hotmail.com

### 第三步：无新邮件时执行自驱动研究

**轮循顺序**：
`work-01 → work-02 → work-03 → work-04 → work-05 → work-06 → work-07 → work-08 → work-09 → 循环`

**工作内容**：
1. 确定下一个work：找到所有work目录，按`research-update-YYYYMMDD-HHMM`目录的mtime排序，选最老的（最近30分钟内未更新的）
2. 读取当前work的README.md或index.html，了解状态和待研究问题
3. 进行研究，产出新的`research-update-YYYYMMDD-HHMM`目录
4. 将研究报告保存到该目录的index.html
5. 汇报给巴菲特

**Wiki路径**：`/home/agentuser/wiki/site/projects/work-04-ims/research-update-YYYYMMDD-HHMM/index.html`

**选择下一个work的逻辑**：
```bash
# 找到所有research-update目录，按mtime排序，选最老的
ls -lt /home/agentuser/wiki/site/projects/work-*/research-update-* 2>/dev/null | head -20
```

### 第四步：汇报给巴菲特

汇报格式：
```
巴菲特，

姐姐自驱动工作汇报如下：

---

## Cron Job 执行报告 | YYYY-MM-DD HH:MM

**当前轮循：work-0X（项目名）**

---

## 一、邮箱监控
## 二、自驱动研究
### 完成：QX 研究内容标题
## 三、下一步

―― 姐姐
YYYY-MM-DD HH:MM
```

**周末规则**：周末只监控邮箱，不发汇报。

## 踩坑记录

1. **UID跟踪必须用文件持久化**：processed_uids存`/tmp/processed_emails.json`，跨session有效
2. **processed文件损坏**：如果processed数量远少于server数量（比如<10%），文件可能损坏，直接用`list(server_uids)`覆盖
3. **周末不发汇报**：周六/周日只处理邮件，不触发汇报邮件
4. **乔布斯重复邮件**：乔布斯会发大量重复review请求，只处理seq_num最大的那封（最新的），其余跳过
5. **Wiki是静态HTML**：不是mdbook源码，直接写HTML文件到`/home/agentuser/wiki/site/projects/work-XX/research-update-YYYYMMDD-HHMM/index.html`

## 环境路径

- Wiki站点：`/home/agentuser/wiki/site/projects/`
- Processed文件：`/tmp/processed_emails.json`
- 授权码：`QUYwrhcrUN4Bi4ez`
