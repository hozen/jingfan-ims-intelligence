---
name: mqtt-agent-communication
description: 3-peer MQTT agent communication framework with Mosquitto on Ubuntu 24.04 — covers broker setup, in-memory config, password auth, and Python client with ACK+retry pattern
tags: [mqtt, mosquitto, agent, inter-process-communication]
---

# MQTT Agent Communication Framework

## Context
3 peer-to-peer agents communicating via a shared Mosquitto MQTT broker over localhost:1883. Each agent is identified by its own credentials.

## Topic Structure
```
agents/online              # broadcast: announces agent is online
agents/<id>/inbox         # directed inbox for each agent
agents/<id>/ack           # acks directed back to sender
agents/broadcast          # public broadcast (no ACK expected)
```

## Message Format (JSON)
```json
{
  "msg_id": "uuid-v4",
  "from": "agent01",
  "to": "agent02",              // null = broadcast
  "type": "task",                // task | result | ack | ready | ping
  "reply_to": "agents/agent01/ack",
  "payload": { ... },
  "retry_count": 0,
  "timestamp": 1745689200
}
```

## Reliable Send (ACK + Retry)
- Wait **5 seconds** for ACK after publish
- If timeout → retry **once** (only if `retry_count == 0`)
- If still no ACK → log `UNACKNOWLEDGED msg_id=xxx` and drop
- Broadcasts do NOT wait for ACK (pure relay, no subscriber = drop is normal)

## Mosquitto Broker Setup (Ubuntu 24.04)

### Config: /etc/mosquitto/conf.d/zz-inmemory.conf
```
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
Note: Do NOT set `persistence_location` here — it is already set in main /etc/mosquitto/mosquitto.conf and will cause "Duplicate persistence_location" error.

### Password File — ALWAYS use mosquitto_passwd (never tee/echo)
```bash
# Reset entire file (all 3 agents)
sudo bash -c '
    mosquitto_passwd -b /etc/mosquitto/passwd agent01 changeme123
    mosquitto_passwd -b /etc/mosquitto/passwd agent02 changeme456
    mosquitto_passwd -b /etc/mosquitto/passwd agent03 agent3pass999
    chown mosquitto:mosquitto /etc/mosquitto/passwd
    chmod 600 /etc/mosquitto/passwd
'

# Restart after any change
sudo systemctl restart mosquitto
```

**rc=5 Not Authorized even with correct password?** The file is corrupted — likely from `tee` or `echo | passwd`. Use ONLY `mosquitto_passwd -b`. Then verify:
```bash
cat /etc/mosquitto/passwd   # should show agent01:$7$101$...
```

### Restart after config change
```bash
sudo systemctl restart mosquitto
```

### Verify
```bash
ss -tlnp | grep 1883
# Should show: 0.0.0.0:1883
```

## Python Client

### Important: Use python3.12 (system) not python3 (hermes venv)
The Hermes venv python3 has no paho-mqtt. System python3.12 has it.
```bash
python3.12 /path/to/script.py
```

### Install paho-mqtt for custom target
```bash
pip install --target=/home/agentuser/.local/pylib paho-mqtt
PYTHONPATH=/home/agentuser/.local/pylib python3.12 script.py
```

### Client Skeleton
```python
import paho.mqtt.client as mqtt
import json, uuid, threading, time

BROKER = "localhost"
PORT = 1883
MY_ID = "agent01"
CREDS = {"agent01": "pw1", "agent02": "pw2", "agent03": "pw3"}
ACK_TIMEOUT = 5.0
MAX_RETRIES = 1

pending = {}   # msg_id → timer thread
ack_results = {}
lock = threading.Lock()

def on_connect(client, userdata, flags, rc, props=None):
    if rc != 0:
        print(f"[{MY_ID}] Connect failed rc={rc}")
        return
    print(f"[{MY_ID}] Connected")
    client.subscribe(f"agents/{MY_ID}/inbox")
    client.subscribe(f"agents/{MY_ID}/ack")
    client.subscribe("agents/online")
    client.subscribe("agents/broadcast")
    client.publish("agents/online", json.dumps({"from": MY_ID, "type": "ready"}))

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    who = payload.get("from_") or payload.get("from")
    if who == MY_ID:
        return  # skip own messages

    # Handle ACK
    if payload.get("type") == "ack":
        msg_id = payload.get("msg_id")
        with lock:
            ack_results[msg_id] = True
        with lock:
            if msg_id in pending:
                pending[msg_id].cancel()
                del pending[msg_id]
        return

    # Handle message types here:
    #   topic, statement, proposal, vote, decision, etc.
    handle_message(MY_ID, payload)

    # Always ACK directed inbox messages
    if f"agents/{MY_ID}/inbox" in msg.topic and payload.get("reply_to"):
        ack = json.dumps({"msg_id": payload["msg_id"], "from_": MY_ID, "type": "ack"})
        threading.Thread(
            target=lambda t=payload["reply_to"]: client.publish(t, ack)
        ).start()

def send_reliable(client, to, payload, retry=MAX_RETRIES):
    """Directed msg (to!=None): ACK + retry. Broadcast (to=None): fire-and-forget."""
    msg_id = str(uuid.uuid4())
    payload = dict(payload)
    payload.update(msg_id=msg_id, from_=MY_ID, retry_count=0)

    topic = f"agents/{to}/inbox" if to else "agents/broadcast"

    # Broadcast: fire and forget, no ACK
    if to is None:
        client.publish(topic, json.dumps(payload))
        print(f"[{MY_ID}] → [{topic}] broadcast {msg_id[:8]} (no ACK)")
        return True

    # Directed: wait for ACK, retry once on timeout
    payload["reply_to"] = f"agents/{MY_ID}/ack"

    for attempt in range(retry + 1):
        client.publish(topic, json.dumps(payload))
        print(f"[{MY_ID}] → [{topic}] attempt {attempt+1} {msg_id[:8]}")

        start = time.time()
        while time.time() - start < ACK_TIMEOUT:
            with lock:
                if msg_id in ack_results:
                    del ack_results[msg_id]
                    return True
            time.sleep(0.1)

        if attempt < retry:
            payload["retry_count"] = attempt + 1
            print(f"[{MY_ID}] ⏳ No ACK, retrying...")

    print(f"[{MY_ID}] ❌ UNACKNOWLEDGED {msg_id[:8]}")
    return False

# Usage — ALWAYS use empty client_id for Mosquitto 2.x compatibility
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="")
client.username_pw_set(MY_ID, CREDS[MY_ID])
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=30)
client.loop_start()
```

## Pitfalls
- **`client_id=""` required** — Mosquitto 2.x rejects duplicate client IDs. Using `client_id="agent01"` causes `rc=5` on reconnect or when running multiple instances. Always use empty string for auto-generated ID.
- **`max_queued_messages 0` = pure relay** — messages to inactive agent = dropped (normal, not a bug)
- **Broadcast retry** — handle broadcasts as special case with no ACK wait; otherwise `send_reliable` will timeout and retry on an empty topic (expected but noisy)
- **Password file corruption** — `tee`/`echo | mosquitto_passwd` corrupts the hash format → `rc=5`. Use ONLY `mosquitto_passwd -b` exclusively
- **Password file ownership** — mosquitto daemon runs as `mosquitto:mosquitto`; file must be owned by that user
- **Do NOT set `persistence_location`** in custom config (duplicate from main.conf → startup failure)
- **python3 (hermes venv) has no paho-mqtt** — use `python3.12` (system) or `pip install --target=...`
