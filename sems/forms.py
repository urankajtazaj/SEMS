from django import forms
from .models import Upload

class UploadForm(forms.Form):
    title = forms.CharField(max_length=200)
    file = forms.FileField()

    def save(self):
        upload = Upload()
        upload.file = self.file
        upload.name = self.title
        upload.save()
