import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score


# veri setini okuma.
# uyarı spami aldim bu yuzden false a setli, engellemek için
df = pd.read_csv("Smart Home Dataset.csv", low_memory=False)


# time kolonu bozuk geliyor, sayisala cevirme
df["time"] = pd.to_numeric(df["time"], errors="coerce")
df.dropna(subset=["time"], inplace=True)

# unix time -> gercek tarih
df["time"] = pd.to_datetime(df["time"], unit="s")

# saat bilgisi, kiyas icin..
df["hour"] = df["time"].dt.hour

df.head()




# pivot tablo:
# her saat icin EVIN NORMAL ortalma tuketimini cikariyoruz,cunku
#her saatte evin normalde ne kadar enerji harcadigni sayisal bir referans (baseline) olarak cikarmak icin.
# kii modelin yaptigi tahminler bu normal davranis ile karsilastirarak yorumlayabilelim..

pivot_table = pd.pivot_table(
    df,
    index="hour",
    values="use [kW]",
    aggfunc="mean"
)

pivot_table.columns = ["normal_tuketim"]
pivot_table.head()





# modelin kullanacagi ozellikler
features = ["hour", "temperature", "humidity", "pressure"]

# Eksik satirlar var, attim -->-anlamlandiramadigim hatalar cikiyor-
model_df = df[features + ["use [kW]"]].dropna()



X = model_df[features]
y = model_df["use [kW]"]


#           MODEL EGITIMI
"""random forest sectim cunku karmasik ev tuketim davranislarini dogrusal olmayan sekilde ogrenebiliyor kisaca.
R2 skoru 1 e ne kadar yakinsa model o kadar iyi demek."""

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

tahminler = model.predict(X_test)
r2 = r2_score(y_test, tahminler)

print("model R2 skoru:", round(r2, 3))





# ornek bir senaryo 20.saat 
ornek_saat = 20

ornek_veri = pd.DataFrame({
    "hour": [ornek_saat],
    "temperature": [10],
    "humidity": [0.8],
    "pressure": [1013]
})

model_tahmini = model.predict(ornek_veri)[0]
normal_deger = pivot_table.loc[ornek_saat, "normal_tuketim"]

print("Model Tahmini :", round(model_tahmini, 3), "kW")
print("Normal Deger  :", round(normal_deger, 3), "kW")

if model_tahmini > normal_deger * 1.5:
    print("SONUC: TUKETIM NORMALIN UZERINDE (ANORMAL)")
else:
    print("SONUC: TUKETIM NORMAL")



plt.figure()
plt.scatter(y_test, tahminler, alpha=0.5)
plt.xlabel("Gercek Tuketim (kW)")
plt.ylabel("Model Tahmini (kW)")
plt.title("Gercek Degerler vs Model Tahminleri")
plt.grid(True)
plt.show()




plt.figure()
plt.bar(["normal (pivot)", "model tahmini"],
        [normal_deger, model_tahmini])
plt.ylabel("tüketim (kW)")
plt.title(f"{ornek_saat}. saat İcin normal ve tahmin edilen tuketim")
plt.show()




# SUM:

# pivot tablo    = referans davranis
# model          = tahmin mekanizmasi
# karsilastirma  = anormallik analizi


# bu projede pivot tablo kullanilarak
# evin normal tuketim aliskanligi cikarilmistir,
# makine ogrenmesi modeli ile tahmin edilen degerler bu referans ile karsilastirilmistir.


