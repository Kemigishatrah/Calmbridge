Calmbridge:

 Calmbridge is a Django-based mental health web application designed to connect patients with therapists through a structured, role-based system that prioritizes confidentiality, trust, and professional care delivery.


Overview

Calmbridge facilitates mental health service delivery by enabling therapists to manage appointments while patients securely access their care schedules. The system incorporates therapist verification and role-based access control to ensure professional and ethical use of the platform.
The platform provides separate experiences for patients, therapists, and administrators, ensuring that each role has access only to the tools and information relevant to them.


General Objective
The general objective of the CalmBridge system is to provide a secure, user-friendly digital platform that facilitates efficient access to mental health services by enabling patients to book appointments, communicate confidentially with specialists, and manage mental health care processes in an organized and reliable manner.


Functional Requirements.
1. User Management & Security
•	 The system shall provide separate registration flows for Patients and Specialists.
•	 The system shall require a secure login (Email/Password) and support Password Recovery.
•	The system shall restrict access to features based on user roles (patient, therapist and administrator).
•	The system shall authenticate users using secure login credentials.
•	The system shall implement Session Timeouts to protect patient privacy if a computer is left unattended to.
 
•	 users to log out securely.
2. Patient Requirements.
•	patients to create and update personal profiles.
•	 patients to view available specialists and their schedules.
•	patients to book, reschedule, or cancel appointments.
•	The system shall notify patients of upcoming appointments.
•	 patients to communicate securely with assigned specialists.
•	patients to view their appointment history.

3. Specialist Requirements.
•	 Specialists shall be able to create and edit their Professional profiles 
•	Specialists to set and update availability schedules.
•	The system shall prevent Double-Booking by locking a time slot once a patient initiates a booking.
•	Specialists to view and manage booked appointments.
•	 Specialists to communicate securely with assigned patients.
•	Specialists to create and update session notes.
•	 Specialists to view patient case history relevant to their sessions.

4. Administrative Requirements.
•	Administrators to manage user accounts.
•	Administrators to approve or deactivate therapist accounts.
•	Administrators to assign the verified specialists available.
•	Administrators to monitor system usage and activity.
•	Administrators to maintain system data integrity.

5. Communication & Notifications
•	The system shall provide a Dashboard Inbox where patients and specialists can exchange secure text messages.
•	The system shall automatically send appointment changes and reminders before a session.
•	 The system shall log relevant system activities for audit and troubleshooting purposes.

 Key Features
 For Patients
Register and log in securely
View scheduled therapy appointments
Access care in a structured and guided environment
Profile-based access to personal data only

 For Professionals
Secure registration and login
Therapist verification required before accessing scheduling features
Ability to create and manage appointments
View only assigned appointments (caseload management)

 For Administrators
Verify and approve therapist accounts
Manage users through the Django admin interface
Oversee appointments and platform activity
Ensure system integrity and access control

 Technology Stack
Backend: Django 5.2+
Frontend: HTML5, CSS3, JavaScript
Database: SQLite (development)
Authentication: Django custom user model
Styling: Custom CSS
Architecture: MVC (Model–View–Template)

 Project Structure
calmbridge/
├── manage.py
├── calmbridge/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/accounts/
│
├── appointments/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/appointments/
│
├── templates/
│   ├── base.html
│   └── home.html
│
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── base.js
│
└── venv/

 Installation & Setup   Prerequisites
•	Python 3.11+
•	Virtual environment support
•	Basic knowledge of Django
•	Setup Steps

Clone or download the project
cd calmbridge


Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate   # Windows


Install dependencies

pip install django


Run migrations

python manage.py makemigrations
python manage.py migrate



Start the development server:
python manage.py runserver

Access the application at:
http://127.0.0.1:8000/

 
Future Enhancements

Secure therapist–patient messaging
•	Appointment notifications and reminders
•	Analytics and reporting dashboards
•	Deployment to a production environment
•	Enhanced accessibility and mobile responsiveness
