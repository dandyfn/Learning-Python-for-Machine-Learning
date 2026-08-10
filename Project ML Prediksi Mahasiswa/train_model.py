import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("newdataset.csv")

X = data[["IPS", "Kehadiran"]]

y = data["Lulus"]

print("Fitur:")
print(X)

print("\nTarget:")
print(y)

model = DecisionTreeClassifier()

model.fit(X, y)

print("Model berhasil dilatih")
hasil = model.predict([[3.0,95]])

print(hasil)