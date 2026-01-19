Calmbridge

Calmbridge is a Django-based mental health web application designed to connect patients with therapists through a structured, role-based system that prioritizes confidentiality, trust, and professional care delivery.

The platform provides separate experiences for patients, therapists, and administrators, ensuring that each role has access only to the tools and information relevant to them.

 Overview

Calmbridge facilitates mental health service delivery by enabling therapists to manage appointments while patients securely access their care schedules. The system incorporates therapist verification and role-based access control to ensure professional and ethical use of the platform.

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

 Platform-Wide
Role-based authentication and authorization
Secure session management
Clean and responsive user interface
Separation of responsibilities across system roles
Privacy-first design principles

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
 Installation & Setup
Prerequisites

Python 3.11+

Virtual environment support

Basic knowledge of Django

Setup Steps

Clone or download the project

git clone <repository-url>
cd calmbridge


Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate   # Windows


Install dependencies

pip install django


Run migrations

python manage.py makemigrations
python manage.py migrate


Create an admin account

python manage.py createsuperuser


Start the development server

python manage.py runserver


Access the application at:

http://127.0.0.1:8000/

 User Roles & Access
Administrator

Full access to the system

Therapist verification and oversight

User and appointment management

Therapist

Access granted only after admin verification

Create and manage appointments

View only their assigned caseload

Patient

View scheduled appointments

Access personal care information

No access to other users’ data

 Testing the Workflow

Register a therapist account

Attempt scheduling → blocked until verified

Admin verifies therapist

Therapist schedules appointments

Patient registers and views appointments

 Project Purpose

Calmbridge serves as a proof-of-concept mental health platform, demonstrating:

Secure role-based access

Professional verification workflows

Clean separation of responsibilities

Scalable Django project structure

Practical application of privacy-aware design

Future Enhancements

Secure therapist–patient messaging

Appointment notifications and reminders

Analytics and reporting dashboards

Deployment to a production environment

Enhanced accessibility and mobile responsiveness