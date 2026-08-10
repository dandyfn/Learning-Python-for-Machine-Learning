import pandas as pd

data = pd.read_csv("dataset.csv")

print(data)

print("------------------")

print(data.head())
print(data.describe())

print("\nIPS mahasiswa:")
print(data["IPS"])

print("\nKehadiran mahasiswa:")
print(data["Kehadiran"])

print("\nMahasiswa yang lulus:")
print(data[data["Lulus"] == 1])

print("\nMahasiswa yang tidak lulus:")
print(data[data["Lulus"] == 0])