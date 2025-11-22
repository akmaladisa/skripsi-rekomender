# Thesis Topic Recommendation System

Aplikasi web berbasis Django yang merekomendasikan topik skripsi kepada mahasiswa berdasarkan riwayat transkrip nilai mereka menggunakan Machine Learning (TF-IDF & Cosine Similarity).

## Fitur Utama

- **Mahasiswa**:
  - Upload transkrip nilai (PDF).
  - Ekstraksi otomatis mata kuliah dan nilai.
  - Rekomendasi topik skripsi yang relevan.
- **Administrator**:
  - Dashboard statistik.
  - Manajemen dataset skripsi.
  - Manajemen pengguna (mahasiswa).

## Prasyarat

- Python 3.10 atau lebih baru.
- `pip` (Python package manager).

## Cara Menjalankan Aplikasi

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal Anda.

### 1. Clone atau Download Repository

Pastikan Anda berada di dalam folder proyek.

### 2. Buat dan Aktifkan Virtual Environment

Disarankan menggunakan virtual environment agar dependensi tidak tercampur.

```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment (Linux/macOS)
source venv/bin/activate

# Aktifkan virtual environment (Windows)
# venv\Scripts\activate
```

### 3. Install Dependensi

Install semua library yang dibutuhkan (Django, Scikit-learn, PyPDF, dll).

```bash
pip install django scikit-learn pandas numpy pypdf
```

### 4. Setup Database

Jalankan migrasi untuk membuat tabel database.

```bash
python manage.py migrate
```

### 5. (Opsional) Isi Data Dummy

Untuk mencoba aplikasi dengan cepat, Anda bisa mengisi database dengan data contoh topik skripsi.

```bash
python manage.py seed_data
```

### 6. Buat Akun Administrator

Buat akun superuser untuk mengakses panel admin.

```bash
python manage.py createsuperuser
```

Atau gunakan script otomatis untuk membuat user `admin_dummy` (password: `adminpassword123`):

```bash
python create_admin_user.py
```

### 7. Jalankan Server

Jalankan server pengembangan Django.

```bash
python manage.py runserver
```

Akses aplikasi di browser:
- **Web App**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel**: [http://127.0.0.1:8000/admin-panel/](http://127.0.0.1:8000/admin-panel/)

### 8. Akun Demo (Kredensial)

Berikut adalah akun dummy yang dapat digunakan untuk pengujian:

**Akun Mahasiswa:**
- **Username**: `test_student`
- **Password**: `password123`

**Akun Administrator:**
- **Username**: `admin_dummy`
- **Password**: `adminpassword123`

## Cara Penggunaan

### Sebagai Mahasiswa
1. Buka halaman utama dan login (atau register jika fitur tersedia, saat ini gunakan user yang dibuat admin).
2. Masuk ke menu **Upload Transcript**.
3. Unggah file PDF transkrip nilai Anda.
4. Klik **View Results** untuk melihat rekomendasi topik skripsi.

### Sebagai Administrator
1. Login dengan akun superuser.
2. Masuk ke **Admin Dashboard**.
3. Kelola dataset skripsi di menu **Manage Dataset**.
4. Lihat log aktivitas di **System Logs**.

## Struktur Proyek

- `accounts/`: Manajemen user dan autentikasi.
- `core/`: Dashboard utama.
- `recommender/`: Logika rekomendasi (ML) dan parsing PDF.
- `templates/`: File HTML (Bootstrap 5).
- `db.sql`: Referensi skema database.
