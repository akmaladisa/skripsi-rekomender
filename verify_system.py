import os
import django
import sys

# Setup Django environment
sys.path.append('/home/akmal/kuliah/semester5/tugas_ai')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thesis_recommender.settings')
django.setup()

from accounts.models import User, Mahasiswa
from recommender.models import DatasetSkripsi, TranskripUpload, TranskripDetailNilai
from recommender.engine import generate_recommendations

def verify():
    print("--- Starting Verification ---")
    
    # 1. Create User & Student
    user, created = User.objects.get_or_create(username='test_student', role='mahasiswa')
    if created:
        user.set_password('password123')
        user.save()
        print("User created.")
    
    mahasiswa, created = Mahasiswa.objects.get_or_create(
        nim='12345678',
        defaults={'user': user, 'nama_lengkap': 'Test Student'}
    )
    print(f"Student profile: {mahasiswa}")

    # 2. Create Dummy Transcript Upload
    upload = TranskripUpload.objects.create(
        mahasiswa=mahasiswa,
        file_path='dummy.pdf'
    )
    print("Dummy upload created.")

    # 3. Add Courses (Simulate Parsing)
    # Scenario: Student is good at Data Mining and AI
    courses = [
        ('Data Mining', 3, 'A'),
        ('Kecerdasan Buatan', 3, 'A'),
        ('Pemrograman Web', 3, 'B'),
        ('Jaringan Komputer', 3, 'C'), # Should be ignored
    ]
    
    for name, sks, grade in courses:
        TranskripDetailNilai.objects.create(
            upload=upload,
            nama_mk=name,
            sks=sks,
            nilai_huruf=grade
        )
    print(f"Added {len(courses)} courses to transcript.")

    # 4. Run Recommendation
    print("Generating recommendations...")
    recommendations = generate_recommendations(mahasiswa)
    
    print(f"\nFound {len(recommendations)} recommendations:")
    for item in recommendations:
        print(f"- {item['skripsi'].judul_skripsi} (Score: {item['score']}%)")
        print(f"  Category: {item['skripsi'].kategori_topik}")

    # Check if Data Mining/ML topics are recommended
    if len(recommendations) > 0:
        top_topic = recommendations[0]['skripsi'].kategori_topik
        if top_topic in ['Data Mining', 'Machine Learning']:
            print("\nSUCCESS: Recommendation logic works! Correctly identified interest in Data Mining/ML.")
        else:
            print(f"\nWARNING: Top recommendation category is {top_topic}, expected Data Mining or Machine Learning.")
    else:
        print("\nFAILURE: No recommendations found.")

if __name__ == '__main__':
    verify()
