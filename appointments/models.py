from django.db import models
from accounts.models import TherapistProfile, PatientProfile


class Appointment(models.Model):
    STATUS_CHOICES = (
        ("SCHEDULED", "Scheduled"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    therapist = models.ForeignKey(TherapistProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SCHEDULED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.patient} with {self.therapist} on {self.date}"


class AvailabilitySlot(models.Model):
    therapist = models.ForeignKey(
        TherapistProfile,
        on_delete=models.CASCADE,
        related_name="availability_slots"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    is_booked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "start_time"]
        unique_together = ("therapist", "date", "start_time")

    def __str__(self):
        return f"{self.therapist} | {self.date} {self.start_time}-{self.end_time}"


class TherapistAssignment(models.Model):
    patient = models.OneToOneField(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="assignment"
    )
    therapist = models.ForeignKey(
        TherapistProfile,
        on_delete=models.CASCADE,
        related_name="assigned_patients"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patient} → {self.therapist}"
    from django.db import models


class Message(models.Model):
    appointment = models.ForeignKey(
        "Appointment",
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username}"

class SessionNote(models.Model):
    appointment = models.OneToOneField(
        "Appointment",
        on_delete=models.CASCADE,
        related_name="session_note"
    )
    therapist = models.ForeignKey(
        "accounts.TherapistProfile",
        on_delete=models.CASCADE
    )
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session notes for appointment {self.appointment.id}"
