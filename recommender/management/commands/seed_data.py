from django.core.management.base import BaseCommand
from recommender.models import DatasetSkripsi

class Command(BaseCommand):
    help = 'Seeds the database with dummy thesis topics'

    def handle(self, *args, **kwargs):
        data = [
            {
                'judul': 'Penerapan Data Mining Untuk Prediksi Penjualan Menggunakan Algoritma Apriori',
                'abstrak': 'Penelitian ini membahas tentang prediksi penjualan barang di toko X menggunakan algoritma Apriori. Data mining digunakan untuk menemukan pola pembelian konsumen.',
                'kategori': 'Data Mining',
                'keywords': 'Data Mining, Apriori, Prediksi, Penjualan'
            },
            {
                'judul': 'Rancang Bangun Sistem Informasi Akademik Berbasis Web',
                'abstrak': 'Sistem informasi akademik ini dibangun menggunakan PHP dan MySQL untuk memudahkan pengelolaan data mahasiswa dan nilai.',
                'kategori': 'Sistem Informasi',
                'keywords': 'Sistem Informasi, Web, PHP, MySQL'
            },
            {
                'judul': 'Analisis Sentimen Pengguna Twitter Terhadap Pilpres Menggunakan Naive Bayes',
                'abstrak': 'Analisis sentimen ini bertujuan untuk mengetahui opini masyarakat mengenai calon presiden. Metode yang digunakan adalah Naive Bayes Classifier.',
                'kategori': 'Machine Learning',
                'keywords': 'Analisis Sentimen, Naive Bayes, Twitter, Pilpres'
            },
            {
                'judul': 'Implementasi Internet of Things (IoT) Pada Smart Home Berbasis Arduino',
                'abstrak': 'Sistem smart home ini memungkinkan pengguna mengontrol lampu dan kipas angin dari jarak jauh menggunakan aplikasi Android dan Arduino.',
                'kategori': 'IoT',
                'keywords': 'IoT, Smart Home, Arduino, Android'
            },
            {
                'judul': 'Pengembangan Game Edukasi Matematika Untuk Anak SD Berbasis Android',
                'abstrak': 'Game edukasi ini dirancang untuk membantu siswa SD belajar matematika dengan cara yang menyenangkan. Menggunakan Unity 3D.',
                'kategori': 'Game Development',
                'keywords': 'Game Edukasi, Android, Unity, Matematika'
            }
        ]

        for item in data:
            DatasetSkripsi.objects.create(
                judul_skripsi=item['judul'],
                abstrak=item['abstrak'],
                kategori_topik=item['kategori'],
                kata_kunci=item['keywords'],
                tahun_lulus=2023
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(data)} thesis topics.'))
