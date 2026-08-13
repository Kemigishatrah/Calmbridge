from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from accounts.models import PatientProfile, TherapistProfile, User

from .models import Appointment, AvailabilitySlot, TherapistAssignment


class AppointmentsTestCase(TestCase):
    def setUp(self):
        self.therapist_user = User.objects.create_user(
            username="therapist1", password="pw", role="THERAPIST"
        )
        self.therapist = TherapistProfile.objects.create(
            user=self.therapist_user, specialization="CBT", is_verified=True
        )

        self.other_therapist_user = User.objects.create_user(
            username="therapist2", password="pw", role="THERAPIST"
        )
        self.other_therapist = TherapistProfile.objects.create(
            user=self.other_therapist_user, specialization="DBT", is_verified=True
        )

        self.patient_user = User.objects.create_user(
            username="patient1", password="pw", role="PATIENT"
        )
        self.patient = PatientProfile.objects.create(user=self.patient_user)

        self.other_patient_user = User.objects.create_user(
            username="patient2", password="pw", role="PATIENT"
        )
        self.other_patient = PatientProfile.objects.create(user=self.other_patient_user)

        self.admin_user = User.objects.create_user(
            username="admin1", password="pw", role="PATIENT", is_staff=True
        )

        self.assignment = TherapistAssignment.objects.create(
            patient=self.patient, therapist=self.therapist, is_active=True
        )

        self.slot = AvailabilitySlot.objects.create(
            therapist=self.therapist,
            date=date.today() + timedelta(days=1),
            start_time="10:00",
            end_time="11:00",
        )


class AccessControlTests(AppointmentsTestCase):
    def test_appointment_list_requires_login(self):
        response = self.client.get(reverse("appointment_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_manage_availability_blocks_patients(self):
        self.client.login(username="patient1", password="pw")
        response = self.client.get(reverse("manage_availability"))
        self.assertRedirects(response, reverse("appointment_list"))

    def test_assign_therapist_blocks_non_staff(self):
        self.client.login(username="therapist1", password="pw")
        response = self.client.get(reverse("assign_therapist"))
        self.assertNotEqual(response.status_code, 200)

    def test_assign_therapist_allows_staff(self):
        self.client.login(username="admin1", password="pw")
        response = self.client.get(reverse("assign_therapist"))
        self.assertEqual(response.status_code, 200)

    def test_available_sessions_blocks_therapists(self):
        self.client.login(username="therapist1", password="pw")
        response = self.client.get(reverse("available_sessions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "appointments/not_allowed.html")

    def test_session_notes_requires_login(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            therapist=self.therapist,
            date=self.slot.date,
            start_time=self.slot.start_time,
            end_time=self.slot.end_time,
        )
        response = self.client.get(
            reverse("session_notes", args=[appointment.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_session_notes_blocks_non_owning_therapist(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            therapist=self.therapist,
            date=self.slot.date,
            start_time=self.slot.start_time,
            end_time=self.slot.end_time,
        )
        self.client.login(username="therapist2", password="pw")
        response = self.client.get(
            reverse("session_notes", args=[appointment.id])
        )
        self.assertTemplateUsed(response, "appointments/not_allowed.html")

    def test_appointment_messages_blocks_unrelated_users(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            therapist=self.therapist,
            date=self.slot.date,
            start_time=self.slot.start_time,
            end_time=self.slot.end_time,
        )
        self.client.login(username="patient2", password="pw")
        response = self.client.get(
            reverse("appointment_messages", args=[appointment.id])
        )
        self.assertTemplateUsed(response, "appointments/not_allowed.html")


class AvailabilityFormTests(AppointmentsTestCase):
    def test_therapist_can_add_availability(self):
        self.client.login(username="therapist1", password="pw")
        response = self.client.post(reverse("manage_availability"), {
            "date": (date.today() + timedelta(days=2)).isoformat(),
            "start_time": "09:00",
            "end_time": "10:00",
        })
        self.assertRedirects(response, reverse("manage_availability"))
        self.assertTrue(
            AvailabilitySlot.objects.filter(
                therapist=self.therapist, start_time="09:00"
            ).exists()
        )

    def test_end_time_before_start_time_is_rejected(self):
        self.client.login(username="therapist1", password="pw")
        self.client.post(reverse("manage_availability"), {
            "date": (date.today() + timedelta(days=2)).isoformat(),
            "start_time": "13:00",
            "end_time": "12:00",
        })
        self.assertFalse(
            AvailabilitySlot.objects.filter(start_time="13:00").exists()
        )

    def test_past_date_is_rejected(self):
        self.client.login(username="therapist1", password="pw")
        self.client.post(reverse("manage_availability"), {
            "date": (date.today() - timedelta(days=1)).isoformat(),
            "start_time": "09:00",
            "end_time": "10:00",
        })
        self.assertFalse(
            AvailabilitySlot.objects.filter(start_time="09:00").exists()
        )


class BookingTests(AppointmentsTestCase):
    def test_patient_can_book_available_slot(self):
        self.client.login(username="patient1", password="pw")
        response = self.client.post(reverse("book_session", args=[self.slot.id]))

        self.assertEqual(response.status_code, 200)
        self.slot.refresh_from_db()
        self.assertFalse(self.slot.is_active)
        self.assertTrue(
            Appointment.objects.filter(patient=self.patient, therapist=self.therapist).exists()
        )

    def test_double_booking_the_same_slot_is_prevented(self):
        self.client.login(username="patient1", password="pw")
        self.client.post(reverse("book_session", args=[self.slot.id]))

        # A second booking attempt against the now-inactive slot must not
        # create a second appointment.
        second_response = self.client.post(reverse("book_session", args=[self.slot.id]))

        self.assertRedirects(second_response, reverse("available_sessions"))
        self.assertEqual(
            Appointment.objects.filter(therapist=self.therapist, patient=self.patient).count(), 1
        )

    def test_patient_cannot_book_slot_of_unassigned_therapist(self):
        other_slot = AvailabilitySlot.objects.create(
            therapist=self.other_therapist,
            date=date.today() + timedelta(days=1),
            start_time="14:00",
            end_time="15:00",
        )
        self.client.login(username="patient1", password="pw")
        response = self.client.post(reverse("book_session", args=[other_slot.id]))

        self.assertTemplateUsed(response, "appointments/not_allowed.html")
        other_slot.refresh_from_db()
        self.assertTrue(other_slot.is_active)
