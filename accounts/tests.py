from django.test import TestCase
from django.urls import reverse

from .models import PatientProfile, TherapistProfile, User


class RegistrationTests(TestCase):
    def _post(self, **overrides):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "a-very-strong-passw0rd",
            "password_confirm": "a-very-strong-passw0rd",
            "role": "PATIENT",
        }
        data.update(overrides)
        return self.client.post(reverse("accounts:register"), data)

    def test_valid_registration_creates_patient_profile_and_logs_in(self):
        response = self._post()

        user = User.objects.get(username="newuser")
        self.assertEqual(user.role, "PATIENT")
        self.assertTrue(PatientProfile.objects.filter(user=user).exists())
        self.assertTrue(user.check_password("a-very-strong-passw0rd"))
        self.assertRedirects(response, reverse("appointment_list"))

    def test_valid_registration_creates_therapist_profile(self):
        self._post(username="newtherapist", email="therapist@example.com", role="THERAPIST")

        user = User.objects.get(username="newtherapist")
        self.assertEqual(user.role, "THERAPIST")
        self.assertTrue(TherapistProfile.objects.filter(user=user).exists())

    def test_weak_password_is_rejected(self):
        self._post(password="12345678", password_confirm="12345678")

        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_mismatched_passwords_are_rejected(self):
        self._post(password_confirm="something-else")

        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(username="newuser", password="x", role="PATIENT")

        self._post()

        self.assertEqual(User.objects.filter(username="newuser").count(), 1)

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            username="someoneelse", password="x", email="newuser@example.com", role="PATIENT"
        )

        self._post()

        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_invalid_role_is_rejected(self):
        response = self._post(role="ADMIN")

        self.assertFalse(User.objects.filter(username="newuser").exists())
        self.assertEqual(response.status_code, 200)


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="patient1", password="a-very-strong-passw0rd", role="PATIENT"
        )
        PatientProfile.objects.create(user=self.user)

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "patient1",
            "password": "a-very-strong-passw0rd",
        })

        self.assertRedirects(response, reverse("appointment_list"))

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "patient1",
            "password": "wrong-password",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username="patient1", password="a-very-strong-passw0rd")
        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("accounts:login"))
