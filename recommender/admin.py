from django.contrib import admin
from .models import DatasetSkripsi, TranskripUpload, TranskripDetailNilai, RekomendasiLog

@admin.register(DatasetSkripsi)
class DatasetSkripsiAdmin(admin.ModelAdmin):
    list_display = ('judul_skripsi', 'kategori_topik', 'tahun_lulus')
    search_fields = ('judul_skripsi', 'abstrak')

@admin.register(TranskripUpload)
class TranskripUploadAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'tanggal_upload')

@admin.register(TranskripDetailNilai)
class TranskripDetailNilaiAdmin(admin.ModelAdmin):
    list_display = ('upload', 'nama_mk', 'nilai_huruf', 'sks')
    list_filter = ('nilai_huruf',)

@admin.register(RekomendasiLog)
class RekomendasiLogAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'skripsi_ref', 'skor_kemiripan', 'tanggal_rekomendasi')
