#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 17:24:24 2024

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
    print("Client A (tanpa lock) mulai.")
    current_balance = get_balance()
    print(f"Client A membaca saldo: {current_balance}")
    time.sleep(20)
    new_balance = current_balance + amount
    print(f"Client A memperbarui saldo menjadi: {new_balance}")
    set_balance(new_balance)
    print("Client A selesai.")

# Modifikasi saldo dengan menambah 500
modify_balance(500)

# Stop ZooKeeper client
zk.stop()
