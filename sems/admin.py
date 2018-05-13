from django.contrib import admin
from .models import Student, Course, Program, Upload, State

class UploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'file')


admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Program)
admin.site.register(Upload, UploadAdmin)
admin.site.register(State)
