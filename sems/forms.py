from django import forms
from .models import UploadForm

class UploadFormFile(forms.ModelForm):
    class Meta:
        model = UploadForm
        fields = ('title', 'file', )