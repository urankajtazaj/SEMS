from django import forms
from .models import Upload

class UploadFormFile(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('name', 'file', 'course', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})