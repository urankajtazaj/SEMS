from django import forms
from .models import Upload

class UploadFormFile(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('name', 'file', 'course', )