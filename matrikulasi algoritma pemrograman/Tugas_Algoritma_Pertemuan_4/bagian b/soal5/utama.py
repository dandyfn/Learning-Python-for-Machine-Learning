
# Nama: Dandy Al-Farisi Natanegara
# NIM: 646000113
# File: utama.py

"""Program utama untuk menghitung total belanja."""

from harga import hitung_total_harga


def main():
    """Menjalankan contoh perhitungan total belanja."""
    print("=== PROGRAM PERHITUNGAN HARGA ===")

    harga_barang = 20000
    jumlah_barang = 3
    diskon = 10

    total = hitung_total_harga(
        harga_barang,
        jumlah_barang,
        diskon
    )

    print(f"Harga satuan : Rp{harga_barang:,.0f}")
    print(f"Jumlah barang: {jumlah_barang}")
    print(f"Diskon       : {diskon}%")
    print(f"Total harga  : Rp{total:,.0f}")


if __name__ == "__main__":
    main()
