#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 17:37:17 2024

@author: widhi
"""

from kazoo.client import KazooClient
import time

# Inisialisasi klien ZooKeeper
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

# Node yang menyimpan saldo
balance_node = "/balance"

# Fungsi untuk membaca saldo dari ZooKeeper
def get_balance():
    data, _ = zk.get(balance_node)
    return int(data.decode('utf-8'))

# Fungsi untuk memperbarui saldo di ZooKeeper
def set_balance(new_balance):
    zk.set(balance_node, str(new_balance).encode('utf-8'))

# Fungsi untuk melakukan modifikasi saldo
def modify_balance(amount):
    # [3D] TANPA LOCK: acquire/release dihapus, bagian kritis langsung dijalankan
    print("Client B (tanpa lock) mulai.")
    current_balance = get_balance()
    print(f"Client B membaca saldo: {current_balance}")
    new_balance = current_balance + amount
    print(f"Client B memperbarui saldo menjadi: {new_balance}")
    set_balance(new_balance)
    time.sleep(2)
    print("Client B selesai.")

# Modifikasi saldo dengan mengurangi 300
modify_balance(-300)

# Stop ZooKeeper client
zk.stop()
