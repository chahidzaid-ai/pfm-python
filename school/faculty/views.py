from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'authentication/login.html')

@login_required
def dashboard(request):
    return render(request, 'students/student-dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'Home/index.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'students/student-dashboard.html')