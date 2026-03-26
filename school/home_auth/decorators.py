from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        messages.error(request, "AccÃ¨s rÃ©servÃ© Ã  l'administrateur.")
        return redirect('dashboard')
    return wrapper


def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_teacher:
            return view_func(request, *args, **kwargs)
        messages.error(request, "AccÃ¨s rÃ©servÃ© Ã  l'enseignant.")
        return redirect('dashboard')
    return wrapper


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_student:
            return view_func(request, *args, **kwargs)
        messages.error(request, "AccÃ¨s rÃ©servÃ© Ã  l'Ã©tudiant.")
        return redirect('dashboard')
    return wrapper
