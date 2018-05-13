from django.urls import include, path
from . import views

urlpatterns = [
    path('students/', views.students_view, name='students'),
    path('student/<int:pk>', views.student_detail, name='student_detail'),
    path('programs/', views.programs_view, name='programs'),
    path('course/add/', views.course_add, name='course_add'),
    # path('programs/<int:pk>', views.program_detail, name='programs_detail'),
    path('programs/course/<int:pk>', views.course_detail, name='course_detail'),
    path('program/<int:pk>', views.program_detail, name='program_single'),
]