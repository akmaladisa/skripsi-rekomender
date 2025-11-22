from django import forms
from .models import TranskripUpload

class TranskripUploadForm(forms.ModelForm):
    class Meta:
        model = TranskripUpload
        fields = ['file_path']
        widgets = {
            'file_path': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }
