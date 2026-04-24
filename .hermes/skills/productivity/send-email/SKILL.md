---
name: send-email
description: 发送邮件到指定邮箱。使用163邮箱SMTP服务，支持HTML和纯文本双格式。发件人：hozen@163.com
triggers:
  - "发邮件到"
  - "发送邮件"
  - "send.*email"
  - "发个邮件"
---

# send-email 技能

## 用途
通过163邮箱SMTP发送邮件，支持HTML格式和纯文本双格式。

## 凭证
- SMTP服务器: smtp.163.com
- SMTP端口: 465 (SSL)
- 用户名: hozen@163.com
- 密码: SDmxwwnLJdYCXHyn

## 使用方法

### Python调用方式（推荐）
```python
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = "smtp.163.com"
SMTP_PORT = 465
SMTP_USER = "hozen@163.com"
SMTP_PASS = "SDmxwwnLJdYCXHyn"

def send_email(subject, html_body, plain_body="", to_email=None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email or "leshi@hach.com"
    
    part1 = MIMEText(plain_body, "plain", "utf-8")
    part2 = MIMEText(html_body, "html", "utf-8")
    msg.attach(part1)
    msg.attach(part2)
    
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.sendmail(SMTP_USER, [to_email], msg.as_bytes())
    print("Sent OK")

# 示例
send_email(
    subject="闻泰科技监控简报 2026-04-25",
    html_body="<html><body><h1>简报内容</h1></body></html>",
    plain_body="简报内容",
    to_email="13917662032@139.com"
)
```

### 命令行调用方式
```bash
python3 /home/agentuser/.hermes/scripts/send_email.py "邮件标题" "<html内容>" "<纯文本内容>"
```

## 常用收件人
- Hach内部: leshi@hach.com
- 用户个人邮箱: 13917662032@139.com

## 注意事项
- HTML邮件需要有`<html><body>...</body></html>`标签
- 纯文本版本不能为空（至少传一个空格或简单文本）
- 如果收件人填错了，邮件会发送失败（检查域名是否正确）
