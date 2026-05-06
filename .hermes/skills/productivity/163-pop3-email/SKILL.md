---
name: 163-pop3-email
description: Connect to 163.com邮箱 via POP3 SSL to check/list/send emails. Use when user asks to check email on 163邮箱.
---

# 163邮箱 POP3/SMTP 访问

## 连接参数（已验证）

| 项目 | 值 |
|------|-----|
| 收件(POP3) | `pop.163.com` + PORT 995 (SSL) |
| 发件(SMTP) | `smtp.163.com` + PORT 465 (SSL) |
| 用户名 | `hozen@163.com`（完整邮箱） |
| 密码 | **授权码**（不是登录密码！） |

**⚠️ 关键：163邮箱必须用客户端授权码，不能用登录密码。授权码在网页邮箱 → 设置 → POP3/SMTP/IMAP → 获取。**

## Python连接代码

### 读取邮件（POP3）- 正确方式
```python
import poplib
import email as email_lib
from email.header import decode_header

mail = poplib.POP3_SSL('pop.163.com', 995)  # 必须用SSL
mail.user('hozen@163.com')
mail.pass_(auth_code)

# 获取UIDL映射 {seq_num: uid}
response = mail.uidl()
uidl_map = {}
for line in response[1]:
    parts = line.decode().split()
    if len(parts) >= 2:
        uidl_map[int(parts[0])] = parts[1]

# 读取所有邮件（用retr按顺序号，不能用top按uid）
for seq_num, uid in uidl_map.items():
    lines = mail.retr(seq_num)[1]
    msg = email_lib.message_from_bytes(b'\n'.join(lines))
    
    # 解码主题 (正确方式 - 遍历整个decode_header结果，不是[0])
    subject = ''
    for part, charset in decode_header(msg['Subject'] or ''):
        if isinstance(part, bytes):
            subject += part.decode(charset or 'utf-8', errors='replace')
        elif isinstance(part, str):
            subject += part
    
    print(f"UID: {uid}, Subject: {subject}, From: {msg['From']}")

mail.quit()

# 跟踪已处理邮件：存UID字符串，不是顺序号
processed_uids = set(['xtbCzRKlS2nkt5I7AwAA3h', ...])  # 正确：存UID字符串
```

### 发送邮件（SMTP SSL）
```python
import smtplib
from email.mime.text import MIMEText
from email.header import Header

msg = MIMEText('正文内容', 'plain', 'utf-8')
msg['From'] = 'hozen@163.com'
msg['To'] = 'recipient@example.com'
msg['Subject'] = Header('邮件主题', 'utf-8')

server = smtplib.SMTP_SSL('smtp.163.com', 465)  # 必须用465端口SSL
server.login('hozen@163.com', auth_code)
server.sendmail('hozen@163.com', 'recipient@example.com', msg.as_string())
server.quit()
```

## 踩坑记录

1. **IMAP失败**：163邮箱默认不开启IMAP，且不支持标准IMAP登录（会报`LOGIN Login error`）
2. **必须用POP3**：已知环境只有POP3可用，IMAP不可用
3. **授权码≠密码**：实际密码是授权码（用户单独提供）
4. **Python3直接可用**：内置`poplib`和`email`库，无需安装额外包
5. **必须用POP3_SSL**：非SSL版本`poplib.POP3`会报`-ERR EOF`错误
6. **`top()`对UID无效**：163.com的POP3服务器用`mail.top(uid)`会报`-ERR Unknown message`，必须用`mail.retr(seq_num)`按顺序号获取
7. **UID与顺序号区别**：POP3顺序号(1,2,3...)与UIDL不同，跟踪已处理邮件必须存UIDL字符串而非顺序号。163.com的UIDL格式可能是整数(`"7", "8"`)或Base64-like(`"xtbCzRKlS2nkt5I7AwAA3h"`)，processed列表应原样保存从服务器返回的字符串。

8. **decode_header遍历错误**：常见错误是`for part, charset in decode_header(msg['Subject'])[0]:`，这会尝试遍历第一个tuple的bytes导致"too many values to unpack"。正确方式：`for part, charset in decode_header(msg['Subject'] or ''):`（不加[0]），且part可能是bytes或str需分别处理
9. **获取UID映射**：用`mail.uidl()`得到`{seq_num: uid}`映射，再对每个uid调用`retr(seq_num)`

10. **POP3 API返回值结构（重要！容易导致ValueError: too many values to unpack）**：
    - `mail.list()` 返回 `tuple(3元素)`，实际消息列表在 `[1]`（不是`[0]`和`[1]`）
      ```python
      resp = mail.list()
      msg_list = resp[1]  # 正确的消息列表
      # 错误：_, msg_list = mail.list()  # ValueError!
      ```
    - `mail.uidl(seq_num)` 当传入特定序号时，返回 **bytes**（不是tuple）
      ```python
      uid_resp = mail.uidl(1)
      uid = uid_resp.decode().split()[1]  # 正确：先decode再split
      # 错误：_, uid = mail.uidl(1)  # ValueError!
      ```
    - `mail.retr(seq_num)` 返回 `tuple(3元素)`，实际内容在 `[1]`
      ```python
      lines = mail.retr(seq_num)[1]  # 正确：直接用[1]取lines
      # 错误：_, lines = mail.retr(seq_num)  # ValueError!
      ```
    **调试技巧**：如果遇到 `ValueError: too many values to unpack`，先打印 `type(resp)` 和 `len(resp)` 确认返回结构
11. **已处理文件数据损坏/格式不匹配**：processed_emails.json可能混合了旧整数ID(1,2,3)和新的UID字符串，导致"所有邮件都是新的"假象。修复方法：
    - 加载时过滤：只保留以`xtb`开头的有效UID字符串
    - 与服务器同步：从服务器获取当前所有UID，与processed列表取交集，清理已删除邮件的UID
    - **调试技巧**：在判断新邮件前，先打印几个processed UID和server UID对比，确认格式一致
    - 示例：
      ```python
      # 清理无效UID（只保留服务器上仍存在的）
      server_uids = set(uidl_map.values())
      valid_processed = [uid for uid in processed if isinstance(uid, str) and uid in server_uids]
      
      # 调试：确认格式匹配
      sample_processed = list(processed_uids)[:3]
      sample_server = list(server_uids)[:3]
      print(f"Sample processed UIDs: {sample_processed}")  # 应该是xtb开头
      print(f"Sample server UIDs: {sample_server}")        # 应该是xtb开头
      ```
    - **如果格式不匹配**：所有邮件都会显示为"new"，需要清理processed列表重新开始或迁移

11. **SMTP发送失败"Connection unexpectedly closed"**：服务器出口策略阻断邮件发送，不是端口不通。
    - 诊断：`nc -zv smtp.qq.com 587` 成功但 `smtplib.SMTP().sendmail()` 失败
    - 原因：服务器防火墙允许SMTP端口连接，但阻断实际发送
    - 此时浏览器也无法登录（内嵌iframe无法操作），只能让用户手动发送或换其他方式

12. **processed_uids文件数据损坏导致"全假新邮件"**：当processed_uids文件只有1个UID但服务器有67封邮件时，`server_uids - processed_uids`会返回全部67封，所有邮件都显示为"new"。诊断信号：
    ```python
    # 诊断：检查processed文件数量是否合理
    server_count = len(server_uids)       # e.g. 67
    processed_count = len(processed_uids)  # e.g. 1 (损坏) vs 67 (正常)
    if processed_count < server_count * 0.1:  # 异常：processed远少于server
        print(f"WARNING: processed={processed_count} but server={server_count}, likely corrupted!")
    ```
    **修复方法**：直接用当前服务器UID列表覆盖processed列表（接受"重复处理"比"漏处理"好）：
    ```python
    # 简单粗暴修复：直接同步全量
    with open('/tmp/processed_emails.json', 'w') as f:
        json.dump(list(server_uids), f)  # 全量覆盖
    ```
    **预防**：每次处理完新邮件后立即更新processed_uids，不要跨session丢失状态。

16. **认证码可能已更新**：曾记录 `SRKWTVLJXUHOWQAB`，实际测试返回 `-ERR Unable to log on`。正确授权码是 `QUYwrhcrUN4Bi4ez`（已验证可用）。如果POP3登录失败，先确认为最新授权码。

17. **processed_emails.json缺失时的大规模邮件处理策略**：当文件缺失时所有邮件都会显示为"new"，但实际可用方法：
    - 先获取完整UIDL映射 `mail.uidl()`
    - 用发件人地址过滤目标邮件（如`279235@qq.com`等）
    - 用主题关键字识别spam（如"[review] 乔布斯禅宗文章"重复153封）
    - 只读取实质内容邮件（通常<10封）进行处理
    - 处理完毕后统一将所有278个UID保存为processed

18. **163邮箱退信(hotmail/QQ等)**：163发出的邮件可能被对方邮件系统识别为垃圾邮件并退信。
    - 退信主题通常为"系统退信"或"Undeliverable"
    - 触发原因：邮件内容含外链、附件、或发件人域名被识别为垃圾来源
    - 本环境向hotmail.com发送邮件曾被识别为垃圾邮件退信（550 5.5.0 Requested action not taken）
    - 解决方案：改用其他联系方式，或请收件人将发件人加入白名单

14. **HTML内容嵌在text/plain中**：发件人发送的邮件可能声明为`text/plain`但内容是HTML（如`<html><body><article>...</article></body></html>`）。
    - 判断方法：`msg.is_multipart()`返回`False`，但正文中包含`<html>`标签
    - 提取方式：用正则提取`<article>`标签内容，或用`re.sub(r'<[^>]+>', '', body)`去除HTML标签
    - 示例：
      ```python
      body = payload.decode(charset, errors='replace')
      if '<article>' in body:
          import re
          article_match = re.search(r'<article>(.*?)</article>', body, re.DOTALL)
          if article_match:
              article_text = re.sub(r'<[^>]+>', '', article_match.group(1))
      ```

15. **筛选目标发件人邮件的正确顺序**：
    - 不要用`seq_num=1`假设是第一封新邮件（服务器上最旧的邮件可能仍在seq 1）
    - 正确流程：
      1. 获取完整UIDL映射 `mail.uidl()`
      2. 遍历所有`seq_num, uid`对
      3. 对每个uid调用`mail.retr(seq_num)`获取邮件
      4. 检查`msg['From']`是否包含目标发件人地址
      5. 只处理匹配目标发件人的邮件
    - 示例：
      ```python
      target_senders = ['279235@qq.com', '69870728@qq.com']
      for seq_num, uid in uidl_map.items():
          if uid in processed_uids:
              continue
          lines = mail.retr(seq_num)[1]
          msg = email_lib.message_from_bytes(b'\n'.join(lines))
          from_addr = msg['From'] or ''
          if any(sender in from_addr for sender in target_senders):
              # 处理这封邮件
      ```

## 邮箱配置信息

- 地址：`hozen@163.com`
- **POP3授权码**：`QUYwrhcrUN4Bi4ez`
- **SMTP授权码**：与POP3相同，`QUYwrhcrUN4Bi4ez`（⚠️ 注意：曾误用`HNXHWVJCTJFL`导致SMTP认证失败）

### POP3和SMTP使用相同授权码
- 163邮箱的客户端授权码对POP3和SMTP是**同一个码**
- 如果SMTP认证失败但POP3成功，尝试用POP3的授权码发送SMTP邮件
- 授权码在网页版：设置 → POP3/SMTP/IMAP → 获取/重置

## 环境限制

**核心原则**：
1. **主动发** - 不等对方，先把自己该做的做好
2. **主动跟进** - 发完没回复，主动发邮件询问进度、提醒
3. **主动推进** - 不只配合，要推动事情向前

**工作流**：
1. 检查邮箱发现新邮件
2. 跟进了什么（做了什么动作）
3. 产出了什么（文件/邮件）
4. 正在进行什么
5. 需要什么帮助（如有）

**汇报格式示例**：
```
收到乔布斯邮件，跟进：回复确认框架
产出：jobs-research-framework.md
正在进行：等第一阶段完成
需要帮助：无
```

## 环境限制

- `himalaya` CLI **未安装**，不可用
- 需使用原生 Python `poplib` + `smtplib`
- cron job 环境 home 目录为 `/home/agentuser`，不是 `/root`
