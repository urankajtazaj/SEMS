from django.shortcuts import render
from django.http import HttpRequest
from .models import Student, Course, Program, State, Upload
from elearning import settings


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
    students = Student.objects.filter()
    return render(
        request,
        'program_single.html',
        {'program': program, 'courses': courses},
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
        request, 'student_detail.html', {'student': student},
    )


def course_detail(request, pk):
    course = Course.objects.get(pk = pk)
    files = Upload.objects.filter(course_id = pk)

    return render(
        request, 'course_single.html', {'course': course, 'files': files, 'media_url': settings.MEDIA_ROOT},
    )

def course_add(request):
    pass
