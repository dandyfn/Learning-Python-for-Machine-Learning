import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score


data = pd.read_csv("dataset.csv")

X = data[["IPS", "Kehadiran"]]

y = data["Lulus"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Jumlah Training:", len(X_train))
print("Jumlah Testing :", len(X_test))


model = DecisionTreeClassifier()

model.fit(X_train, y_train)

print("\nModel selesai belajar")


prediksi = model.predict(X_test)

print("\nPrediksi Model:")
print(prediksi)

print("\nJawaban Asli:")
print(y_test.values)


akurasi = accuracy_score(
    y_test,
    prediksi
)

print("\nAkurasi =", akurasi)