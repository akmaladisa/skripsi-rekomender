import os
import django
import sys

# Setup Django environment
sys.path.append('/home/akmal/kuliah/semester5/tugas_ai')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thesis_recommender.settings')
django.setup()

from recommender.utils import parse_transcript
from recommender.models import TranskripUpload, Mahasiswa
from accounts.models import User

def test_real_pdf():
    print("--- Testing Real PDF Parsing ---")
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='test_student')
    mahasiswa, _ = Mahasiswa.objects.get_or_create(nim='12345678', user=user)
    
    # Create dummy upload instance
    upload = TranskripUpload.objects.create(
        mahasiswa=mahasiswa,
        file_path='Transkrip-nilai.pdf' # This path is relative to MEDIA_ROOT usually, but for utils it takes absolute path
    )
    
    pdf_path = '/home/akmal/kuliah/semester5/tugas_ai/Transkrip-nilai.pdf'
    
    try:
        count = parse_transcript(pdf_path, upload)
        print(f"Successfully extracted {count} courses.")
        
        if count > 0:
            print("Sample extracted courses:")
            for detail in upload.detail_nilai.all()[:5]:
                print(f"- {detail.nama_mk} (Grade: {detail.nilai_huruf}, SKS: {detail.sks})")
        else:
            print("FAILED: No courses extracted.")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    test_real_pdf()
