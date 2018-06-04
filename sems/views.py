from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect
from .models import Course, Program, User, Upload, Student, New, Grade
from django.contrib.auth.models import User, Group
from elearning import settings
from django.db.models import Sum, Avg, Max, Min
from .forms import UploadFormFile, UpdateProfile, SelectTeachersForm, AddPostForm, GradeStudentsFormSet, CourseAddForm, ProgramForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.core.paginator import Paginator


def programs_view(request):
    programs = Program.objects.all()

    if request.user.is_authenticated:
        return render (
            request,
            'programs_list.html',
            {'programs': programs},
        )
    else:
        return redirect('login')


def program_add(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('programs')
    else:
        form = ProgramForm()

    return render (
        request, 'program_add.html', {'form': form},
    )


def program_delete(request, pk):
    program = Program.objects.get(pk=pk)
    program.delete()

    return redirect('programs')


def program_edit(request, pk):
    program = Program.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('programs')
    else:
        form = ProgramForm(instance=program)

    return render(
        request, 'program_add.html', {'form': form},
    )


def program_detail(request, pk):
    program = Program.objects.get(pk=pk)
    courses = Course.objects.filter(program_id=pk)
    credits = Course.objects.aggregate(Sum('credits'))

    if request.user.is_authenticated:
        return render(
            request,
            'program_single.html',
            {'program': program, 'courses': courses, 'credits': credits},
        )
    else: 
        return redirect('login')


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

    if request.user.is_authenticated:
        return render(
            request,
            'students_list.html',
            {'students': students, 'programs': programs, 'media_url': settings.MEDIA_ROOT},
        )
    else:
        return redirect('login')


def student_detail(request, pk):
    student = Student.objects.get(pk=pk)
    success = Grade.objects.filter(student=student.user).order_by('-grade')
    details = Grade.objects.filter(student=student.user, grade__gt=4).aggregate(Avg('grade'), Max('grade'), Min('grade'))

    if request.user.is_authenticated:
        return render(
            request, 'student_profile.html', {'student': student, 'success': success, 'details': details},
        )
    else:
        return redirect('login')


def course_detail(request, pk):
    course = Course.objects.get(pk = pk)
    files = Upload.objects.filter(course_id = pk)
    users = User.objects.filter(student__course_teacher__in=[course])
    grades = Grade.objects.filter(student_id=request.user.id, course_id=pk)
    teachers = Student.objects.filter(course_teacher__in=[course])

    if request.user.is_authenticated:
        return render(
            request, 'course_single.html', {'usrs': users, 'course': course, 'files': files, 'grades': grades, 'teachers': teachers, 'media_url': settings.MEDIA_ROOT},
        )
    else:
        return redirect('login')


def course_add(request):
    if request.method == 'POST':
        form = CourseAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('program_single', pk=request.POST.get('program'))
    else:
        form = CourseAddForm()

    if request.user.is_authenticated and request.user.is_superuser:
        return render (
            request, 'course_add.html', {'form': form},
        )
    else:
        return redirect('login')


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


def handle_file_edit(request, course_id, file_id):
    course = Course.objects.get(pk=course_id)
    instance = Upload.objects.get(pk=file_id)
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=course_id)
    else:
        form = UploadFormFile(instance=instance)

    return render (
        request, 'upload_file_form.html', {'form': form, 'course': course}
    )


# TODO Add this
def handle_file_delete(request, course_id, file_id):
    file = Upload.objects.get(pk=file_id)
    file.delete()

    return redirect('course_detail', pk=course_id)


def user_add(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uid = Student.objects.latest('pk').pk
            return redirect('user_edit', pk=uid)
    else:
        form = UserCreationForm()

    if request.user.is_authenticated and request.user.is_superuser:
        return render(
            request, 'user_add.html', {'form': form},
        )
    else:
        return redirect('login')


def user_edit(request, pk):
    student = Student.objects.get(pk=pk)

    instance = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, request.FILES, instance = instance)
        if form.is_valid():
            form.save(commit=False)

            courses = request.POST.getlist('course')

            for c in courses:
                grade = Grade()
                usr = User.objects.get(pk=request.POST.get('user'))
                crs = Course.objects.get(pk=c)
                if not Grade.objects.filter(course=crs, student=usr).exists():
                    grade.student = usr
                    grade.grade = 0
                    grade.course = crs
                    grade.save()

            existing_courses = list(Student.objects.values_list('course', flat=True).filter(pk=pk))
            
            for c in existing_courses:
                if str(c) not in courses:
                    Grade.objects.filter(student=User.objects.get(pk=request.POST.get('user')), course=c).delete()

            form.save()
            return redirect('students')
    else:
        form = UpdateProfile(instance=instance)

    return render(
        request, 'user_profile_edit.html', {'form': form, 'student': student},
    )


def select_teacher(request, course_id):
    students = Student.objects.all()
    curr_teachers = Student.objects.filter(course_teacher__in=[Course.objects.get(pk=course_id)])

    print(curr_teachers)

    if request.method == 'GET':
        first_name = request.GET.get('first_name', '')
        last_name = request.GET.get('last_name', '')
        students = Student.objects.filter(first_name__contains=first_name, last_name__contains=last_name).exclude(course_teacher__in=[Course.objects.get(pk=course_id)])

    paginator = Paginator(students, 15)

    page = request.GET.get('page')
    students = paginator.get_page(page)

    return render (
        request, 'select_teacher.html', {'students': students, 'course_id': course_id, 'teachers': curr_teachers},
    )



def confirm_select_teacher(request, course_id, student_id):
    student = Student.objects.get(pk=student_id)
    course = Course.objects.get(pk=course_id)

    student.course_teacher.add(course)
    student.save()

    return redirect('add_teacher', course_id=course_id)    



def confirm_delete_teacher(request, course_id, student_id):
    student = Student.objects.get(pk=student_id)
    course = Course.objects.get(pk=course_id)

    student.course_teacher.remove(course)
    student.save()

    return redirect('add_teacher', course_id=course_id)



# AJAX Call
def filter_courses_view(request):
    program = request.GET.get('program', None)
    course = Course.objects.filter(program=program).values('pk', 'name', )
    data = list(course)
    return JsonResponse(data, safe=False)


def home_view(request):
    uploads = Upload.objects.all().order_by('-upload_time')[:5]
    programs = Program.objects.all()
    users = User.objects.all().order_by('-last_login')[:5]
    news = New.objects.all().order_by('-create_date')[:3]

    if request.user.is_authenticated:
        return render (
            request, 'home.html', {'uploads': uploads, 'programs': programs, 'users': users, 'news': news},
        )
    else:
        return redirect('login')


def post_list(request):

    posts = New.objects.all().order_by('-create_date')
    paginator = Paginator(posts, 12)

    page = request.GET.get('page')
    post = paginator.get_page(page)

    return render(
        request, 'post_list.html', {'posts': post}, 
    )


def post_single(request, pk):
    post = New.objects.get(pk=pk)
    posts = New.objects.all().order_by('-create_date')[:10]
    uploads = Upload.objects.all().order_by('-upload_time')[:5]

    if request.user.is_authenticated:
        return render (
            request, 'post_single.html', {'post': post, 'posts': posts, 'uploads': uploads},
        )
    else:
        return redirect('login')

def post_add(request):

    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    if request.user.is_authenticated and request.user.is_superuser:
        return render (
            request, 'add_new_post.html', {'form': form},
        )
    else:
        return redirect('login')


def grade_students(request, course_id):
    course = Course.objects.get(pk=course_id)
    curr_grades = Grade.objects.filter(course=course)

    queryset = Grade.objects.filter(course=course)

    if request.method == 'POST':
        formset = GradeStudentsFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            return redirect('course_detail', pk=course_id)
        else:
            print(formset.errors)
    else:
        # queryset = Student.objects.filter(course=course)
        formset = GradeStudentsFormSet(queryset=queryset)

    return render (
        request, 'grade_students.html', {'formset': formset, 'course': course},
    )
