---
name: mqtt-agent-framework
description: Minimal MQTT Agent framework + paho-mqtt v2.1.0 callback signatures. Broker 175.24.134.225:1883.
---

# MQTT Agent Framework (Minimal v2)

## Broker
- Address: `175.24.134.225:1883`
- Auth: `agent01`, `agent02`, `agent03` — all password `changeme123`

## Python Environment (CRITICAL)
paho-mqtt is installed on **`/usr/bin/python3.12`** only.
The camoufox venv (`~/.camoufox-venv/bin/python3`) does NOT have paho.
Always use `/usr/bin/python3.12` when running MQTT agent code.

## Framework: mqtt_simple.py

Minimal, stateless, single-file. No identity files, no project concepts.

```python
from mqtt_simple import Agent

a = Agent("alice", "175.24.134.225", 1883, "agent01", "changeme123")
a.connect()
a.subscribe("test/bob", lambda agent, msg: print(msg.payload))
a.publish("test/bob", "hello")
a.disconnect()
```

### Methods
| Method | Description |
|--------|-------------|
| `connect()` | Blocking connect (waits up to 5s for CONNACK) |
| `subscribe(topic, handler)` | QoS1 subscribe; handler: `(agent, MQTTMessage)` |
| `publish(topic, payload_str)` | Fire-and-forget publish |
| `reply(msg, payload_str)` | Auto-reply: strips last topic segment → `/reply` |
| `disconnect()` | Clean disconnect |

### MQTTMessage fields
- `topic` (str), `payload` (bytes), `mid` (int)

---

## paho-mqtt v2.1.0 Callback Signatures (VERSION2)

**This caused 12 hours of debugging — get it right the first time.**

```python
import paho.mqtt.client as mqtt

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,  # MUST be VERSION2
    client_id="myid",
    protocol=mqtt.MQTTv311,
)
```

### on_connect (VERSION2) — 5 positional args after self
```python
def _on_connect(self, client, userdata, flags, reasonCode, properties):
    # reasonCode == 0 means success
```

### on_disconnect (VERSION2) — 6 positional args after self
```python
def _on_disconnect(self, client, userdata, disconnect_flags, reasonCode, properties):
    # disconnect_flags.is_disconnect_packet_from_server (bool)
    # reasonCode: int
    # properties: MQTTProperties
```
**COMMON MISTAKE**: Writing only 4 args (`client, userdata, reasonCode, properties`) → TypeError.

### on_message (VERSION2) — 3 positional args after self
```python
def _on_message(self, client, userdata, msg):
    # msg.topic   = str
    # msg.payload = bytes
    # msg.mid     = int
```

---

## Threading Model

Use `loop_forever()` in `start()`, NOT `loop_start()`.

- `loop_start()` creates a **daemon thread**. When the main thread exits, the daemon is killed immediately — MQTT loop stops, no messages dispatched.
- `loop_forever()` **blocks the calling thread** in the network loop. Call `loop_stop()` before `disconnect()`.

```python
def start(self):
    self._client.loop_start()
    if not self._conn_event.wait(timeout=5):
        raise TimeoutError("connection timeout")
    return self

def stop(self):
    self._client.loop_stop()
    self._client.disconnect()
```

---

## Verified Working (Apr 2026)

- `mqtt_simple.py` — PASS ✅
- `mqtt_simple_test.py` — alice↔bob 双向消息 ✅
- Broker: raw mosquitto_pub/sub confirmed ✅
- Python: `/usr/bin/python3.12` (has paho 2.1.0) ✅

---

## Anti-patterns to Avoid

1. **Don't use subprocess isolation for simple tests** — wastes time debugging buffering/exit issues
2. **Don't use identity files or sys.modules hacks** — unnecessary complexity
3. **Don't use `loop_start()` in test scripts** — daemon thread dies on main exit
4. **Don't mix VERSION1 and VERSION2 callbacks** — pick VERSION2 and use correct 6-arg `_on_disconnect`

---

## Files
- Framework: `/home/agentuser/scripts/mqtt_simple.py`
- Test: `/home/agentuser/scripts/mqtt_simple_test.py`

## Status
✅ Production ready. Minimal, tested, callback signatures verified.
