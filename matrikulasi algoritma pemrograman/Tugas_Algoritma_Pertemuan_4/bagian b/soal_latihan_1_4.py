
# Nama: Dandy Al-Farisi Natanegara
# NIM: 646000113
# File: soal_latihan_1_4.py

"""Latihan fungsi dan rekursi."""


# SOAL 1: Rata-rata dengan variadic arguments
def rata_rata(*nilai):
    """Menghitung rata-rata dari sejumlah nilai.

    Args:
        *nilai: Kumpulan angka yang akan dihitung rata-ratanya.

    Returns:
        float: Nilai rata-rata, atau None jika tidak ada nilai.
    """
    if len(nilai) == 0:
        return None

    return sum(nilai) / len(nilai)


print("=== SOAL 1: RATA-RATA ===")
print("Rata-rata 80, 90 =", rata_rata(80, 90))
print("Rata-rata 70, 80, 90 =", rata_rata(70, 80, 90))
print("Tanpa argumen =", rata_rata())


# SOAL 2: Pangkat dengan rekursi
def pangkat(a, n):
    """Menghitung a pangkat n menggunakan rekursi.

    Args:
        a (int atau float): Bilangan dasar.
        n (int): Pangkat bilangan nonnegatif.

    Returns:
        int atau float: Hasil a pangkat n.

    Raises:
        ValueError: Jika n bukan bilangan bulat nonnegatif.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n harus berupa bilangan bulat nonnegatif.")

    if n == 0:
        return 1

    return a * pangkat(a, n - 1)


print("\n=== SOAL 2: PANGKAT ===")
print("2 pangkat 0 =", pangkat(2, 0))
print("2 pangkat 3 =", pangkat(2, 3))
print("3 pangkat 4 =", pangkat(3, 4))



# SOAL 3: Membalik string dan memeriksa palindrom
def balik_string(teks):
    """Membalik urutan karakter menggunakan rekursi.

    Args:
        teks (str): Teks yang akan dibalik.

    Returns:
        str: Teks dengan urutan karakter terbalik.
    """
    if len(teks) <= 1:
        return teks

    return balik_string(teks[1:]) + teks[0]


def is_palindrom(teks):
    """Memeriksa apakah teks merupakan palindrom.

    Args:
        teks (str): Teks yang diperiksa.

    Returns:
        bool: True jika palindrom, selain itu False.
    """
    teks = teks.lower()

    if len(teks) <= 1:
        return True

    if teks[0] != teks[-1]:
        return False

    return is_palindrom(teks[1:-1])


print("\n=== SOAL 3: STRING DAN PALINDROM ===")
for teks in ("", "a", "katak", "komputer"):
    print(f"Teks: {teks!r}")
    print("Hasil dibalik:", balik_string(teks))
    print("Palindrom:", is_palindrom(teks))



# SOAL 4: Jumlah digit secara rekursif dan iteratif
def jumlah_digit_rekursif(n):
    """Menghitung jumlah digit menggunakan rekursi.

    Args:
        n (int): Bilangan bulat yang dihitung digitnya.

    Returns:
        int: Jumlah seluruh digit bilangan.
    """
    n = abs(n)

    if n < 10:
        return n

    return (n % 10) + jumlah_digit_rekursif(n // 10)


def jumlah_digit_iteratif(n):
    """Menghitung jumlah digit menggunakan perulangan.

    Args:
        n (int): Bilangan bulat yang dihitung digitnya.

    Returns:
        int: Jumlah seluruh digit bilangan.
    """
    n = abs(n)
    total = 0

    while n > 0:
        total += n % 10
        n //= 10

    return total


print("\n=== SOAL 4: JUMLAH DIGIT ===")
for angka in (0, 12345, -987):
    print(f"Angka: {angka}")
    print("Rekursif:", jumlah_digit_rekursif(angka))
    print("Iteratif:", jumlah_digit_iteratif(angka))

