#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
klien2_optimistic.py - Proyek Mini P4 (Lock optimistik), Client B

Sama seperti klien2.py (kurangi 300, tanpa jeda panjang), tetapi TANPA lock.
Sebagai gantinya dipakai compare-and-set: zk.set(..., version=stat.version).
Jika versi /balance sudah berubah sejak dibaca -> BadVersionError -> baca ulang & coba lagi.
"""
from kazoo.client import KazooClient
from kazoo.exceptions import BadVersionError
import time

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

balance_node = "/balance"


def modify_balance_optimistic(amount, jeda=20):
    percobaan = 0
    while True:
        percobaan += 1
        # 1) Baca saldo + versi node
        data, stat = zk.get(balance_node)
        current_balance = int(data.decode('utf-8'))
        print(f"Client B (percobaan {percobaan}) membaca saldo: {current_balance} | versi: {stat.version}")

        # 2) Simulasi pekerjaan lama (hanya pada percobaan pertama)
        if percobaan == 1 and jeda > 0:
            time.sleep(jeda)

        # 3) Tulis bersyarat: hanya berhasil jika versi belum berubah
        new_balance = current_balance + amount
        try:
            zk.set(balance_node, str(new_balance).encode('utf-8'), version=stat.version)
            print(f"Client B memperbarui saldo menjadi: {new_balance} (berhasil, versi {stat.version} -> {stat.version + 1})")
            return percobaan
        except BadVersionError:
            print(f"Client B KONFLIK: versi {stat.version} sudah berubah, data yang dibaca sudah usang. Coba lagi...")


jumlah = modify_balance_optimistic(-300, jeda=0)
print(f"Client B selesai setelah {jumlah} percobaan.")
zk.stop()
