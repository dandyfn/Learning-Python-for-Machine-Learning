import joblib

model = joblib.load("model_server.pkl")

print("Model berhasil dimuat")
print("Masukkan kondisi server:")

cpu = int(input("CPU (%): "))
ram = int(input("RAM (%): "))
latency = int(input("Latency (ms): "))
packetloss = int(input("Packet Loss (%): "))

data_baru = [
    [cpu, ram, latency, packetloss]
]

hasil = model.predict(data_baru)

information =  False
if hasil[0] == 1:
    information = True
    print("Status Server: NORMAL")
else:
    information = False
    print("Status Server: BERMASALAH")

if information == False:

    print("\n=== Diagnosa Masalah ===")

    if cpu >= 80:
        print("- Penggunaan CPU terlalu tinggi")

    if ram >= 80:
        print("- Penggunaan RAM terlalu tinggi")

    if latency >= 100:
        print("- Latency jaringan terlalu tinggi")

    if packetloss >= 10:
        print("- Packet Loss tinggi")

    print("=======================")