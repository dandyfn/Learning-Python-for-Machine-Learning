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

print("Model selesai belajar")

server_baru = [
    [92, 90, 220, 18]
]

hasil = model.predict(server_baru)

print(hasil)