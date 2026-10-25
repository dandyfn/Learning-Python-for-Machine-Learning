# Nama: Dandy Al-Farisi Natanegara
# NIM: 646000113
# File: mat_mini.py

"""Modul mini untuk operasi matematika rekursif."""


def faktorial(n):
    """Menghitung faktorial dari bilangan bulat nonnegatif.

    Args:
        n (int): Bilangan yang akan dihitung faktorialnya.

    Returns:
        int: Hasil faktorial n.

    Raises:
        ValueError: Jika n bukan bilangan bulat nonnegatif.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n harus berupa bilangan bulat nonnegatif.")

    if n == 0 or n == 1:
        return 1

    return n * faktorial(n - 1)


def fibonacci(n):
    """Menghitung bilangan Fibonacci secara rekursif.

    Args:
        n (int): Indeks Fibonacci yang dimulai dari 0.

    Returns:
        int: Bilangan Fibonacci ke-n.

    Raises:
        ValueError: Jika n bukan bilangan bulat nonnegatif.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n harus berupa bilangan bulat nonnegatif.")

    if n == 0:
        return 0

    if n == 1:
        return 1

    return fibonacci(n - 1) + fibonacci(n - 2)


def fpb(a, b):
    """Menghitung FPB menggunakan algoritma Euclid.

    Args:
        a (int): Bilangan bulat nonnegatif pertama.
        b (int): Bilangan bulat nonnegatif kedua.

    Returns:
        int: Faktor persekutuan terbesar dari a dan b.

    Raises:
        ValueError: Jika input tidak valid atau keduanya nol.
    """
    input_valid = (
        isinstance(a, int)
        and not isinstance(a, bool)
        and isinstance(b, int)
        and not isinstance(b, bool)
        and a >= 0
        and b >= 0
    )

    if not input_valid:
        raise ValueError("a dan b harus bilangan bulat nonnegatif.")

    if a == 0 and b == 0:
        raise ValueError("a dan b tidak boleh keduanya nol.")

    if b == 0:
        return a

    return fpb(b, a % b)


if __name__ == "__main__":
    print("Uji faktorial:", faktorial(5))
    print("Uji Fibonacci:", fibonacci(6))
    print("Uji FPB:", fpb(24, 18))