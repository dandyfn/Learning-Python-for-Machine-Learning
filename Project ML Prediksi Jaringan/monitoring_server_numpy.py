import numpy as np

cpu = np.array([
    20,
    35,
    40,
    50,
    65,
    90,
    95
])

print(cpu)

print("Rata-rata CPU =", cpu.mean())
print("CPU Tertinggi =", cpu.max())
print("CPU Terendah =", cpu.min())
print("Total CPU =", cpu.sum())
overload = cpu > 80

print(overload)
print("Jumlah Server Overload =", overload.sum())
print(cpu[cpu > 80])