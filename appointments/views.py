from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm


@login_required
def appointment_list(request):
    user = request.user

    if user.role == 'THERAPIST':
        appointments = Appointment.objects.filter(
            therapist=user.therapistprofile
        )
    else:
        appointments = Appointment.objects.filter(
            patient=user.patientprofile
        )

    return render(request, 'appointments/list.html', {
        'appointments': appointments
    })


@login_required
def create_appointment(request):
    user = request.user

    if user.role != 'THERAPIST':
        return redirect('appointment_list')

    therapist_profile = user.therapistprofile

    if not therapist_profile.is_verified:
        return render(request, 'appointments/not_verified.html')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.therapist = therapist_profile
            appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/create.html', {'form': form})

