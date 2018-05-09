from django.contrib import admin
from .models import Student, Course, Program, Upload, State

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Program)
admin.site.register(Upload)
admin.site.register(State)
