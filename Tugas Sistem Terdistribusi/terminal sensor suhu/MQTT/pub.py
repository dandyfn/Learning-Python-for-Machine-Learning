
import json
import time
import paho.mqtt.client as mqtt

# Konfigurasi broker MQTT lokal
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883
TOPIC = "sister/temp"

NODE_ID = "node-1"
SUHU = 28.0
INTERVAL_SECONDS = 1

connected = False


def on_connect(client, userdata, flags, reason_code, properties):
    global connected

    if reason_code == 0:
        connected = True
        print("Publisher terhubung ke Mosquitto lokal.")
    else:
        print(f"Koneksi gagal: {reason_code}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

print("Menghubungkan publisher ke Mosquitto lokal...")

try:
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    # Tunggu hingga koneksi berhasil
    timeout = 10
    start_time = time.time()

    while not connected and time.time() - start_time < timeout:
        time.sleep(0.1)

    if not connected:
        raise RuntimeError("Publisher gagal terhubung ke broker.")

    sequence_no = 0

    print("Publisher berjalan. Tekan Ctrl+C untuk berhenti.")

    while True:
        sequence_no += 1

        payload = {
            "node_id": NODE_ID,
            "t_send_ms": time.time_ns() // 1_000_000,
            "suhu": SUHU,
            "sequence_no": sequence_no,
        }

        result = client.publish(
            TOPIC,
            json.dumps(payload),
            qos=0,
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(
                f"Mengirim suhu={SUHU} C, "
                f"sequence={sequence_no}"
            )
        else:
            print(f"Gagal mengirim sequence={sequence_no}")

        time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("\nPublisher dihentikan.")

except (OSError, RuntimeError) as error:
    print(f"Kesalahan: {error}")

finally:
    client.disconnect()
    client.loop_stop()
