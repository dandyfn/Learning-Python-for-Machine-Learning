import pandas as pd

from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("server_dataset.csv")

X = data[
    [
        "CPU",
        "RAM",
        "Latency",
        "PacketLoss"
    ]
]

y = data["Status"]

model = DecisionTreeClassifier()

model.fit(X, y)

print("Model selesai belajar, coba masukan data kondisi perangkat jaringan : ")

cpu = int(input("CPU (%): "))
ram = int(input("RAM (%): "))
latency = int(input("Latency (ms): "))
packetloss = int(input("Packet Loss (%): "))

data_baru = [
    [cpu, ram, latency, packetloss]
]

hasil = model.predict(data_baru)

if hasil[0] == 1:
    print("Status Server: NORMAL")
else:
    print("Status Server: BERMASALAH")
    