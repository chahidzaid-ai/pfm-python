# 🎓 Preskool - School Management System (Django)

## 📌 Project Overview

**Preskool / PFM Python** is a school management system built using **Django**.
It allows administrators, teachers, and students to manage academic data through role-based dashboards.

The system includes features like:

* User authentication & role-based access
* Student & teacher management
* Departments & subjects
* Timetable scheduling
* Exams & holidays
* Dashboard interface with sidebar navigation

---

## ⚙️ Technologies Used

* Python 3.x
* Django
* SQLite (default database)
* HTML / CSS (Django Templates)


---

## 👥 User Roles

### 🔑 Admin

* Full access to the system
* Manage students, teachers, departments, subjects
* Manage exams, holidays, timetable

### 👨‍🏫 Teacher

* View assigned subjects and timetable
* Access limited dashboard features

### 🎓 Student

* View timetable, exams, and academic info
* Limited access

---

## 📁 Project Structure

```
pfm python/
│
├── manage.py
├── db.sqlite3
│
├── school/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│
├── home_auth/       # Authentication & user roles
├── faculty/         # Teachers, departments, subjects
├── student/         # Students, timetable, holidays, exams
│
└── templates/       # HTML templates
    ├── dashboard/
    ├── students/
    ├── faculty/
```

---

## 🔐 Custom User Model

The project uses a custom user model with roles:

```python
is_admin = models.BooleanField(default=False)
is_teacher = models.BooleanField(default=False)
is_student = models.BooleanField(default=False)
```

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/preskool.git
cd preskool
```

### 2. Create virtual environment

```bash
python -m venv monenv
monenv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install django
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser

```bash
python manage.py createsuperuser
```

### 6. Run server

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

---

## 📊 Features

### ✅ Authentication

* Login / Logout
* Role-based redirection

### ✅ Dashboards

* Admin dashboard
* Teacher dashboard
* Student dashboard

### ✅ CRUD Modules

* Students
* Teachers
* Departments
* Subjects
* Holidays
* Exams
* Timetable

---

## 🧠 Key Concepts Used

* Django MVT Architecture
* Custom User Model
* Role-Based Access Control (RBAC)
* Django Templates & URL routing
* CRUD operations

---

## ⚠️ Important Notes

* Do **NOT** use `.html` in URLs
  Always use Django `{% url %}`

Example:

```html
<a href="{% url 'holiday_list' %}">Holidays</a>
```

---

## 📌 Future Improvements

* Add REST API (Django REST Framework)
* Improve UI/UX
* Add notifications system
* Add attendance tracking

---

## 👨‍💻 Author

**Zaid Chahid**

---
video link :

https://drive.google.com/file/d/1-Y3reFONDSrg0OtOIZmPQLOWPCcF_Vsf/view?usp=sharing

---
#Rapport technique
[Rapport_PFM_Python.docx](https://github.com/user-attachments/files/26413817/Rapport_PFM_Python.docx)


