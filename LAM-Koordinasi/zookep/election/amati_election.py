"""
amati_election.py - Pengamat znode pemilihan pemimpin (Aktivitas 4)

Mencetak daftar child di path election (dengan jam) setiap kali berubah,
beserta ephemeralOwner (ID sesi pemilik node).

Cara pakai:
    python amati_election.py                              -> /leader_election_priority (4.1)
    python amati_election.py /leader_election_tolerant    -> (4.2)
Hentikan dengan Ctrl+C.
"""
import sys
import time
from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError

PATH = sys.argv[1] if len(sys.argv) > 1 else "/leader_election_priority"

zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()
print(f"Mengamati {PATH} ... (Ctrl+C untuk berhenti)")

last = None
try:
    while True:
        try:
            children = sorted(zk.get_children(PATH))
        except NoNodeError:
            children = []

        if children != last:
            jam = time.strftime("%H:%M:%S")
            print(f"\n[{jam}] {len(children)} node di {PATH}")
            for child in children:
                try:
                    _, stat = zk.get(f"{PATH}/{child}")
                    owner = hex(stat.ephemeralOwner)
                except NoNodeError:
                    owner = "(node sudah hilang)"
                print(f"  {child}   ephemeralOwner={owner}")
            last = children
        time.sleep(0.3)
except KeyboardInterrupt:
    print("\nPengamatan dihentikan.")
finally:
    zk.stop()
