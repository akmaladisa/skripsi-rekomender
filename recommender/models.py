from django.db import models
from accounts.models import Mahasiswa

class DatasetSkripsi(models.Model):
    judul_skripsi = models.TextField()
    abstrak = models.TextField(null=True, blank=True)
    kategori_topik = models.CharField(max_length=100, null=True, blank=True)
    kata_kunci = models.CharField(max_length=255, null=True, blank=True)
    tahun_lulus = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul_skripsi

class TranskripUpload(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='transkrip_uploads')
    file_path = models.FileField(upload_to='transkrip/')
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    semester_berjalan = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Transkrip {self.mahasiswa.nim} - {self.tanggal_upload}"

class TranskripDetailNilai(models.Model):
    upload = models.ForeignKey(TranskripUpload, on_delete=models.CASCADE, related_name='detail_nilai')
    kode_mk = models.CharField(max_length=20, null=True, blank=True)
    nama_mk = models.CharField(max_length=255)
    sks = models.IntegerField()
    nilai_huruf = models.CharField(max_length=2, null=True, blank=True)
    angka_mutu = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    bobot = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.nama_mk} ({self.nilai_huruf})"

class RekomendasiLog(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='rekomendasi_logs')
    skripsi_ref = models.ForeignKey(DatasetSkripsi, on_delete=models.CASCADE, null=True, blank=True)
    skor_kemiripan = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    alasan_rekomendasi = models.TextField(null=True, blank=True)
    tanggal_rekomendasi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rekomendasi for {self.mahasiswa.nim} - {self.skor_kemiripan}"
