---
name: cron-email-checker
description: Cron job template for checking emails via POP3 with local processed-ID tracking
category: cronjob
---

# Cron Email Checker Skill

## Trigger
Use when setting up a cron job to check emails via POP3 and track processed IDs locally.

## Steps

### 1. POP3 Email Check Template
```python
import poplib
import email
from email.header import decode_header
import json
import os

def decode_str(s):
    if s is None:
        return ''
    parts = decode_header(s)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try:
                charset = charset or 'utf-8'
                result.append(part.decode(charset, errors='replace'))
            except:
                result.append(part.decode('utf-8', errors='replace'))
        else:
            result.append(str(part))
    return ''.join(result)

def get_body(msg):
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == 'text/plain':
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    body = part.get_payload(decode=True).decode(charset, errors='replace')
                    break
                except:
                    pass
    else:
        try:
            charset = msg.get_content_charset() or 'utf-8'
            body = msg.get_payload(decode=True).decode(charset, errors='replace')
        except:
            pass
    return body

# Connect
mail = poplib.POP3_SSL('pop.163.com', 995)
mail.user('your-email@163.com')
mail.pass_('your-password')

# Get email count
num_messages = len(mail.list()[1])

# List all email IDs
responses = mail.list()
email_list = []
for item in responses[1]:
    parts = item.decode().split()
    email_id = int(parts[0])
    email_list.append(email_id)
email_list.sort(reverse=True)
```

### 2. Load Processed IDs
```python
# CRITICAL: Use /home/agentuser/.hermes/ path, NOT /root/.hermes/
PROCESSED_PATH = '/home/agentuser/.hermes/cron/output/processed_emails.json'

processed = set()
if os.path.exists(PROCESSED_PATH):
    with open(PROCESSED_PATH, 'r') as f:
        processed = set(json.load(f))
```

### 3. Filter and Process New Emails
```python
for eid in email_list:
    if str(eid) in processed:
        continue
    # Check sender, process email...
```

### 4. Save Processed IDs
```python
with open(PROCESSED_PATH, 'w') as f:
    json.dump(list(processed_ids), f)
```

## Pitfalls

### Path Resolution Issue
- Cron jobs run as `agentuser` (uid=1001), home is `/home/agentuser`
- The path `~/.hermes/cron/output/` in cron prompts expands to `/home/agentuser/.hermes/cron/output/`
- **DO NOT** use `/root/.hermes/` paths — they are not writable from the cron agent context
- **VERIFIED writable path**: `/home/agentuser/.hermes/cron/output/`

### execute_code Sandbox File Persistence
- **CRITICAL**: Files written via `execute_code`'s `write_file` tool or Python's `open()` in a sandboxed script do NOT persist to the real filesystem — they write to a temporary overlay that gets discarded after the script completes
- To actually persist files (like processed_emails.json), you MUST use the `terminal()` tool with shell commands (e.g., `cat > path << 'EOF'`)
- Workaround: Do all POP3 logic in one execute_code call, but use terminal() to write the processed_ids JSON

### Email ID Storage Format
- Processed email IDs are stored as **strings** in JSON (e.g., `"1"`, `"2"`, not `1`, `2`)
- When comparing, convert: `if eid not in processed_ids` where `processed_ids` is a `set(str)`

### POP3 SSL Port
- Use port `995` with `POP3_SSL` for 163.com

### Email Body Decoding
- Always try multiple charsets (utf-8, gb2312, gbk) when decoding
- Use `errors='replace'` to handle malformed characters
