---
name: email-send-163
description: Send emails via 163.com SMTP using the working password from cron jobs
version: 1.0.0
author: Hermes
metadata:
  hermes:
    tags: [email, smtp, 163.com]
prerequisites:
  environment_variables:
    - EMAIL_ADDRESS
---

# Email Send Skill (163.com)

## Key Discovery

**Important**: 163.com has TWO passwords:
- `.env` file stored password: does NOT work for SMTP send
- Cron job password `QUYwrhcrUN4Bi4ez`: WORKS

Always use the cron job password for sending emails.

## Send Email Script

## Agent Contact Emails

| Agent | Email | Description |
|-------|-------|-------------|
| Hermes姐姐 | hozen@163.com | Agent-A, sender |
| 乔布斯 (Steve Jobs) | 279235@qq.com | Agent-B |
| Mr. Buffett | hozenshi@hotmail.com | 老板, boss |

## Usage

```bash
# Send to 乔布斯
python3 ~/.hermes/scripts/send_email.py --to "279235@qq.com" --subject "Subject" --body "Body"

# Send to Mr. Buffett
python3 ~/.hermes/scripts/send_email.py --to "hozenshi@hotmail.com" --subject "Subject" --body "Body"
```

## Python Usage

```python
import smtplib
from email.mime.text import MIMEText

email_addr = "hozen@163.com"
email_pass = "QUYwrhcrUN4Bi4ez"  # cron job password
smtp_host = "smtp.163.com"
smtp_port = 465

msg = MIMEText("Email body", "plain", "utf-8")
msg["Subject"] = "Subject"
msg["From"] = email_addr
msg["To"] = "recipient@example.com"

server = smtplib.SMTP_SSL(smtp_host, smtp_port)
server.login(email_addr, email_pass)
server.sendmail(email_addr, ["recipient@example.com"], msg.as_string())
server.quit()
```

## If SMTP Fails

1. Check if password is correct - try `QUYwrhcrUN4Bi4ez`
2. For 163.com, you need an **app password** (not login password)
3. Generate app password in 163.com email settings → POP3/SMTP settings