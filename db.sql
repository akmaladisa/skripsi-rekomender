-- =============================================
-- SCRIPT PEMBUATAN STRUKTUR TABEL
-- Project: Rekomendasi Topik Skripsi (Django + Scikit-Learn)
-- Database: PostgreSQL
-- =============================================

-- 1. ENUM untuk Role User
-- Memastikan hanya ada dua jenis role: admin atau mahasiswa
DROP TYPE IF EXISTS user_role_enum CASCADE;
CREATE TYPE user_role_enum AS ENUM ('admin', 'mahasiswa');

-- 2. Tabel Users
-- Tabel ini akan sinkron dengan autentikasi Django
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role_enum DEFAULT 'mahasiswa',
    is_active BOOLEAN DEFAULT TRUE,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabel Profil Mahasiswa
-- Menyimpan data statis mahasiswa sesuai header transkrip 
CREATE TABLE mahasiswa_profil (
    nim VARCHAR(20) PRIMARY KEY, -- NIM Mahasiswa (misal: 230101010046)
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    nama_lengkap VARCHAR(255) NOT NULL, -- (misal: AKMAL ADI SAPUTRA) [cite: 11]
    program_studi VARCHAR(100), -- (misal: PJJ Sistem Informasi) 
    tempat_lahir VARCHAR(100), -- (misal: BOGOR) 
    tanggal_lahir DATE, -- (misal: 2004-11-23) 
    ipk_terakhir NUMERIC(4, 2) DEFAULT 0.00 -- (misal: 4.00) [cite: 21]
);

-- 4. Tabel Dataset Skripsi (Knowledge Base)
-- Tabel ini diisi Admin untuk referensi Machine Learning
CREATE TABLE dataset_skripsi (
    id SERIAL PRIMARY KEY,
    judul_skripsi TEXT NOT NULL,
    abstrak TEXT, -- Kolom vital untuk analisis TF-IDF
    kategori_topik VARCHAR(100), -- Label klasifikasi (misal: Data Mining, IoT)
    kata_kunci VARCHAR(255),
    tahun_lulus INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabel Log Upload Transkrip
-- Menyimpan history file PDF yang diunggah
CREATE TABLE transkrip_upload (
    id SERIAL PRIMARY KEY,
    nim VARCHAR(20) REFERENCES mahasiswa_profil(nim) ON DELETE CASCADE,
    file_path VARCHAR(255) NOT NULL, -- Lokasi file PDF di server Django
    tanggal_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    semester_berjalan INTEGER -- Opsional
);

-- 6. Tabel Detail Nilai (Hasil Ekstraksi PDF)
-- Menyimpan baris per baris mata kuliah dari tabel transkrip 
CREATE TABLE transkrip_detail_nilai (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES transkrip_upload(id) ON DELETE CASCADE,
    kode_mk VARCHAR(20), -- (misal: 200201201) 
    nama_mk VARCHAR(255) NOT NULL, -- (misal: Manajemen Umum) 
    sks INTEGER NOT NULL, -- (misal: 2 atau 3) 
    nilai_huruf VARCHAR(2), -- (misal: A) 
    angka_mutu NUMERIC(3, 2), -- (misal: 4.00) 
    bobot NUMERIC(5, 2) -- (misal: 8 atau 12) 
);

-- 7. Tabel Log Hasil Rekomendasi
-- Menyimpan hasil prediksi yang diberikan sistem ke mahasiswa
CREATE TABLE rekomendasi_log (
    id SERIAL PRIMARY KEY,
    nim VARCHAR(20) REFERENCES mahasiswa_profil(nim) ON DELETE CASCADE,
    skripsi_ref_id INTEGER REFERENCES dataset_skripsi(id), -- Referensi ke judul mirip
    skor_kemiripan NUMERIC(5, 4), -- Nilai Cosine Similarity (0.0 - 1.0)
    alasan_rekomendasi TEXT, -- (misal: "Karena mata kuliah Business Intelligent")
    tanggal_rekomendasi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexing untuk optimasi query Django & ML
CREATE INDEX idx_detail_nilai_nama ON transkrip_detail_nilai(nama_mk);
CREATE INDEX idx_dataset_abstrak ON dataset_skripsi USING gin(to_tsvector('indonesian', abstrak));

-- Verifikasi tabel berhasil dibuat
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';