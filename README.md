# Akıllı Ev Enerji Tüketimi Analizi ve Tahmini

Bu proje, bir akıllı eve ait enerji tüketim verileri kullanılarak
makine öğrenmesi ile tüketim tahmini yapılmasını ve
bu tahminlerin geçmişteki **normal tüketim alışkanlıkları** ile
karşılaştırılmasını amaçlamaktadır.

Proje özellikle **pivot tablo kullanımı** üzerine kuruludur.
Çünkü model çıktılarının yorumlanabilmesi için
bir referans (baseline) değere ihtiyaç vardır.

---

## Projenin Amacı

- Saat ve çevresel koşullara göre evin enerji tüketimini tahmin etmek  
- Geçmiş verilere bakarak evin **normal tüketim davranışını** çıkarmak  
- Tahmin edilen değer ile normal değer arasında karşılaştırma yaparak
  tüketimin **normal mi yoksa anormal mi** olduğunu yorumlamak  

Bu proje sadece tahmin üretmek için değil,
üretilen tahminlerin **anlamlı hale getirilmesi** için yapılmıştır.

---

## Kullanılan Veri Seti

Veri setinde aşağıdaki bilgiler bulunmaktadır:

- Zaman bilgisi (Unix time)
- Toplam enerji tüketimi (`use [kW]`)
- Sıcaklık (`temperature`)
- Nem (`humidity`)
- Basınç (`pressure`)

Zaman verisi saat bilgisine dönüştürülmüştür.
Çünkü makine öğrenmesi modeli zamanı bu şekilde daha anlamlı öğrenmektedir.

---

## Pivot Tablo (En Önemli Kısım)

Pivot tablo kullanılarak:

- Günün **her saati için**
- Evin geçmişteki **ortalama (normal) enerji tüketimi** hesaplanmıştır

Bu tablo, evin alışkanlıklarını temsil eden
sayısal bir **referans noktası (baseline)** olarak kullanılmıştır.

### Pivot Tablo Neden Zorunludur?

Model yalnızca bir sayı tahmin eder.
Ancak bu sayının:

- normal mi
- yoksa anormal mi

olduğunu anlayabilmek için geçmişteki normal davranışı bilmek gerekir.

Pivot tablo olmadan:
- Tahmin yapılabilir
- Ancak sonuç **yorumlanamaz**

Bu nedenle pivot tablo bu projenin temelini oluşturmaktadır.

---

## Kullanılan Makine Öğrenmesi Modeli

Bu proje bir **regresyon problemidir**.
Çünkü tahmin edilen değer (enerji tüketimi) sürekli bir sayıdır.

### Kullanılan Model
- Random Forest Regressor

### Neden Random Forest?
- Enerji tüketimi doğrusal değildir
- Random Forest karmaşık ilişkileri iyi öğrenir
- Gürültülü verilerde daha kararlı sonuçlar verir

Model başarımı **R2 skoru** ile ölçülmüştür.

---

## Grafikler ve Görsel Analiz

### 1. Gerçek Değerler vs Model Tahminleri

Aşağıdaki grafik, modelin gerçek tüketim değerlerine
ne kadar yakın tahminler yaptığını göstermektedir.

![Gercek vs Tahmin](ekran1.png)

**Açıklama:**  
Noktalar diyagonal çizgiye yaklaştıkça modelin başarımı artar.
Grafik genel olarak modelin eğilimi öğrendiğini göstermektedir.

---

### 2. Model Çıktısı ve Sayısal Sonuç

Aşağıda modelin R2 skoru,
seçilen saat için yaptığı tahmin
ve pivot tablodan gelen normal değer görülmektedir.

![Model Sonucu](ekran2.png)

**Açıklama:**  
Modelin ürettiği tahmin,
pivot tablodan gelen normal değer ile karşılaştırılarak
tüketimin normal olduğu sonucuna varılmıştır.

---

### 3. Normal Tüketim vs Model Tahmini (Saat Bazlı)

Seçilen bir saat için,
normal tüketim ile model tahmini aşağıdaki grafikte gösterilmiştir.

![Normal vs Tahmin](ekran3.png)

**Açıklama:**  
Bu grafik, pivot tablonun neden kullanıldığını net bir şekilde göstermektedir.
Model tahmini, normal tüketim referansı ile doğrudan karşılaştırılabilmektedir.

---

## Sonuç

Bu projede:

- Pivot tablo kullanılarak evin normal enerji tüketim profili çıkarılmış
- Makine öğrenmesi modeli ile tüketim tahmini yapılmış
- Tahminler, pivot tablodaki normal değerlerle karşılaştırılmıştır

Sonuç olarak bu çalışma,
sadece tahmin yapan bir model değil,
aynı zamanda bu tahminleri anlamlı hale getiren
bir analiz çalışmasıdır.

Bu yaklaşım, akıllı ev sistemlerinde
anormal enerji tüketimlerinin tespit edilmesi için
gerçek hayatta kullanılabilir.

---

## Final Sınavı İçin Kısa Not

- Pivot tablo → **normal davranış**
- Model → **tahmin**
- Karşılaştırma → **yorum ve analiz**

Pivot olmadan bu proje eksik kalır.
