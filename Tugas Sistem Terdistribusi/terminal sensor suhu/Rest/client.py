
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

# Untuk pengujian awal pada satu laptop.
# Nanti ganti 127.0.0.1 dengan IP Laptop 2.
SERVER_URL = "http://127.0.0.1:5151/temperature"

NODE_ID = "node-1"
INTERVAL_SECONDS = 1
SUHU = 28.0

sequence_no = 0

print("REST client berjalan. Tekan Ctrl+C untuk berhenti.")

try:
    while True:
        sequence_no += 1

        # Waktu pengiriman dalam milidetik sejak epoch Unix
        t_send_ms = time.time_ns() // 1_000_000

        payload = {
            "node_id": NODE_ID,
            "t_send_ms": t_send_ms,
            "suhu": SUHU,
            "sequence_no": sequence_no,
        }

        try:
            response = requests.post(
                SERVER_URL,
                json=payload,
                timeout=5
            )

            if response.status_code == 200:
                print(f"REST terkirim: sequence={sequence_no}")
            else:
                print(
                    f"REST gagal: sequence={sequence_no}, "
                    f"status={response.status_code}"
                )

        except requests.RequestException as error:
            print(f"Kesalahan koneksi: {error}")

        time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("\nREST client dihentikan.")
