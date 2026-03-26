from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import admin_required, student_required, teacher_required
from .models import CustomUser, PasswordResetRequest


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if role not in [CustomUser.ROLE_ADMIN, CustomUser.ROLE_TEACHER, CustomUser.ROLE_STUDENT]:
            messages.error(request, 'Please select a valid role.')
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.set_role(role)
        user.save()

        messages.success(request, 'Signup successful!')
        return redirect('login')

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(user.get_dashboard_url())

        messages.error(request, 'Invalid credentials.')

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def dashboard_view(request):
    return redirect(request.user.get_dashboard_url())


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email)
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent successfully.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No user found with this email.')

        return redirect('forgot-password')

    return render(request, 'authentication/forgot-password.html')


def reset_password_view(request, token):
    reset_request = get_object_or_404(PasswordResetRequest, token=token)

    if not reset_request.is_valid():
        messages.error(request, 'Reset token has expired.')
        return redirect('forgot-password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset-password', token=token)

        user = reset_request.user
        user.set_password(new_password)
        user.save()

        reset_request.delete()
        messages.success(request, 'Password reset successful.')
        return redirect('login')

    return render(request, 'authentication/reset_password.html')


@login_required
def profile_view(request):
    return render(request, 'authentication/profile.html')


@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')

        if CustomUser.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, 'This email is already used by another account.')
            return redirect('edit-profile')

        if CustomUser.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, 'This username is already used by another account.')
            return redirect('edit-profile')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'authentication/edit-profile.html')


@login_required
@admin_required
def admin_page(request):
    return render(request, 'home_auth/admin_page.html')


@login_required
@teacher_required
def teacher_page(request):
    return render(request, 'home_auth/teacher_page.html')


@login_required
@student_required
def student_page(request):
    return render(request, 'home_auth/student_page.html')
