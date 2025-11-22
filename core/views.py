from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'mahasiswa':
        return redirect('student_dashboard')
    else:
        return render(request, 'core/dashboard.html') # Fallback

@login_required
def student_dashboard(request):
    return render(request, 'core/student_dashboard.html')

from accounts.models import Mahasiswa
from recommender.models import DatasetSkripsi, TranskripUpload, RekomendasiLog

@login_required
def admin_dashboard(request):
    context = {
        'total_students': Mahasiswa.objects.count(),
        'total_topics': DatasetSkripsi.objects.count(),
        'total_uploads': TranskripUpload.objects.count(),
        'total_recommendations': RekomendasiLog.objects.count(),
    }
    return render(request, 'core/admin_dashboard.html', context)
