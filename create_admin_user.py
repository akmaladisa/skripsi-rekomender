import os
import django
import sys

# Setup Django environment
sys.path.append('/home/akmal/kuliah/semester5/tugas_ai')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thesis_recommender.settings')
django.setup()

from accounts.models import User

def create_admin():
    username = 'admin_dummy'
    password = 'adminpassword123'
    email = 'admin@example.com'
    
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists.")
        return

    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='admin'
    )
    print(f"Successfully created admin user:")
    print(f"Username: {username}")
    print(f"Password: {password}")

if __name__ == '__main__':
    create_admin()
