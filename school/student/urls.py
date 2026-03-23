from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('students/<str:student_id>/', views.view_student, name='view_student'),
    path('edit/<str:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<str:student_id>/', views.delete_student, name='delete_student'),
    path('timetable/', views.timetable_list, name='timetable_list'),
    path('holidays/', views.holiday_list, name='holiday_list'),

    
    path('timetable/add/', views.add_timetable, name='add_timetable'),
    path('timetable/edit/<int:timetable_id>/', views.edit_timetable, name='edit_timetable'),
    path('timetable/delete/<int:timetable_id>/', views.delete_timetable, name='delete_timetable'),

    
]