from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Mahasiswa

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ('nim', 'nama_lengkap', 'program_studi', 'ipk_terakhir')
    search_fields = ('nim', 'nama_lengkap')
