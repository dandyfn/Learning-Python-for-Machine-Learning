import pandas as pd
import joblib

from sklearn.tree import DecisionTreeClassifier


# baca dataset
data = pd.read_csv("server_dataset.csv")

# fitur
X = data[
    [
        "CPU",
        "RAM",
        "Latency",
        "PacketLoss"
    ]
]

# target
y = data["Status"]

# training
model = DecisionTreeClassifier()

model.fit(X, y)

# simpan model
joblib.dump(
    model,
    "model_server.pkl"
)

print("Model berhasil disimpan")