
# Nama: Dandy Al-Farisi Natanegara
# NIM: 646000113
# File: utama.py

"""Program utama untuk menguji modul mat_mini."""

from functools import lru_cache
from time import perf_counter

import mat_mini


def fibonacci_naif(n):
    """Menghitung Fibonacci tanpa cache."""
    if n < 0:
        raise ValueError("n harus nonnegatif.")

    if n == 0:
        return 0

    if n == 1:
        return 1

    return fibonacci_naif(n - 1) + fibonacci_naif(n - 2)


@lru_cache(maxsize=None)
def fibonacci_cache(n):
    """Menghitung Fibonacci dengan cache."""
    if n < 0:
        raise ValueError("n harus nonnegatif.")

    if n == 0:
        return 0

    if n == 1:
        return 1

    return fibonacci_cache(n - 1) + fibonacci_cache(n - 2)


def main():
    """Menampilkan hasil pengujian fungsi matematika."""
    print("=== UJI FAKTORIAL ===")
    for angka in (0, 1, 5):
        print(f"faktorial({angka}) = {mat_mini.faktorial(angka)}")

    print("\n=== UJI FIBONACCI ===")
    for angka in (0, 1, 6):
        print(f"fibonacci({angka}) = {mat_mini.fibonacci(angka)}")

    print("\n=== UJI FPB ===")
    for a, b in ((12, 8), (24, 18), (7, 0)):
        print(f"fpb({a}, {b}) = {mat_mini.fpb(a, b)}")

    n = 30

    mulai = perf_counter()
    hasil_naif = fibonacci_naif(n)
    waktu_naif = perf_counter() - mulai

    mulai = perf_counter()
    hasil_cache = fibonacci_cache(n)
    waktu_cache = perf_counter() - mulai

    print("\n=== PERBANDINGAN WAKTU FIBONACCI ===")
    print(f"n = {n}")
    print(f"Hasil Fibonacci naif: {hasil_naif}")
    print(f"Waktu Fibonacci naif: {waktu_naif:.6f} detik")
    print(f"Hasil Fibonacci cache: {hasil_cache}")
    print(f"Waktu Fibonacci cache: {waktu_cache:.6f} detik")

    if waktu_cache > 0:
        print(f"Perbandingan waktu: {waktu_naif / waktu_cache:.2f} kali")
    else:
        print("Waktu cache terlalu kecil untuk dibandingkan secara stabil.")

    print("\nKedua fungsi seharusnya menghasilkan nilai yang sama.")


if __name__ == "__main__":
    main()
