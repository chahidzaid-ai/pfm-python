from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Department, Teacher
from django.db import models

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


# ---------------- DEPARTMENTS ----------------

@login_required
def department_list(request):
    departments = Department.objects.all().order_by('name')
    return render(request, 'departments/department-list.html', {'departments': departments})


@login_required
def add_department(request):
    teachers = Teacher.objects.all().order_by('first_name', 'last_name')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        teacher_ids = request.POST.getlist('teachers')

        if Department.objects.filter(name=name).exists():
            messages.error(request, 'Department already exists.')
            return redirect('add_department')

        department = Department.objects.create(
            name=name,
            description=description
        )

        if teacher_ids:
            Teacher.objects.filter(id__in=teacher_ids).update(department=department)

        messages.success(request, 'Department added successfully.')
        return redirect('department_list')

    return render(request, 'departments/add-department.html', {'teachers': teachers})


@login_required
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    teachers = Teacher.objects.all().order_by('first_name', 'last_name')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        teacher_ids = request.POST.getlist('teachers')

        if Department.objects.exclude(id=department.id).filter(name=name).exists():
            messages.error(request, 'Another department with this name already exists.')
            return redirect('edit_department', department_id=department.id)

        department.name = name
        department.description = description
        department.save()

        Teacher.objects.filter(department=department).update(department=None)

        if teacher_ids:
            Teacher.objects.filter(id__in=teacher_ids).update(department=department)

        messages.success(request, 'Department updated successfully.')
        return redirect('department_list')

    selected_teacher_ids = list(
        Teacher.objects.filter(department=department).values_list('id', flat=True)
    )

    return render(request, 'departments/edit-department.html', {
        'department': department,
        'teachers': teachers,
        'selected_teacher_ids': selected_teacher_ids,
    })


@login_required
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        Teacher.objects.filter(department=department).update(department=None)
        department.delete()
        messages.success(request, 'Department deleted successfully.')

    return redirect('department_list')


# ---------------- TEACHERS ----------------

@login_required
def teacher_list(request):
    query = request.GET.get('q', '')
    department_id = request.GET.get('department', '')

    teachers = Teacher.objects.select_related('department').all().order_by('first_name', 'last_name')
    departments = Department.objects.all().order_by('name')

    if query:
        teachers = teachers.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(email__icontains=query) |
            models.Q(teacher_id__icontains=query)
        )

    if department_id:
        teachers = teachers.filter(department_id=department_id)

    return render(request, 'teachers/teacher-list.html', {
        'teachers': teachers,
        'departments': departments,
        'query': query,
        'selected_department': department_id,
    })


@login_required
def add_teacher(request):
    departments = Department.objects.all().order_by('name')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        teacher_id = request.POST.get('teacher_id')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        seniority = request.POST.get('seniority') or 1
        address = request.POST.get('address', '')
        department_id = request.POST.get('department')

        if Teacher.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('add_teacher')

        if Teacher.objects.filter(teacher_id=teacher_id).exists():
            messages.error(request, 'Teacher ID already exists.')
            return redirect('add_teacher')

        department = None
        if department_id:
            department = Department.objects.filter(id=department_id).first()

        Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            teacher_id=teacher_id,
            email=email,
            phone=phone,
            seniority=seniority,
            address=address,
            department=department
        )

        messages.success(request, 'Teacher added successfully.')
        return redirect('teacher_list')

    return render(request, 'teachers/add-teacher.html', {'departments': departments})


@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    departments = Department.objects.all().order_by('name')

    if request.method == 'POST':
        email = request.POST.get('email')
        teacher_code = request.POST.get('teacher_id')
        department_id = request.POST.get('department')

        if Teacher.objects.exclude(id=teacher.id).filter(email=email).exists():
            messages.error(request, 'Another teacher already uses this email.')
            return redirect('edit_teacher', teacher_id=teacher.id)

        if Teacher.objects.exclude(id=teacher.id).filter(teacher_id=teacher_code).exists():
            messages.error(request, 'Another teacher already uses this Teacher ID.')
            return redirect('edit_teacher', teacher_id=teacher.id)

        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.teacher_id = teacher_code
        teacher.email = email
        teacher.phone = request.POST.get('phone')
        teacher.seniority = request.POST.get('seniority') or 1
        teacher.address = request.POST.get('address', '')
        teacher.department = Department.objects.filter(id=department_id).first() if department_id else None
        teacher.save()

        messages.success(request, 'Teacher updated successfully.')
        return redirect('teacher_list')

    return render(request, 'teachers/edit-teacher.html', {
        'teacher': teacher,
        'departments': departments
    })


@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully.')

    return redirect('teacher_list')