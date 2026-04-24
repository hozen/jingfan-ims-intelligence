#!/usr/bin/env python3
"""发送邮件到IMS情报订阅者"""
import smtplib, ssl, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

SMTP_HOST = "smtp.163.com"
SMTP_PORT = 465
SMTP_USER = "hozen@163.com"
SMTP_PASS = "SDmxwwnLJdYCXHyn"

subject = sys.argv[1]
html_body = sys.argv[2]
plain = sys.argv[3] if len(sys.argv) > 3 else ""

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = SMTP_USER
msg["To"] = "leshi@hach.com"

part1 = MIMEText(plain, "plain", "utf-8")
part2 = MIMEText(html_body, "html", "utf-8")
msg.attach(part1)
msg.attach(part2)

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx) as smtp:
    smtp.login(SMTP_USER, SMTP_PASS)
    smtp.sendmail(SMTP_USER, ["leshi@hach.com"], msg.as_bytes())

print("Sent OK")
