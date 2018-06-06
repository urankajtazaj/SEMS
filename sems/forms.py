from django import forms
from .models import Upload, Student, New, Grade, Course, Program
from django.contrib.auth.models import User
from django.forms import CharField

# Upload files to specific course
class UploadFormFile(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('name', 'file', 'course', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})


# Add/Edit User profile
class UpdateProfile(forms.ModelForm):

    # course = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.CheckboxSelectMultiple)

    is_super = forms.BooleanField(required=False)

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'course', 'program', 'country', 'city', 'picture', 'website', 'user', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'hidden': True})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['program'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'City'})
        self.fields['website'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Website'})
        self.fields['course'].widget.attrs.update({'class': 'full-width'})


# Sign up form
class SignUpForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())
    

    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.username)
            raise forms.ValidationError('User already exists')
        except User.DoesNotExist:
            return self.username


    def clean_password(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')

        if pw1 and pw2 and pw1 == pw2:
            return pw1
        raise forms.ValidationError("Password doesn't match")


# Select teachers for a specific course
class SelectTeachersForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = forms.ModelMultipleChoiceField(queryset=Student.objects.all())
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})


class AddPostForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ('title', 'content', 'picture', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['picture'].widget.attrs.update({'class': 'form-control'})


class GradeStudentsForm(forms.ModelForm):

    # student = forms.ChoiceField(choices=[(s.pk, s.first_name + ' ' + s.last_name) for s in Student.objects.all()])

    class Meta:
        model = Grade
        fields = ('student', 'grade', )

    def __init__(self, *args, **kwargs):
        super(GradeStudentsForm, self).__init__(*args, **kwargs)
        # if course:
            # self.fields['student'].widget = forms.ChoiceField(choices=[(s.pk, s.first_name) for s in Student.objects.all()])
        # self.fields['student'].widget = forms.ChoiceField(queryset=Student.objects.values_list('pk', 'first_name'))
        self.fields['student'].widget.attrs.update({'class': 'form-control'})
        self.fields['grade'].widget.attrs.update({'class': 'form-control'})




class DateInput(forms.DateInput):
    input_type = 'date'

class CourseAddForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['program'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['credits'].widget.attrs.update({'class': 'form-control'})


class ProgramForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
