
# Nama: Dandy Al-Farisi Natanegara
# NIM: 646000113
# File: harga.py

"""Modul untuk menghitung harga belanja."""


def hitung_total_harga(harga, jumlah, diskon=0):
    """Menghitung total harga setelah diskon.

    Args:
        harga (int atau float): Harga satu barang.
        jumlah (int): Jumlah barang yang dibeli.
        diskon (float): Persentase diskon dari 0 sampai 100.

    Returns:
        float: Total harga setelah diskon.

    Raises:
        ValueError: Jika harga, jumlah, atau diskon tidak valid.
    """
    if harga < 0:
        raise ValueError("Harga tidak boleh negatif.")

    if not isinstance(jumlah, int) or isinstance(jumlah, bool) or jumlah < 0:
        raise ValueError("Jumlah harus bilangan bulat nonnegatif.")

    if not isinstance(diskon, (int, float)) or isinstance(diskon, bool):
        raise ValueError("Diskon harus berupa angka.")

    if not 0 <= diskon <= 100:
        raise ValueError("Diskon harus antara 0 dan 100.")

    total = harga * jumlah
    return total * (1 - diskon / 100)
