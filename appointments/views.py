from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Appointment, AvailabilitySlot, SessionNote, TherapistAssignment,Message
from accounts.models import PatientProfile, TherapistProfile

@login_required
def appointment_list(request):
    user = request.user

    if user.role == "THERAPIST":
        appointments = Appointment.objects.filter(
            therapist=user.therapistprofile
        )

    elif user.role == "PATIENT":
        patient, _ = PatientProfile.objects.get_or_create(user=user)
        appointments = Appointment.objects.filter(patient=patient)

    else:
        # Admin or any other role
        appointments = Appointment.objects.none()

    return render(
        request,
        "appointments/list.html",
        {"appointments": appointments}
    )



@login_required
def appointment_detail(request, appointment_id):
    user = request.user

    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return redirect('appointments:appointment_list')

    # Ensure the user has permission to view this appointment
    if user.role == 'THERAPIST' and appointment.therapist.user != user:
        return redirect('appointments:appointment_list')
    elif user.role == 'PATIENT' and appointment.patient.user != user:
        return redirect('appointments:appointment_list')

    return render(request, 'appointments/detail.html', {
        'appointment': appointment
    })

@login_required
def manage_availability(request):
    user = request.user

    # Only therapists can access
    if user.role != "THERAPIST":
        return redirect("appointment_list")

    therapist = user.therapistprofile

    # Block unverified therapists
    if not therapist.is_verified:
        return render(request, "appointments/not_verified.html")

    if request.method == "POST":
        slot_date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        AvailabilitySlot.objects.create(
            therapist=therapist,
            date=slot_date,
            start_time=start_time,
            end_time=end_time
        )

        return redirect("manage_availability")

    slots = AvailabilitySlot.objects.filter(
        therapist=therapist,
        is_active=True
    )

    return render(
        request,
        "appointments/manage_availability.html",
        {"slots": slots}
    )

@staff_member_required
def assign_therapist(request):
    patients = PatientProfile.objects.all()
    therapists = TherapistProfile.objects.filter(is_verified=True)

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        therapist_id = request.POST.get("therapist")

        patient = PatientProfile.objects.get(id=patient_id)
        therapist = TherapistProfile.objects.get(id=therapist_id)

        TherapistAssignment.objects.update_or_create(
            patient=patient,
            defaults={"therapist": therapist, "is_active": True}
        )

        return redirect("assign_therapist")

    return render(
        request,
        "appointments/assign_therapist.html",
        {
            "patients": patients,
            "therapists": therapists
        }
    )
@login_required
def available_sessions(request):
    user = request.user

    # Only patients can access this page
    if user.role != "PATIENT":
        return render(request, "appointments/not_allowed.html")

    # Check therapist assignment
    assignment = TherapistAssignment.objects.filter(
        patient=user.patientprofile,
        is_active=True
    ).first()

    if not assignment:
        return render(
            request,
            "appointments/no_assignment.html"
        )

    therapist = assignment.therapist

    slots = AvailabilitySlot.objects.filter(
        therapist=therapist,
        is_active=True
    ).order_by("date", "start_time")

    return render(
        request,
        "appointments/available_sessions.html",
        {
            "therapist": therapist,
            "slots": slots
        }
    )
@login_required
def book_session(request, slot_id):
    user = request.user

    if user.role != "PATIENT":
        return render(request, "appointments/not_allowed.html")

    assignment = TherapistAssignment.objects.filter(
        patient=user.patientprofile,
        is_active=True
    ).first()

    if not assignment:
        return render(request, "appointments/no_assignment.html")

    slot = get_object_or_404(
        AvailabilitySlot,
        id=slot_id,
        is_active=True
    )

    # Ensure slot belongs to assigned therapist
    if slot.therapist != assignment.therapist:
        return render(request, "appointments/not_allowed.html")

    # Create appointment
    Appointment.objects.create(
        patient=user.patientprofile,
        therapist=slot.therapist,
        date=slot.date,
        start_time=slot.start_time,
        end_time=slot.end_time
    )

    # Lock the slot
    slot.is_active = False
    slot.save()

    return render(
        request,
        "appointments/booking_confirmed.html",
        {
            "therapist": slot.therapist,
            "date": slot.date,
            "start": slot.start_time,
            "end": slot.end_time,
        }
    )
@login_required
def appointment_messages(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    user = request.user

    # Access control
    if user not in [
        appointment.patient.user,
        appointment.therapist.user
    ] and not user.is_staff:
        return render(request, "appointments/not_allowed.html")

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(
                appointment=appointment,
                sender=user,
                content=content
            )
            return redirect("appointment_messages", appointment_id=appointment.id)

    messages = appointment.messages.order_by("created_at")

    return render(
        request,
        "appointments/messages.html",
        {
            "appointment": appointment,
            "messages": messages
        }
    )
login_required
def session_notes(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    user = request.user

    # Therapist-only (admin read-only handled later)
    if user.role != "THERAPIST":
        return render(request, "appointments/not_allowed.html")

    therapist = appointment.therapist

    # Ensure therapist owns this appointment
    if therapist.user != user:
        return render(request, "appointments/not_allowed.html")

    note, created = SessionNote.objects.get_or_create(
        appointment=appointment,
        therapist=therapist
    )

    if request.method == "POST":
        note.notes = request.POST.get("notes")
        note.save()
        return redirect("session_notes", appointment_id=appointment.id)

    return render(
        request,
        "appointments/session_notes.html",
        {
            "appointment": appointment,
            "note": note
        }
    )