from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset-password/<str:token>/', views.reset_password_view, name='reset-password'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit-profile'),

    path('admin-page/', views.admin_page, name='admin-page'),
    path('teacher-page/', views.teacher_page, name='teacher-page'),
    path('student-page/', views.student_page, name='student-page'),
]