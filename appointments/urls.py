from django.urls import path
from .views import appointment_list, create_appointment

urlpatterns = [
    path('', appointment_list, name='appointment_list'),
    path('create/', create_appointment, name='create_appointment'),
]
