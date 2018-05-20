from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import redirect
from .models import Course, Program, User, Upload, Student
from django.contrib.auth.models import User, Group
from elearning import settings
from django.db.models import Sum
from .forms import UploadFormFile, UpdateProfile, SelectTeachersForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404


def programs_view(request):
    programs = Program.objects.all()
    return render (
        request,
        'programs_list.html',
        {'programs': programs},
    )


def program_detail(request, pk):
    program = Program.objects.get(pk=pk)
    courses = Course.objects.filter(program_id=pk)
    credits = Course.objects.aggregate(Sum('credits'))
    return render(
        request,
        'program_single.html',
        {'program': program, 'courses': courses, 'credits': credits},
    )


def students_view(request):
    students = Student.objects.all()
    programs = Program.objects.all()

    if request.method == 'GET':
        p = request.GET.get('program', '')
        name = request.GET.get('name', '')
        email = request.GET.get('email', '')

        if p != '':
            students = Student.objects.filter(program=p, first_name__contains=name, email__contains=email)
        else:
            students = Student.objects.filter(first_name__contains=name, email__contains=email)

    return render(
        request,
        'students_list.html',
        {'students': students, 'programs': programs, 'media_url': settings.MEDIA_ROOT},
    )


def student_detail(request, pk):
    student = Student.objects.get(pk=pk)

    return render(
        request, 'student_profile.html', {'student': student},
    )


def course_detail(request, pk):
    course = Course.objects.get(pk = pk)
    files = Upload.objects.filter(course_id = pk)
    # group = Group.objects.get(name='Teacher')
    # users = group.user_set.all()
    users = User.objects.all()

    return render(
        request, 'course_single.html', {'usrs': users, 'course': course, 'files': files, 'media_url': settings.MEDIA_ROOT},
    )


def course_add(request):
    pass


def handle_file_upload(request, course_id):
    course = Course.objects.get(pk = course_id)
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES, {'course': course})
        if form.is_valid():
            form.save()
            return redirect('/programs/course/' + str(course_id))
    else:
        form = UploadFormFile()
    return render(
        request, 'upload_file_form.html', {'form': form, 'course': course},
    )


def user_add(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uid = Student.objects.latest('pk').pk
            return redirect('user_edit', pk=uid)
    else:
        form = UserCreationForm()
    return render(
        request, 'user_add.html', {'form': form},
    )


def user_edit(request, pk):
    user = Student.objects.get(pk=pk)

    instance = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = UpdateProfile(instance=instance)

    return render(
        request, 'user_profile_edit.html', {'form': form, 'user': user},
    )

def select_teacher(request, course_id):

    instance = get_object_or_404(Student, pk=1)
    if request.method == 'POST':
        form = SelectTeachersForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('programs')
    else:
        form = SelectTeachersForm(instance=instance)
    return render (
        request, 'select_teacher.html', {'form': form},
    )
