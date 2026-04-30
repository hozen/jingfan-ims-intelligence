---
name: mosquitto-inmemory-setup
description: Install and configure Mosquitto MQTT broker for memory-only (no disk) operation with password auth on Ubuntu 24.04
triggers:
  - "setup mqtt broker"
  - "mosquitto install"
  - "mqtt lightweight no persistence"
  - "mqtt broker memory only"
---

# Mosquitto In-Memory MQTT Broker Setup (Ubuntu 24.04)

## Goal
Lightweight MQTT broker with: no disk I/O, password authentication, accessible on all interfaces.

## Steps

### 1. Install
```bash
sudo apt install -y mosquitto mosquitto-clients
```

### 2. Config file — /etc/mosquitto/conf.d/zz-inmemory.conf
```properties
listener 1883 0.0.0.0
allow_anonymous false
password_file /etc/mosquitto/passwd
persistence false
log_dest stdout
log_type error
log_type warning
max_queued_messages 0
max_keepalive 65535
```
> ⚠️ Do NOT set `persistence_location` here — the main config at `/etc/mosquitto/mosquitto.conf` already defines it, and duplicates cause startup failure with "Error: Duplicate persistence_location value".

### 3. Create password file
```bash
# Interactive creation
sudo mosquitto_passwd -c /etc/mosquitto/passwd <username>
# Then enter password twice when prompted

# Batch mode (no interactive prompt) — preferred for scripting
sudo mosquitto_passwd -b /etc/mosquitto/passwd <username> <password>

# Add multiple users at once
sudo bash -c '
  mosquitto_passwd -b /etc/mosquitto/passwd agent01 changeme123
  mosquitto_passwd -b /etc/mosquitto/passwd agent02 changeme456
  mosquitto_passwd -b /etc/mosquitto/passwd agent03 agent3pass999
  chown mosquitto:mosquitto /etc/mosquitto/passwd
  chmod 600 /etc/mosquitto/passwd
'
```
> ⚠️ Password file must be owned by the mosquitto user, otherwise broker fails to start with "Error opening password file".

### 4. Fix ownership
```bash
sudo chown mosquitto:mosquitto /etc/mosquitto/passwd
sudo systemctl restart mosquitto
```

### 5. Verify
```bash
ss -tlnp | grep 1883
# Should show: LISTEN 0.0.0.0:1883
```

### 6. Test pub/sub (from another terminal)
```bash
# Terminal 1: subscribe
mosquitto_sub -h localhost -p 1883 -u agent01 -P changeme123 -t test -C 1 -W 5

# Terminal 2: publish
mosquitto_pub -h localhost -p 1883 -u agent01 -P changeme123 -t test -m "hello"
```

## Pitfalls

### Password file permission error
- **Symptom:** `Error opening password file "/etc/mosquitto/passwd"` in journalctl
- **Cause:** File owned by root, mosquitto user (uid 111) cannot read it
- **Fix:** `sudo chown mosquitto:mosquitto /etc/mosquitto/passwd`

### rc=5 Not Authorized (even with correct password)
- **Symptom:** Client connect fails with `rc=5` despite correct username/password
- **Cause:** Password file is corrupted or truncated. Often happens when using `tee` or `echo | passwd` to write the file — these tools can corrupt the hash format
- **Fix:** Always use `mosquitto_passwd` exclusively. To reset:
  ```bash
  sudo bash -c '
    mosquitto_passwd -b /etc/mosquitto/passwd agent01 changeme123
    mosquitto_passwd -b /etc/mosquitto/passwd agent02 changeme456
    mosquitto_passwd -b /etc/mosquitto/passwd agent03 changeme789
    chown mosquitto:mosquitto /etc/mosquitto/passwd
    chmod 600 /etc/mosquitto/passwd
  '
  ```

### Duplicate persistence_location
- **Symptom:** `Error: Duplicate persistence_location value in configuration`
- **Cause:** Main `/etc/mosquitto/mosquitto.conf` sets `persistence_location /var/lib/mosquitto/`; conf.d file also sets it
- **Fix:** Remove `persistence_location` from conf.d override — `persistence false` is sufficient

### Client ID conflict (rc=5 on reconnect)
- **Symptom:** First connect succeeds, subsequent runs fail with `rc=5`
- **Cause:** Mosquitto 2.x rejects reconnecting clients with the same client ID within a short window (max_inflight_size/persistent_client_expiration window)
- **Fix:** Use empty client ID (`client_id=""`) so paho-mqtt generates a random one each run

### Messages not received
- **Symptom:** Publisher succeeds but subscriber never receives
- **Cause:** `max_queued_messages 0` = pure relay mode. If no active subscriber when message is sent, it is discarded
- **Fix:** This is expected behavior for cache-less relay. Ensure subscriber is connected before publishing

### Binds to 127.0.0.1 only
- **Symptom:** External hosts cannot connect
- **Cause:** Default mosquitto.conf does not specify listener interface
- **Fix:** Use `listener 1883 0.0.0.0` instead of just `listener 1883`

### systemd restart fails repeatedly ("Start request repeated too quickly")
- **Symptom:** After a config error, systemd backs off and refuses to restart
- **Cause:** mosquitto crashed on bad config and systemd enters a back-off loop
- **Fix:** Run `sudo mosquitto -c /etc/mosquitto/conf.d/zz-inmemory.conf` manually to see the actual error, fix it, then `sudo systemctl restart mosquitto`

## Multi-Agent Client IDs (paho-mqtt)
When simulating or running multiple clients from one process, always use `client_id=""` (auto-generated):
```python
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="")  # empty = random
```
Do NOT reuse fixed client IDs like `"agent01"` across multiple threads/processes — Mosquitto 2.x treats duplicate IDs within the same session as a conflict and rejects the newcomer.

## Firewall (if needed)
```bash
sudo ufw allow 1883/tcp
```

## Credentials Format (for client libs like paho-mqtt)
```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.username_pw_set("agent01", "changeme123")
client.connect("<broker-ip>", 1883)
client.subscribe("topic/name")
client.publish("topic/name", "message")
```
