from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_transcript, name='upload_transcript'),
    path('results/', views.recommendation_results, name='recommendation_results'),
    path('thesis/<int:pk>/', views.thesis_detail, name='thesis_detail'),
]
