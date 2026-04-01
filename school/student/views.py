from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from home_auth.models import CustomUser
from .models import Student, Parent, Timetable, Exam, Grade, Holiday


def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    return render(request, 'students/students.html', {'student_list': student_list})


def add_student(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion', '')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists.')
            return redirect('add_student')

        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )

        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_class=student_class,
            religion=religion,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent
        )

        messages.success(request, 'Student added successfully.')
        return redirect('student_list')

    return render(request, 'students/add-student.html')


def view_student(request, student_id):
    student = get_object_or_404(Student.objects.select_related('parent'), student_id=student_id)
    return render(request, 'students/student-details.html', {'student': student})


def edit_student(request, student_id):
    student = get_object_or_404(Student.objects.select_related('parent'), student_id=student_id)
    parent = student.parent

    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        student.religion = request.POST.get('religion')
        student.joining_date = request.POST.get('joining_date')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')

        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')

        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')

        parent.save()
        student.save()

        messages.success(request, 'Student updated successfully.')
        return redirect('student_list')

    return render(request, 'students/edit-student.html', {'student': student})


def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')

    return redirect('student_list')


def timetable_list(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    timetables = Timetable.objects.all().order_by('start_time', 'day')

    time_slots = []
    seen = set()

    for t in timetables:
        key = (t.start_time, t.end_time)
        if key not in seen:
            seen.add(key)
            time_slots.append(key)

    table_rows = []
    for start_time, end_time in time_slots:
        row = {
            'time': f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}",
            'cells': []
        }

        for day in days:
            entry = None
            for t in timetables:
                if t.day == day and t.start_time == start_time and t.end_time == end_time:
                    entry = t
                    break

            row['cells'].append(entry)

        table_rows.append(row)

    return render(request, 'students/timetable.html', {
        'days': days,
        'table_rows': table_rows,
    })


def add_timetable(request):
    if request.method == 'POST':
        Timetable.objects.create(
            student_class=request.POST.get('student_class'),
            section=request.POST.get('section'),
            subject=request.POST.get('subject'),
            teacher=request.POST.get('teacher'),
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
        )
        messages.success(request, 'Timetable added successfully.')
        return redirect('timetable_list')

    return render(request, 'students/add-timetable.html')


def edit_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id)

    if request.method == 'POST':
        timetable.student_class = request.POST.get('student_class')
        timetable.section = request.POST.get('section')
        timetable.subject = request.POST.get('subject')
        timetable.teacher = request.POST.get('teacher')
        timetable.day = request.POST.get('day')
        timetable.start_time = request.POST.get('start_time')
        timetable.end_time = request.POST.get('end_time')
        timetable.save()

        messages.success(request, 'Timetable updated successfully.')
        return redirect('timetable_list')

    return render(request, 'students/edit-timetable.html', {'timetable': timetable})


def delete_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id)

    if request.method == 'POST':
        timetable.delete()
        messages.success(request, 'Timetable deleted successfully.')

    return redirect('timetable_list')

def add_timetable(request):
    if request.method == 'POST':
        Timetable.objects.create(
            student_class=request.POST.get('student_class'),
            section=request.POST.get('section'),
            subject=request.POST.get('subject'),
            teacher=request.POST.get('teacher'),
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
        )
        messages.success(request, 'Timetable added successfully.')
        return redirect('timetable_list')

    return render(request, 'students/add-timetable.html')


def edit_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id)

    if request.method == 'POST':
        timetable.student_class = request.POST.get('student_class')
        timetable.section = request.POST.get('section')
        timetable.subject = request.POST.get('subject')
        timetable.teacher = request.POST.get('teacher')
        timetable.day = request.POST.get('day')
        timetable.start_time = request.POST.get('start_time')
        timetable.end_time = request.POST.get('end_time')
        timetable.save()

        messages.success(request, 'Timetable updated successfully.')
        return redirect('timetable_list')

    return render(request, 'students/edit-timetable.html', {'timetable': timetable})


def delete_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id)

    if request.method == 'POST':
        timetable.delete()
        messages.success(request, 'Timetable deleted successfully.')

    return redirect('timetable_list')


def holiday_list(request):
    holidays = Holiday.objects.all().order_by('holiday_date')
    return render(request, 'students/holidays.html', {'holidays': holidays})



def add_holiday(request):
    if request.method == 'POST':
        Holiday.objects.create(
            title=request.POST.get('title'),
            holiday_date=request.POST.get('holiday_date'),
            description=request.POST.get('description'),
        )
        messages.success(request, 'Holiday added successfully.')
        return redirect('holiday_list')

    return render(request, 'students/add-holiday.html')


def edit_holiday(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)

    if request.method == 'POST':
        holiday.title = request.POST.get('title')
        holiday.holiday_date = request.POST.get('holiday_date')
        holiday.description = request.POST.get('description')
        holiday.save()

        messages.success(request, 'Holiday updated successfully.')
        return redirect('holiday_list')

    return render(request, 'students/edit-holiday.html', {'holiday': holiday})


def delete_holiday(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)

    if request.method == 'POST':
        holiday.delete()
        messages.success(request, 'Holiday deleted successfully.')

    return redirect('holiday_list')

def exam_list(request):
    exams = Exam.objects.all().order_by('exam_date')
    return render(request, 'students/exam-list.html', {'exams': exams})


def add_exam(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        student_class = request.POST.get('student_class')
        subject = request.POST.get('subject')
        exam_date = request.POST.get('exam_date')

        Exam.objects.create(
            title=title,
            student_class=student_class,
            subject=subject,
            exam_date=exam_date
        )

        messages.success(request, 'Exam added successfully.')
        return redirect('exam_list')

    return render(request, 'students/add-exam.html')


def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        exam.title = request.POST.get('title')
        exam.student_class = request.POST.get('student_class')
        exam.subject = request.POST.get('subject')
        exam.exam_date = request.POST.get('exam_date')
        exam.save()

        messages.success(request, 'Exam updated successfully.')
        return redirect('exam_list')

    return render(request, 'students/edit-exam.html', {'exam': exam})


def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully.')

    return redirect('exam_list')  
  
def add_grade(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    students = CustomUser.objects.filter(is_student=True)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        marks = request.POST.get('marks')

        Grade.objects.create(
            exam=exam,
            student_id=student_id,
            marks=marks
        )

        messages.success(request, "Grade added successfully")
        return redirect('exam_list')

    return render(request, 'students/add-grade.html', {
        'exam': exam,
        'students': students
    })
