"""
amati_lock.py - Pengamat antrean lock /balance_lock (Aktivitas 3, Skenario 3B)

Mencetak daftar child ephemeral-sequential di /balance_lock setiap kali berubah,
beserta ephemeralOwner (ID sesi) dan identitas klien (data node).
Child dengan nomor urut terkecil = pemegang lock, sisanya mengantre.

Jalankan SEBELUM klien1.py dan klien2.py. Hentikan dengan Ctrl+C.
"""
import time
from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError

LOCK_PATH = "/balance_lock"

zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()
print(f"Mengamati {LOCK_PATH} ... (Ctrl+C untuk berhenti)")

last = None
try:
    while True:
        try:
            children = zk.get_children(LOCK_PATH)
        except NoNodeError:
            children = []
        # urutkan berdasarkan 10 digit nomor urut di akhir nama node
        children = sorted(children, key=lambda c: c[-10:])

        if children != last:
            jam = time.strftime("%H:%M:%S")
            print(f"\n[{jam}] {len(children)} child di {LOCK_PATH}")
            for i, child in enumerate(children):
                try:
                    data, stat = zk.get(f"{LOCK_PATH}/{child}")
                    klien = data.decode("utf-8") or "-"
                    owner = hex(stat.ephemeralOwner)
                except NoNodeError:
                    klien, owner = "-", "(node sudah hilang)"
                peran = "PEMEGANG LOCK" if i == 0 else "menunggu"
                print(f"  {child}")
                print(f"     klien={klien} | ephemeralOwner={owner} | {peran}")
            last = children
        time.sleep(0.3)
except KeyboardInterrupt:
    print("\nPengamatan dihentikan.")
finally:
    zk.stop()