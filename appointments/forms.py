from datetime import date

from django import forms

from accounts.models import PatientProfile, TherapistProfile

from .models import AvailabilitySlot


class AvailabilitySlotForm(forms.ModelForm):
    class Meta:
        model = AvailabilitySlot
        fields = ['date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        slot_date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if slot_date and slot_date < date.today():
            self.add_error('date', 'Availability cannot be added for a past date.')

        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', 'End time must be after start time.')

        return cleaned_data


class AssignTherapistForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=PatientProfile.objects.all())
    therapist = forms.ModelChoiceField(
        queryset=TherapistProfile.objects.filter(is_verified=True)
    )
