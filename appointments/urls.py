from django.urls import path
from .views import appointment_detail, appointment_list, manage_availability
from .views import assign_therapist
from .views import available_sessions
from .views import book_session



urlpatterns = [
    path('', appointment_list, name='appointment_list'),
    path('detail/<int:appointment_id>/', appointment_detail, name='appointment_detail'),
    path("availability/", manage_availability, name="manage_availability"),
    path("assign/", assign_therapist, name="assign_therapist"),
    path("available/", available_sessions, name="available_sessions"),
    path("book/<int:slot_id>/", book_session, name="book_session")
]