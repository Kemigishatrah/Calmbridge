from django import forms
from django.contrib.auth.models import User
from .models import TherapistProfile, PatientProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class TherapistSignUpForm(forms.ModelForm):
    specialization = forms.CharField(max_length=100)
    license_number = forms.CharField(max_length=50)
    years_experience = forms.IntegerField(min_value=0)

    class Meta:
        model = User
        fields = ("username", "email", "password")
        widgets = {
            'password': forms.PasswordInput(),
        }

class PatientSignUpForm(forms.ModelForm):
    intake_summary = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ("username", "email", "password")
        widgets = {
            'password': forms.PasswordInput(),
        }
