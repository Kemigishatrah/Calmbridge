import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .models import PatientProfile, TherapistProfile

logger = logging.getLogger(__name__)


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("appointment_list")

    # IMPORTANT: correct template path
    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            user = form.save()
        except IntegrityError:
            logger.warning("Registration failed due to a database integrity error.")
            messages.error(request, "Something went wrong. Please try again.")
            return redirect("accounts:register")

        # Create profile based on role
        if user.role == "THERAPIST":
            TherapistProfile.objects.create(
                user=user,
                specialization="General"
            )
        else:
            PatientProfile.objects.create(user=user)

        login(request, user)
        return redirect("appointment_list")

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
