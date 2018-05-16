from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from datetime import datetime
from django import forms
from django.db.models.signals import post_save

class Program(models.Model):
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=600, null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField(max_length=600, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    picture = models.ImageField(null=True, blank=True, default='no-img.png')
    website = models.URLField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=100, null=True)
    course = models.ManyToManyField(Course, related_name='course')


    def get_website(self):
        if self.website[0:4] != 'http':
            return 'http://' + self.website
        else:
            return self.website

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        student = Student.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class UploadForm(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField()


class Upload(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
    upload_time = models.DateTimeField(default=datetime.now)

    def get_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext)-1]

        if ext == 'doc' or ext == 'docx':
            return 'word'
        elif ext == 'pdf':
            return 'pdf'
        elif ext == 'xls' or ext == 'xlsx':
            return 'excel'
        elif ext == 'ppt' or ext == 'pptx':
            return 'powerpoint'
        elif ext == 'zip' or ext == 'rar' or ext == '7zip':
            return 'archive'

    def __str__(self):
        return str(self.file)[6:]
