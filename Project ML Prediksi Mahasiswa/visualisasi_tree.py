import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree

import matplotlib.pyplot as plt


# Baca dataset
data = pd.read_csv("newdataset.csv")

# Feature
X = data[["IPS", "Kehadiran"]]

# Target
y = data["Lulus"]

# Buat model
model = DecisionTreeClassifier()

# Training
model.fit(X, y)

# Gambar pohon
plt.figure(figsize=(12,6))

plot_tree(
    model,
    feature_names=["IPS", "Kehadiran"],
    class_names=["Tidak Lulus", "Lulus"],
    filled=True
)

plt.show()