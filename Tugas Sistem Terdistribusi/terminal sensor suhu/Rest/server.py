
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from datetime import datetime
import csv
import os
import time

app = Flask(__name__)

LOG_FILE = os.path.join(os.path.dirname(__file__), "log_rest.csv")

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


@app.route("/temperature", methods=["POST"])
def receive_temperature():
    # Catat waktu penerimaan dan ukuran body HTTP
    t_recv_ms = time.time_ns() // 1_000_000
    raw_body = request.get_data()

    try:
        data = request.get_json()

        node_id = str(data["node_id"])
        t_send_ms = int(data["t_send_ms"])
        suhu = float(data["suhu"])
        sequence_no = int(data["sequence_no"])

        log_data = {
            "timestamp_iso": datetime.now().astimezone().isoformat(),
            "node_id": node_id,
            "protocol": "rest",
            "t_send_ms": t_send_ms,
            "t_recv_ms": t_recv_ms,
            "payload_bytes": len(raw_body),
            "suhu": suhu,
            "sequence_no": sequence_no,
        }

        write_log(log_data)

        print(
            f"REST menerima suhu={suhu} C, "
            f"node={node_id}, sequence={sequence_no}"
        )

        return jsonify({
            "status": "ok",
            "sequence_no": sequence_no
        }), 200

    except (TypeError, ValueError, KeyError):
        return jsonify({"error": "Payload tidak valid"}), 400


if __name__ == "__main__":
    # 0.0.0.0 memungkinkan server diakses melalui jaringan lokal
    app.run(host="0.0.0.0", port=5151, debug=False)
