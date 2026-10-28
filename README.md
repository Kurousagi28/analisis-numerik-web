# Aplikasi Web Analisis Numerik

Aplikasi web interaktif berbasis **Python Flask** untuk menyelesaikan persoalan pencarian akar persamaan non-linear menggunakan berbagai metode analisis numerik dilengkapi dengan tabel iterasi dan visualisasi kurva grafik (Matplotlib).

## 🚀 Fitur & Metode yang Diimplementasikan

1. **Metode Tabel**
   - Fungsi: $f(x) = x^2 + 3e^x$
   - Dilengkapi tabel pemindaian multi-tahap (4 percobaan) serta deteksi nilai minimum.
2. **Metode Biseksi**
   - Fungsi: $f(x) = 2^x - 2 - x^2$
   - Dilengkapi validasi teorema Bolzano ($f(a) \cdot f(b) < 0$), tabel iterasi galat relatif, dan grafik penentuan akar.
3. **Metode Newton-Raphson & Metode Secant**
   - Perbandingan kedua metode terbuka dengan tabel iterasi konvergensi dan visualisasi grafik perbandingan akar.

---

## 🛠️ Prasyarat & Teknologi

- **Python** (versi 3.9+)
- **Flask** (Framework web)
- **NumPy** (Komputasi numerik)
- **Matplotlib** (Visualisasi grafik)

---

## 💻 Panduan Menjalankan Proyek

### 1. Kloning Repository
```bash
git clone https://github.com/Kurousagi28/analisis-numerik-web.git
cd analisis-numerik-web
```

### 2. Install Dependensi
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
python app.py
```

### 4. Buka di Browser
Buka browser lalu kunjungi:
```
http://127.0.0.1:5000
```
