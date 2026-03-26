from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def roles_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Veuillez vous connecter.")
                return redirect('login')

            if getattr(request.user, 'role', None) in allowed_roles:
                return view_func(request, *args, **kwargs)

            messages.error(request, "Vous n'avez pas l'autorisation d'acceder a cette page.")
            return redirect('dashboard')

        return wrapper

    return decorator


def admin_required(view_func):
    return roles_required('admin')(view_func)


def teacher_required(view_func):
    return roles_required('teacher')(view_func)


def student_required(view_func):
    return roles_required('student')(view_func)
