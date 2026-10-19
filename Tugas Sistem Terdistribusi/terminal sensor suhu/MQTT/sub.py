
import os
import json
import csv
import time
from datetime import datetime

import paho.mqtt.client as mqtt

# Konfigurasi broker MQTT lokal
BROKER_HOST = "172.19.246.136"
BROKER_PORT = 1883
TOPIC = "sister/temp"

# File log disimpan di folder MQTT
LOG_FILE = os.path.join(os.path.dirname(__file__), "log_mqtt.csv")

COLUMNS = [
    "timestamp_iso",
    "node_id",
    "protocol",
    "t_send_ms",
    "t_recv_ms",
    "payload_bytes",
    "suhu",
    "sequence_no",
]


def write_log(data):
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)

        if not file_exists or os.path.getsize(LOG_FILE) == 0:
            writer.writeheader()

        writer.writerow(data)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Subscriber terhubung ke Mosquitto lokal.")
        client.subscribe(TOPIC, qos=0)
        print(f"Mendengarkan topic: {TOPIC}")
    else:
        print(f"Koneksi gagal: {reason_code}")


def on_message(client, userdata, msg):
    t_recv_ms = time.time_ns() // 1_000_000
    raw_payload = msg.payload

    try:
        data = json.loads(raw_payload.decode("utf-8"))

        node_id = str(data["node_id"])
        t_send_ms = int(data["t_send_ms"])
        suhu = float(data["suhu"])
        sequence_no = int(data["sequence_no"])

        log_data = {
            "timestamp_iso": datetime.now().astimezone().isoformat(),
            "node_id": node_id,
            "protocol": "mqtt",
            "t_send_ms": t_send_ms,
            "t_recv_ms": t_recv_ms,
            "payload_bytes": len(raw_payload),
            "suhu": suhu,
            "sequence_no": sequence_no,
        }

        write_log(log_data)

        print(
            f"MQTT menerima suhu={suhu} C, "
            f"node={node_id}, sequence={sequence_no}"
        )

    except (ValueError, TypeError, KeyError, UnicodeDecodeError) as error:
        print(f"Pesan tidak valid, tidak dicatat ke CSV: {error}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("Menghubungkan subscriber ke Mosquitto lokal...")

try:
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nSubscriber dihentikan.")
finally:
    client.disconnect()
