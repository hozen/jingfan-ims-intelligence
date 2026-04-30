---
name: paho-mqtt-v2-callbacks
description: paho-mqtt 2.1.0 VERSION2 callback signatures and pitfalls
---

# paho-mqtt v2.1.0 VERSION2 回调签名

## 背景
paho-mqtt v2.1.0 的 `CallbackAPIVersion.VERSION2` 回调签名与文档描述有差异，直接用 `int(reasonCode)` 或 `reasonCode == 0` 会抛 `TypeError`。这个问题在调试中花了很长时间才定位。

## 正确的 VERSION2 回调签名

```python
import paho.mqtt.client as mqtt

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311,
)

def on_connect(client, userdata, flags, reasonCode, properties):
    # reasonCode 是 ReasonCode 对象，不能直接 int() 或 == 0
    # 正确取整数值：
    rc = reasonCode.value if hasattr(reasonCode, 'value') else int(reasonCode)
    if rc == 0:
        print("connected")

def on_disconnect(client, userdata, disconnect_flags, reasonCode, properties):
    # 注意：disconnect 的 reasonCode 也是 .value，不是第一个参数
    rc = reasonCode.value if hasattr(reasonCode, 'value') else int(reasonCode)
    print(f"disconnected rc={rc}")

def on_message(client, userdata, msg: mqtt.MQTTMessage):
    # msg.topic  → str
    # msg.payload → bytes
    # msg.mid    → int
    print(f"{msg.topic}: {msg.payload}")
```

## 关键陷阱

| 错误写法 | 正确写法 |
|---------|---------|
| `int(reasonCode)` | `reasonCode.value` |
| `reasonCode == 0` | `reasonCode.value == 0` |
| `reasonCode == ReasonCode(Connack, 'Success')` | `reasonCode.value == 0` |
| `on_disconnect(client, rc, props)` | `on_disconnect(client, userdata, flags, rc, props)` |
| 误以为 reasonCode 是第3个参数 | 第3个是 disconnect_flags，第4个才是 reasonCode |
| 用 VERSION1 签名注册到 VERSION2 客户端 | 用 VERSION2 签名或显式指定 `callback_api_version=mqtt.CallbackAPIVersion.VERSION2` |

## 常见错误

### TypeError: on_connect() missing 2 required positional arguments
- **原因：** 用 VERSION1 回调签名 `on_connect(c, u, f, rc, p, p2)` 注册到了 VERSION2 客户端
- **解决：** 使用正确的 VERSION2 签名或创建 Client 时指定 `callback_api_version=mqtt.CallbackAPIVersion.VERSION1`

### rc=5 Not Authorized（密码正确但仍拒绝）
- **原因：** password file 被破坏（常见于用 `tee`/`echo` 写入），或文件权限不对
- **解决：** `sudo chown mosquitto:mosquitto /etc/mosquitto/passwd`；或用 `mosquitto_passwd -b` 重建用户

## 验证方法

```python
# 快速验证回调签名是否正确
c = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="test", protocol=mqtt.MQTTv311)
c.on_connect = on_connect
c.connect("broker", 1883)
c.loop_start()
import time; time.sleep(1)
c.disconnect()
# 如果没抛 TypeError in callback，说明签名正确
```

## 适用版本
- paho-mqtt 2.1.0（/usr/bin/python3.12）
- 不适用于 v1.x（v1 的 VERSION1 签名完全不同）
- `mqtt.CallbackAPIVersion.VERSION1` 在 v2 里仍然可用但已废弃
