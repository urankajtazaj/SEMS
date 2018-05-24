from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('students/', views.students_view, name='students'),
    path('profile/<int:pk>', views.student_detail, name='student_detail'),
    path('programs/', views.programs_view, name='programs'),
    path('course/add/', views.course_add, name='course_add'),
    # path('programs/<int:pk>', views.program_detail, name='programs_detail'),
    path('programs/course/<int:pk>', views.course_detail, name='course_detail'),
    path('program/<int:pk>', views.program_detail, name='program_single'),
    path('program/course/<int:course_id>/upload/', views.handle_file_upload, name='upload_file_view'),
    path('students/add/', views.user_add, name='user_add'),
    path('profile/edit/<int:pk>', views.user_edit, name='user_edit'),
    path('course/<int:course_id>/teacher/edit/', views.select_teacher, name='add_teacher'),
    path('ajax/filter_course/', views.filter_courses_view, name='filter_views'),
    path('post/<int:pk>', views.post_single, name='post_single'),
    path('post/add/', views.post_add, name='post_add'),
    path('course/<int:course_id>/grades/', views.grade_students, name='grade_students'),
    re_path(r'^$', views.home_view, name='home'),
]