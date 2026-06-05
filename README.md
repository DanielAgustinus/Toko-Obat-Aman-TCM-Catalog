# 中药目录 — Katalog Online Obat Tradisional Chinese

Panduan lengkap membangun katalog online untuk toko obat tradisional Chinese
menggunakan **Python + FastAPI**.

---

## Daftar Isi

1. [Struktur Project](#1-struktur-project)
2. [Instalasi & Setup](#2-instalasi--setup)
3. [Menjalankan Aplikasi](#3-menjalankan-aplikasi)
4. [Arsitektur & Penjelasan Kode](#4-arsitektur--penjelasan-kode)
5. [Menambah Data Produk](#5-menambah-data-produk)
6. [Menggunakan REST API](#6-menggunakan-rest-api)
7. [Kustomisasi Tampilan](#7-kustomisasi-tampilan)
8. [Deploy ke Production](#8-deploy-ke-production)
9. [Pengembangan Lanjutan](#9-pengembangan-lanjutan)

---

## 1. Struktur Project

```
tcm-catalog/
├── main.py              ← Aplikasi utama FastAPI (routing & endpoint)
├── models.py            ← Data model Pydantic (Herb, Search, dll)
├── database.py          ← Layer penyimpanan data (CRUD operations)
├── requirements.txt     ← Daftar library Python yang dibutuhkan
├── data/
│   └── herbs.json       ← Data produk herbal (8 contoh siap pakai)
├── templates/
│   ├── base.html        ← Template dasar (navigasi, footer)
│   ├── index.html       ← Halaman beranda
│   ├── katalog.html     ← Halaman katalog + filter
│   ├── detail.html      ← Halaman detail produk
│   ├── tentang.html     ← Halaman tentang toko
│   └── 404.html         ← Halaman error
└── static/
    ├── css/
    │   └── style.css    ← Stylesheet utama
    ├── js/              ← (untuk JavaScript tambahan)
    └── images/          ← Folder gambar produk
```

---

## 2. Instalasi & Setup

### Prasyarat
- Python 3.11 atau lebih baru
- pip (package manager Python)
- Terminal / Command Prompt

### Langkah-langkah

```bash
# 1. Buat folder project
mkdir tcm-catalog
cd tcm-catalog

# 2. Buat virtual environment (sangat disarankan)
python -m venv venv

# 3. Aktifkan virtual environment
#    Windows:
venv\Scripts\activate
#    macOS/Linux:
source venv/bin/activate

# 4. Install semua dependency
pip install -r requirements.txt
```

### Penjelasan Library
| Library           | Fungsi                                            |
|-------------------|---------------------------------------------------|
| `fastapi`         | Framework web utama (routing, API, validasi)      |
| `uvicorn`         | ASGI server untuk menjalankan FastAPI              |
| `jinja2`          | Template engine untuk render halaman HTML          |
| `python-multipart`| Menangani form data & file upload                  |
| `aiofiles`        | Serve static file secara async                     |
| `pydantic`        | Validasi data & model definition                   |

---

## 3. Menjalankan Aplikasi

```bash
# Jalankan server development (dengan auto-reload)
python main.py

# ATAU langsung dengan uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Buka browser dan akses:

| URL                          | Halaman                    |
|------------------------------|----------------------------|
| http://localhost:8000        | Beranda                    |
| http://localhost:8000/katalog | Katalog lengkap + filter  |
| http://localhost:8000/herb/1 | Detail produk (contoh ID 1)|
| http://localhost:8000/tentang | Tentang toko              |
| http://localhost:8000/docs   | API Documentation (Swagger)|
| http://localhost:8000/redoc  | API Documentation (ReDoc)  |

---

## 4. Arsitektur & Penjelasan Kode

### 4a. Model Data (`models.py`)

Semua model menggunakan Pydantic untuk validasi otomatis:

- **`KategoriObat`** — Enum kategori: herbal, akar, bunga, daun, biji, dll.
- **`SifatObat`** — Sifat dalam TCM: panas (热), hangat (温), netral (平), sejuk (凉), dingin (寒)
- **`RasaObat`** — Lima Rasa TCM: manis (甘), pahit (苦), pedas (辛), asam (酸), asin (咸)
- **`Herb`** — Model utama produk dengan 18 field lengkap
- **`HerbCreate`** / **`HerbUpdate`** — Model untuk operasi tambah/edit
- **`SearchQuery`** — Model pencarian multi-filter

### 4b. Database Layer (`database.py`)

Menggunakan JSON file sebagai penyimpanan (mudah untuk prototype):

- `get_all_herbs()` — Ambil semua produk
- `get_herb_by_id(id)` — Ambil satu produk
- `search_herbs(query)` — Cari dengan multi-filter
- `create_herb(data)` — Tambah produk baru
- `update_herb(id, data)` — Update produk
- `delete_herb(id)` — Hapus produk

### 4c. Routing (`main.py`)

Aplikasi punya 2 jenis endpoint:

**Halaman Web (HTML):**
- `GET /` → Beranda dengan produk populer
- `GET /katalog` → Daftar produk + pencarian + filter
- `GET /herb/{id}` → Detail satu produk
- `GET /tentang` → Halaman tentang

**REST API (JSON):**
- `GET /api/herbs` → List semua (dengan filter)
- `GET /api/herbs/{id}` → Detail satu
- `POST /api/herbs` → Tambah baru
- `PUT /api/herbs/{id}` → Update
- `DELETE /api/herbs/{id}` → Hapus
- `GET /api/summary` → Ringkasan katalog

---

## 5. Menambah Data Produk

### Cara 1: Edit langsung file JSON

Buka `data/herbs.json` dan tambahkan objek baru:

```json
{
  "id": 9,
  "nama_indonesia": "Cordyceps",
  "nama_chinese": "冬虫夏草",
  "nama_pinyin": "Dōng Chóng Xià Cǎo",
  "nama_latin": "Ophiocordyceps sinensis",
  "kategori": "jamur",
  "sifat": "hangat",
  "rasa": ["manis"],
  "meridian": ["Paru-paru", "Ginjal"],
  "khasiat": "Menguatkan paru dan ginjal, menambah energi",
  "deskripsi": "Cordyceps adalah jamur langka...",
  "cara_pakai": "Rebus 3-5 gram...",
  "dosis": "3-9 gram per hari",
  "peringatan": "Konsultasikan dengan dokter...",
  "harga": 250000,
  "satuan": "5 gram",
  "stok": 20,
  "gambar": "",
  "populer": true
}
```

### Cara 2: Via API (menggunakan curl atau Postman)

```bash
curl -X POST http://localhost:8000/api/herbs \
  -H "Content-Type: application/json" \
  -d '{
    "nama_indonesia": "Cordyceps",
    "nama_chinese": "冬虫夏草",
    "nama_pinyin": "Dōng Chóng Xià Cǎo",
    "kategori": "jamur",
    "sifat": "hangat",
    "rasa": ["manis"],
    "khasiat": "Menguatkan paru dan ginjal",
    "deskripsi": "Cordyceps adalah jamur langka...",
    "harga": 250000,
    "satuan": "5 gram",
    "stok": 20,
    "populer": true
  }'
```

### Cara 3: Via Swagger UI

Buka http://localhost:8000/docs → klik **POST /api/herbs** → Try it out.

---

## 6. Menggunakan REST API

### Pencarian dengan Filter

```bash
# Cari berdasarkan keyword
GET /api/herbs?q=ginseng

# Filter berdasarkan kategori
GET /api/herbs?kategori=akar

# Filter berdasarkan sifat
GET /api/herbs?sifat=hangat

# Kombinasi filter
GET /api/herbs?q=darah&sifat=hangat&min_harga=30000&max_harga=100000

# Hanya yang stok tersedia
GET /api/herbs?hanya_stok=true

# Hanya produk populer
GET /api/herbs?hanya_populer=true
```

### Contoh Response

```json
{
  "id": 1,
  "nama_indonesia": "Ginseng",
  "nama_chinese": "人参",
  "nama_pinyin": "Rén Shēn",
  "nama_latin": "Panax ginseng",
  "kategori": "akar",
  "sifat": "hangat",
  "rasa": ["manis", "pahit"],
  "meridian": ["Paru-paru", "Limpa", "Jantung"],
  "khasiat": "Menguatkan Qi, menyehatkan limpa...",
  "harga": 85000,
  "satuan": "10 gram",
  "stok": 50,
  "populer": true
}
```

---

## 7. Kustomisasi Tampilan

### Mengubah Warna
Edit CSS variables di `static/css/style.css`:

```css
:root {
    --red:        #b5403a;   /* Warna utama (aksen) */
    --gold:       #c8a44e;   /* Warna emas */
    --ink:        #1a1612;   /* Warna teks utama */
    --parchment:  #f5f0e8;   /* Warna background */
    --cream:      #faf8f4;   /* Warna background terang */
}
```

### Menambah Gambar Produk
1. Letakkan file gambar di `static/images/`
2. Update field `gambar` di `data/herbs.json`:
   ```json
   "gambar": "/static/images/nama-file.jpg"
   ```
3. Untuk menampilkan gambar, edit `herb-card-img` di template

### Mengubah Font
Ganti Google Fonts URL di `base.html` dan update CSS variables.

---

## 8. Deploy ke Production

### Opsi A: Railway / Render (Gratis)

1. Push kode ke GitHub
2. Buat akun di railway.app atau render.com
3. Connect GitHub repository
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Opsi B: VPS (DigitalOcean / Contabo)

```bash
# 1. Install di server
sudo apt update && sudo apt install python3-pip python3-venv

# 2. Clone & setup
git clone <repo-url> /opt/tcm-catalog
cd /opt/tcm-catalog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Jalankan dengan Gunicorn (production ASGI server)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# 4. Setup Nginx sebagai reverse proxy
# 5. Setup SSL dengan Let's Encrypt
```

### Opsi C: Docker

Buat `Dockerfile`:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t tcm-catalog .
docker run -p 8000:8000 tcm-catalog
```

---

## 9. Pengembangan Lanjutan

Berikut ide-ide untuk mengembangkan katalog ini lebih lanjut:

- **Database PostgreSQL/SQLite** — Ganti JSON dengan SQLAlchemy ORM
- **Autentikasi Admin** — Tambah login untuk kelola produk via web
- **Upload Gambar** — Form upload foto produk langsung dari browser
- **Keranjang Belanja** — Fitur cart + integrasi payment gateway
- **WhatsApp Order** — Tombol "Pesan via WhatsApp" di setiap produk
- **Pencarian Gejala** — User input gejala → rekomendasi herbal
- **Multi-bahasa** — Tambah pilihan bahasa (ID / CN / EN)
- **PWA** — Jadikan Progressive Web App agar bisa dibuka offline
- **SEO** — Tambahkan meta tags, sitemap, schema markup

---

## Teknologi yang Digunakan

| Teknologi    | Versi    | Peran                          |
|-------------|----------|--------------------------------|
| Python      | 3.11+    | Bahasa pemrograman utama       |
| FastAPI     | 0.115    | Web framework                  |
| Pydantic    | 2.9      | Validasi data & model          |
| Jinja2      | 3.1      | Template engine (HTML)         |
| Uvicorn     | 0.30     | ASGI server                    |
| HTML/CSS    | —        | Frontend & styling             |

---

*Dibuat untuk toko obat tradisional Chinese — 中药铺*
