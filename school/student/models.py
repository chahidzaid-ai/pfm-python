from django.db import models


class Parent(models.Model):
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_mobile = models.CharField(max_length=15)
    father_email = models.EmailField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_mobile = models.CharField(max_length=15)
    mother_email = models.EmailField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()

    def __str__(self):
        return f"{self.father_name} & {self.mother_name}"


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    student_class = models.CharField(max_length=50)
    religion = models.CharField(max_length=50, blank=True, null=True, default='')
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    admission_number = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    student_image = models.ImageField(upload_to='students/', blank=True, null=True)
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Timetable(models.Model):
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    student_class = models.CharField(max_length=50)
    section = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    day = models.CharField(max_length=20, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.student_class} - {self.subject} - {self.day}"


class Exam(models.Model):
    title = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    exam_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.subject}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    mark = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.mark}"


class Holiday(models.Model):
    title = models.CharField(max_length=100)
    holiday_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.holiday_date}"