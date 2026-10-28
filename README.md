# 🧮 Web Analisis Numerik — Pencarian Akar Persamaan Non-Linier

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-11557c?style=for-the-badge)](https://matplotlib.org/)
[![Tests](https://img.shields.io/badge/Tests-Passing-success?style=for-the-badge&logo=githubactions&logoColor=white)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

Aplikasi web interaktif komputasi numerik berbasis **Python Flask** untuk menyelesaikan persoalan pencarian akar persamaan non-linear (*root-finding algorithms*). Dilengkapi dengan kalkulasi otomatis multi-iterasi, tabel data bertingkat, kesimpulan matematis dinamis, dan visualisasi kurva fungsi resolusi tinggi secara *real-time* menggunakan **Matplotlib**.

---

## 📑 Daftar Isi

- [Fitur & Metode Numerik](#-fitur--metode-numerik)
  - [1. Metode Tabel](#1-metode-tabel)
  - [2. Metode Biseksi](#2-metode-biseksi)
  - [3. Metode Newton-Raphson & Secant](#3-metode-newton-raphson--secant)
- [Struktur Proyek](#-struktur-proyek)
- [Prasyarat Sistem](#-prasyarat-sistem)
- [Panduan Instalasi & Menjalankan](#-panduan-instalasi--menjalankan)
- [Menjalankan Pengujian Otomatis (Testing)](#-menjalankan-pengujian-otomatis-testing)
- [Informasi Pengembang / Penyusun](#-informasi-pengembang--penyusun)
- [Lisensi](#-lisensi)

---

## 🔬 Fitur & Metode Numerik

### 1. Metode Tabel
* **Persamaan:**  
  $$f(x) = x^2 + 3e^x$$
* **Karakteristik & Fitur:**
  * Memindai nilai fungsi melalui **4 tahap percobaan selang bertingkat** ($N = 10$).
  * Deteksi otomatis titik minimum lokal pada selang pencarian.
  * Menghasilkan grafik fungsi interaktif yang membuktikan secara visual bahwa kurva selalu berada di atas sumbu $x$ ($f(x) > 0$), sehingga persamaan **tidak memiliki akar real**.

### 2. Metode Biseksi (Bisection Method)
* **Persamaan:**  
  $$f(x) = 2^x - 2 - x^2$$
* **Karakteristik & Fitur:**
  * Metode tertutup (*bracketing method*) dengan batas awal bawaan $x_i = 3.0$ dan $x_u = 5.0$.
  * Validasi otomatis Teorema Nilai Antara (Bolzano): $f(x_i) \cdot f(x_u) < 0$.
  * Perhitungan galat aproksimasi relatif:
    $$\varepsilon_a = \left| \frac{x_{r}^{\text{baru}} - x_{r}^{\text{lama}}}{x_{r}^{\text{baru}}} \right| \times 100\%$$
  * Tabel iterasi dinamis dan plot grafik penanda letak akar eksak.

### 3. Metode Newton-Raphson & Secant
* **Persamaan:**  
  $$f(x) = x^2 + e^{-2x} \sin(x)$$
* **Turunan Pertama Analitik:**  
  $$f'(x) = 2x - 2e^{-2x} \sin(x) + e^{-2x} \cos(x)$$
* **Karakteristik & Fitur:**
  * **Halaman komparatif**: Membandingkan kecepatan konvergensi Metode Terbuka secara langsung.
  * **Newton-Raphson**: Menggunakan 1 tebakan awal ($x_0 = 0.5$) dan turunan pertama analitik:
    $$x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}$$
  * **Metode Secant**: Menggunakan 2 tebakan awal ($x_{r-1} = 0.5$, $x_r = 10.0$):
    $$x_{r+1} = x_r - \frac{f(x_r)(x_r - x_{r-1})}{f(x_r) - f(x_{r-1})}$$
  * Dilengkapi grafik ganda (*subplot*): Tinjauan domain luas dan perbesaran area konvergensi di sekitar akar $x \approx 0$.

---

## 📂 Struktur Proyek

```text
analisis-numerik-web/
├── app.py                  # Entry point aplikasi Flask & kontroler algoritma numerik
├── requirements.txt        # Daftar pustaka dependensi Python
├── LICENSE                 # Lisensi open-source (MIT)
├── .gitignore              # Konfigurasi file yang diabaikan oleh Git
├── .gitattributes         # Konfigurasi normalisasi baris (line endings)
├── README.md               # Dokumentasi utama proyek
├── static/                 # Aset statis web
│   ├── style.css           # Styling kustom (desain modern, responsif & bersih)
│   └── favicon.svg         # Ikon vektor tab peramban (Favicon)
├── templates/              # Berkas HTML template (Jinja2)
│   ├── index.html          # Halaman beranda / navigasi utama
│   ├── tabel.html          # Halaman kalkulator Metode Tabel
│   ├── biseksi.html        # Halaman kalkulator Metode Biseksi
│   └── newton_secant.html  # Halaman perbandingan Newton-Raphson & Secant
└── tests/                  # Berkas pengujian unit (Automated Testing)
    ├── __init__.py         # Inisialisasi modul paket pengujian
    └── test_routes.py      # Pengujian fungsionalitas rute web & kalkulasi
```

---

## ⚙️ Prasyarat Sistem

- **Python**: Versi 3.9 ke atas
- **pip**: Package installer untuk Python
- Peramban web modern (Google Chrome, Firefox, Microsoft Edge, dll.)

---

## 🚀 Panduan Instalasi & Menjalankan

### 1. Kloning Repository
```bash
git clone https://github.com/Kurousagi28/analisis-numerik-web.git
cd analisis-numerik-web
```

### 2. (Opsional) Gunakan Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi Web
```bash
python app.py
```

### 5. Akses Melalui Browser
Buka peramban dan akses alamat berikut:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)** atau **[http://localhost:5000](http://localhost:5000)**

---

## 🧪 Menjalankan Pengujian Otomatis (Testing)

Proyek ini telah dilengkapi dengan unit test otomatis untuk menjamin seluruh rute `GET` dan proses kalkulasi formulir `POST` berfungsi tanpa kesalahan.

Jalankan perintah berikut di terminal:
```bash
python -m unittest discover tests
```
*Hasil yang diharapkan: `Ran 4 tests in ...s - OK`*

---

## 👤 Informasi Pengembang / Penyusun

| Parameter | Data Mahasiswa |
| :--- | :--- |
| **Nama Lengkap** | Elfandy Dear Adhani |
| **NIM** | *(Isi NIM Anda di sini)* |
| **Kelas / Paralel** | *(Isi Kelas Anda di sini)* |
| **Program Studi** | *(Isi Program Studi di sini)* |
| **Mata Kuliah** | Analisis Numerik / Komputasi Numerik |
| **Dosen Pengampu** | *(Isi Nama Dosen Pengampu di sini)* |

---

## 📄 Lisensi

Proyek ini didistribusikan di bawah lisensi **MIT License**. Lihat berkas [LICENSE](LICENSE) untuk rincian lebih lanjut.
