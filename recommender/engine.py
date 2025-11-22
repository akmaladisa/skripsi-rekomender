import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import DatasetSkripsi, TranskripDetailNilai, RekomendasiLog

def generate_recommendations(mahasiswa):
    # 1. Get Student's High Scoring Courses (A, A-, B+, B)
    # Adjust grade filter as needed.
    good_grades = ['A', 'A-', 'B+', 'B']
    
    # Get latest upload
    latest_upload = mahasiswa.transkrip_uploads.last()
    if not latest_upload:
        return []
    
    courses = TranskripDetailNilai.objects.filter(
        upload=latest_upload,
        nilai_huruf__in=good_grades
    ).values_list('nama_mk', flat=True)
    
    if not courses:
        return []
    
    # Construct Query String
    student_profile_text = " ".join(courses)
    
    # 2. Get Knowledge Base
    dataset = DatasetSkripsi.objects.all()
    if not dataset.exists():
        return []
    
    data = list(dataset.values('id', 'judul_skripsi', 'abstrak', 'kategori_topik'))
    df = pd.DataFrame(data)
    
    # Combine text features for TF-IDF
    # We use Title + Abstract + Category as the document text
    df['combined_text'] = df['judul_skripsi'] + " " + df['abstrak'].fillna('') + " " + df['kategori_topik'].fillna('')
    
    # 3. TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english') # 'english' might not be best for Indonesian, but it's a start.
    # Ideally use Sastrawi or Indonesian stop words.
    
    tfidf_matrix = tfidf.fit_transform(df['combined_text'])
    query_vec = tfidf.transform([student_profile_text])
    
    # 4. Calculate Similarity
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # 5. Get Top N Recommendations
    top_n_indices = cosine_sim.argsort()[-5:][::-1] # Top 5
    
    recommendations = []
    for idx in top_n_indices:
        score = cosine_sim[idx]
        if score > 0.0: # Only relevant ones
            skripsi = dataset[int(idx)] # Use index to get object from queryset (careful with ordering)
            # Better: use df.iloc[idx]['id'] to fetch object
            skripsi_id = df.iloc[idx]['id']
            skripsi_obj = DatasetSkripsi.objects.get(id=skripsi_id)
            
            # Save log
            RekomendasiLog.objects.create(
                mahasiswa=mahasiswa,
                skripsi_ref=skripsi_obj,
                skor_kemiripan=score,
                alasan_rekomendasi=f"Based on courses: {student_profile_text[:50]}..."
            )
            
            recommendations.append({
                'skripsi': skripsi_obj,
                'score': round(score * 100, 2)
            })
            
    return recommendations
