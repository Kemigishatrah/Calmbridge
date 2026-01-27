from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('THERAPIST', 'Therapist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class TherapistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #professional details
    qualifications = models.CharField(max_length=255, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
#clinical specialization
    specialization = models.CharField(max_length=100, blank=True)
    focus_areas = models.TextField(max_length=255, blank=True)
    #accessibility options
    language_proficiencies = models.CharField(max_length=100, blank=True)
    offers_teletherapy = models.BooleanField(default=False, blank=True)
    location = models.CharField(max_length=100, blank=True)
#practice details
    availability = models.CharField(max_length=100, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='therapist_profiles/', null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True)


    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

