from django import forms
from .models.models1 import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
