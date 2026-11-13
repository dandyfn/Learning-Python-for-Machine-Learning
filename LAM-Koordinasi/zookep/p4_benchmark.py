#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p4_benchmark.py - Proyek Mini P4: Lock pesimistik vs Lock optimistik (compare-and-set)

N klien (masing-masing punya sesi ZooKeeper sendiri) berjalan BERSAMAAN dan
masing-masing menambah /p4_counter sebanyak K kali (+1 per operasi).
Nilai akhir yang benar = N x K.

Mode yang diuji:
  nolock     : baca -> tulis tanpa pengaman          (pembanding, rawan lost update)
  lock       : kazoo Lock (pesimistik, antre)          seperti klien1/klien2.py
  optimistic : zk.set(..., version=stat.version) + retry jika BadVersionError

Metrik yang dicatat:
  waktu total, throughput (operasi sukses/detik), nilai akhir & selisihnya,
  jumlah konflik (retry) dan tingkat konflik untuk mode optimistik.

Contoh:
  python p4_benchmark.py                       # N = 3, 5, 10 ; K = 20 ; kerja 5 ms
  python p4_benchmark.py --clients 2 5 --ops 30 --work-ms 10
Hasil juga disimpan ke p4_hasil.csv (untuk tabel/grafik laporan).
"""
import argparse
import csv
import threading
import time

from kazoo.client import KazooClient
from kazoo.exceptions import BadVersionError

HOSTS = "127.0.0.1:2181"
COUNTER = "/p4_counter"
LOCK_PATH = "/p4_lock"


def reset_counter():
    zk = KazooClient(hosts=HOSTS)
    zk.start()
    zk.ensure_path(COUNTER)
    zk.set(COUNTER, b"0")
    zk.stop()
    zk.close()


def read_counter():
    zk = KazooClient(hosts=HOSTS)
    zk.start()
    data, _ = zk.get(COUNTER)
    zk.stop()
    zk.close()
    return int(data.decode())


def worker(mode, client_id, ops, work_s, barrier, stats, idx):
    zk = KazooClient(hosts=HOSTS)
    zk.start()
    lock = zk.Lock(LOCK_PATH, f"klien-{client_id}")
    konflik = 0
    barrier.wait()  # semua klien mulai bersamaan

    for _ in range(ops):
        if mode == "nolock":
            data, _ = zk.get(COUNTER)
            time.sleep(work_s)  # simulasi pekerjaan
            zk.set(COUNTER, str(int(data) + 1).encode())

        elif mode == "lock":
            with lock:
                data, _ = zk.get(COUNTER)
                time.sleep(work_s)
                zk.set(COUNTER, str(int(data) + 1).encode())

        elif mode == "optimistic":
            while True:
                data, stat = zk.get(COUNTER)
                time.sleep(work_s)
                try:
                    zk.set(COUNTER, str(int(data) + 1).encode(), version=stat.version)
                    break
                except BadVersionError:
                    konflik += 1  # versi berubah -> baca ulang & coba lagi

    stats[idx] = konflik
    zk.stop()
    zk.close()


def run(mode, n, ops, work_ms):
    reset_counter()
    barrier = threading.Barrier(n + 1)
    stats = [0] * n
    threads = [
        threading.Thread(target=worker, args=(mode, i + 1, ops, work_ms / 1000, barrier, stats, i))
        for i in range(n)
    ]
    for t in threads:
        t.start()
    barrier.wait()            # lepas semua klien
    t0 = time.perf_counter()
    for t in threads:
        t.join()
    durasi = time.perf_counter() - t0

    akhir = read_counter()
    harapan = n * ops
    konflik = sum(stats)
    return {
        "mode": mode,
        "N": n,
        "K": ops,
        "kerja_ms": work_ms,
        "durasi_s": round(durasi, 3),
        "throughput_ops_s": round(harapan / durasi, 2),
        "nilai_akhir": akhir,
        "harapan": harapan,
        "hilang": harapan - akhir,
        "konflik": konflik,
        "tingkat_konflik": round(konflik / (harapan + konflik), 3) if mode == "optimistic" else "",
    }


def main():
    p = argparse.ArgumentParser(description="Benchmark lock pesimistik vs optimistik (P4)")
    p.add_argument("--clients", type=int, nargs="+", default=[3, 5, 10], help="daftar jumlah klien N")
    p.add_argument("--ops", type=int, default=20, help="operasi per klien (K)")
    p.add_argument("--work-ms", type=float, default=5, help="simulasi kerja di bagian kritis (ms)")
    p.add_argument("--modes", nargs="+", default=["nolock", "lock", "optimistic"])
    p.add_argument("--csv", default="p4_hasil.csv")
    a = p.parse_args()

    hasil = []
    for n in a.clients:
        for mode in a.modes:
            print(f"Menjalankan mode={mode:<10} N={n:<3} K={a.ops} ...", flush=True)
            r = run(mode, n, a.ops, a.work_ms)
            hasil.append(r)
            print(f"  durasi={r['durasi_s']} s | throughput={r['throughput_ops_s']} op/s | "
                  f"akhir={r['nilai_akhir']}/{r['harapan']} (hilang {r['hilang']}) | konflik={r['konflik']}",
                  flush=True)

    print("\n=== RINGKASAN ===")
    print(f"{'mode':<11}{'N':>4}{'durasi(s)':>11}{'op/s':>9}{'akhir':>8}{'hilang':>8}{'konflik':>9}{'tk.konflik':>12}")
    for r in hasil:
        print(f"{r['mode']:<11}{r['N']:>4}{r['durasi_s']:>11}{r['throughput_ops_s']:>9}"
              f"{r['nilai_akhir']:>8}{r['hilang']:>8}{r['konflik']:>9}{str(r['tingkat_konflik']):>12}")

    with open(a.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(hasil[0].keys()))
        w.writeheader()
        w.writerows(hasil)
    print(f"\nHasil disimpan ke {a.csv}")


if __name__ == "__main__":
    main()
