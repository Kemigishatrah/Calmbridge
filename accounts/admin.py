from django.contrib import admin
from .models import User, TherapistProfile, PatientProfile
# USER MODEL ADMINISTRATION
# Centralized management for all platform accounts (Patients, Therapists, Admins)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Optimization: Quick-view of account status and roles directly from the list view
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'is_superuser')
    
    # Filter: Enables admins to quickly segment users by role or account status
    list_filter = ('role', 'is_active')

# THERAPIST PROFILE ADMINISTRATION
# Critical for vetting and managing qualified healthcare providers
@admin.register(TherapistProfile)
class TherapistProfileAdmin(admin.ModelAdmin):
    # Visibility: 'is_verified' is displayed prominently to track provider vetting progress
    list_display = ('user', 'specialization', 'is_verified', 'years_of_experience', 'offers_teletherapy', 'hourly_rate', 'location', 'availability', 'language_proficiencies', 'qualifications', 'license_number', 'focus_areas', 'profile_picture', 'bio')
    
    # Filter for unverified therapists to perform credential checks
    list_filter = ('is_verified',)
    
    # Performance: Using double-underscore notation to search through the related User model
    search_fields = ('user__username',)



# PATIENT PROFILE ADMINISTRATION
# Simplified management for individual service seekers

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    #  the profile back to the core user identity for easy cross-referencing
    list_display = ('user',)

