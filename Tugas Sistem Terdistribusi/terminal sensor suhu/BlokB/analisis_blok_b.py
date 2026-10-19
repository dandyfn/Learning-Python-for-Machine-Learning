
from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / "hasil_eksperimen"
OUT = BASE / "hasil_analisis"

NEEDED = {
    "timestamp_iso", "node_id", "protocol", "t_send_ms",
    "t_recv_ms", "payload_bytes", "suhu", "sequence_no"
}


def info(path):
    # Mendukung nama: REST_N2_run01.csv, MQTT_N3_run12.csv, dan seterusnya
    m = re.search(r"(REST|MQTT)_N([234])_RUN(\d+)", path.stem.upper())
    return (
        m.group(1),
        int(m.group(2)),
        int(m.group(3))
    ) if m else None


def main():
    if not DATA.exists():
        raise SystemExit(f"Buat folder terlebih dahulu: {DATA}")

    rows = []

    for f in sorted(DATA.glob("*.csv")):
        meta = info(f)

        if not meta:
            continue

        protocol, n, run = meta

        try:
            d = pd.read_csv(f)
        except Exception as e:
            print(f"Dilewati, CSV gagal dibaca: {f.name} ({e})")
            continue

        if not NEEDED.issubset(d.columns):
            print("Dilewati, kolom tidak cocok:", f.name)
            continue

        for c in [
            "t_send_ms", "t_recv_ms",
            "payload_bytes", "sequence_no"
        ]:
            d[c] = pd.to_numeric(d[c], errors="coerce")

        d = d.dropna(subset=["t_send_ms", "t_recv_ms"])

        if d.empty:
            print("Dilewati, tidak ada data valid:", f.name)
            continue

        latency = d["t_recv_ms"] - d["t_send_ms"]
        valid = latency[latency >= 0]

        duration = (
            d["t_recv_ms"].max() - d["t_recv_ms"].min()
        ) / 1000

        rows.append({
            "file": f.name,
            "protokol": protocol,
            "N": n,
            "run": run,
            "pesan_diterima": len(d),
            "latensi_p50_ms": (
                valid.quantile(0.50) if len(valid) else float("nan")
            ),
            "latensi_p95_ms": (
                valid.quantile(0.95) if len(valid) else float("nan")
            ),
            "latensi_p99_ms": (
                valid.quantile(0.99) if len(valid) else float("nan")
            ),
            "throughput_pesan_detik": (
                len(d) / duration if duration > 0 else float("nan")
            ),
            "latensi_negatif": int((latency < 0).sum())
        })

    if not rows:
        raise SystemExit(
            "Tidak ada CSV yang cocok. Pastikan nama file seperti "
            "REST_N2_run01.csv atau MQTT_N3_run12.csv dan "
            "kolom CSV sesuai."
        )

    OUT.mkdir(parents=True, exist_ok=True)

    runs = pd.DataFrame(rows).sort_values(
        ["protokol", "N", "run"]
    )

    # Jika ada file duplikat untuk protokol, N, dan run yang sama,
    # gunakan satu file saja dan tampilkan peringatannya.
    duplicates = runs.duplicated(
        subset=["protokol", "N", "run"], keep=False
    )

    if duplicates.any():
        print("PERINGATAN: Ada file untuk run yang sama:")
        print(runs.loc[
            duplicates, ["file", "protokol", "N", "run"]
        ].to_string(index=False))

        runs = runs.drop_duplicates(
            subset=["protokol", "N", "run"], keep="first"
        )

    runs.to_csv(OUT / "metrik_per_run.csv", index=False)

    # Run 1 dan 2 adalah warm-up, sehingga tidak masuk ringkasan.
    runs["status"] = runs["run"].apply(
        lambda x: "WARM-UP" if x <= 2 else "DIANALISIS"
    )

    runs[[
        "file", "protokol", "N", "run", "status",
        "pesan_diterima", "latensi_negatif"
    ]].to_csv(OUT / "status_run.csv", index=False)

    metrics = [
        ("latensi_p50_ms", "Latensi p50 (ms)"),
        ("latensi_p95_ms", "Latensi p95 (ms)"),
        ("latensi_p99_ms", "Latensi p99 (ms)"),
        ("throughput_pesan_detik", "Throughput (pesan/detik)")
    ]

    summaries = []

    for (protocol, n), g in runs[
        runs["run"] > 2
    ].groupby(["protokol", "N"]):

        r = {
            "protokol": protocol,
            "N": n,
            "jumlah_run_dianalisis": g["run"].nunique()
        }

        for col, _ in metrics:
            s = pd.to_numeric(
                g[col], errors="coerce"
            ).dropna()

            r[col + "_median"] = (
                s.median() if len(s) else float("nan")
            )

            r[col + "_IQR"] = (
                s.quantile(0.75) - s.quantile(0.25)
                if len(s) else float("nan")
            )

        summaries.append(r)

    summary = pd.DataFrame(summaries)

    summary.to_csv(
        OUT / "ringkasan_median_IQR.csv", index=False
    )

    # Buat grafik per metrik untuk membandingkan REST dan MQTT.
    for col, label in metrics:
        fig, ax = plt.subplots(figsize=(8, 5))

        for protocol in ("REST", "MQTT"):
            g = summary[
                summary["protokol"] == protocol
            ] if not summary.empty else pd.DataFrame()

            if not g.empty:
                g = g.sort_values("N")
                ax.plot(
                    g["N"],
                    g[col + "_median"],
                    marker="o",
                    label=protocol
                )

        ax.set_xticks([2, 3, 4])
        ax.set_xlabel("Jumlah logical sender (N)")
        ax.set_ylabel(label)
        ax.set_title(
            label + " — median run setelah warm-up"
        )
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()

        fig.savefig(
            OUT / ("grafik_" + col + ".png"),
            dpi=160
        )
        plt.close(fig)

    print("\nAnalisis selesai.")
    print("Lokasi hasil:", OUT)
    print("\nRingkasan median dan IQR:")
    print(summary.to_string(index=False))
    print("\nPeriksa jumlah run, latensi negatif, dan kelengkapan data.")


if __name__ == "__main__":
    main()
