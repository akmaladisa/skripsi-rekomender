from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TranskripUploadForm
from .utils import parse_transcript
from .engine import generate_recommendations
from .models import DatasetSkripsi

@login_required
def upload_transcript(request):
    if request.method == 'POST':
        form = TranskripUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.mahasiswa = request.user.mahasiswa_profile
            upload.save()
            
            # Parse PDF
            try:
                count = parse_transcript(upload.file_path.path, upload)
                messages.success(request, f'Transcript uploaded and {count} courses extracted successfully.')
                return redirect('recommendation_results') # Redirect to results directly
            except Exception as e:
                messages.error(request, f'Error parsing PDF: {str(e)}')
                upload.delete() # Cleanup
    else:
        form = TranskripUploadForm()
    
    return render(request, 'recommender/upload.html', {'form': form})

@login_required
def recommendation_results(request):
    mahasiswa = request.user.mahasiswa_profile
    recommendations = generate_recommendations(mahasiswa)
    
    context = {
        'recommendations': recommendations
    }
    return render(request, 'recommender/results.html', context)

@login_required
def thesis_detail(request, pk):
    skripsi = get_object_or_404(DatasetSkripsi, pk=pk)
    return render(request, 'recommender/thesis_detail.html', {'skripsi': skripsi})
