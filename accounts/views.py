from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User, TherapistProfile, PatientProfile


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('appointment_list')

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role
        )

        if role == 'THERAPIST':
            TherapistProfile.objects.create(
                user=user,
                specialization='General'
            )
        else:
            PatientProfile.objects.create(user=user)

        login(request, user)
        return redirect('appointment_list')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')

