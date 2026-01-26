from django.contrib import admin
from .models import AvailabilitySlot, TherapistAssignment, Appointment

@admin.register(AvailabilitySlot)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("therapist", "date", "start_time", "end_time", "is_booked", "is_active")
    list_filter = ("therapist", "date", "is_booked")


@admin.register(TherapistAssignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "therapist", "assigned_at", "is_active")
    list_filter = ("is_active",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "therapist", "date", "start_time", "status")
    list_filter = ("status", "date")
