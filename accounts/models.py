from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('mahasiswa', 'Mahasiswa'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='mahasiswa')

    def __str__(self):
        return self.username

class Mahasiswa(models.Model):
    nim = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mahasiswa_profile')
    nama_lengkap = models.CharField(max_length=255)
    program_studi = models.CharField(max_length=100, null=True, blank=True)
    tempat_lahir = models.CharField(max_length=100, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    ipk_terakhir = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nim} - {self.nama_lengkap}"
