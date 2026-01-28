from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User, TherapistProfile, PatientProfile


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("appointment_list")

    # IMPORTANT: correct template path
    return render(request, "accounts/login.html", {"form": form})

from django.contrib import messages
from django.db import IntegrityError


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Basic validation
        if not username or not password or not role:
            messages.error(request, "All fields are required.")
            return redirect("accounts:register")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "This username is already taken. Please choose another one."
            )
            return redirect("accounts:register")

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                role=role
            )
        except IntegrityError:
            messages.error(
                request,
                "Something went wrong. Please try again."
            )
            return redirect("accounts:register")

        # Create profile based on role
        if role == "THERAPIST":
            TherapistProfile.objects.create(
                user=user,
                specialization="General"
            )
        else:
            PatientProfile.objects.create(user=user)

        login(request, user)
        return redirect("appointment_list")

    return render(request, "accounts/register.html")



def logout_view(request):
    logout(request)
    return redirect("accounts:login")
