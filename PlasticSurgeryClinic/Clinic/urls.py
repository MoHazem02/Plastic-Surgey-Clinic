from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_patient, name='register'),
    path("admin", views.admin, name="admin"),
    path("doctor", views.doctor_view, name='doctor'),
    path("nurse", views.nurse_view, name='nurse'),
    path("patient", views.patient_view, name='patient'),   
    path("edit_profile", views.edit_profile, name='edit_profile'),
    path("doctors", views.doctors, name='view doctors'),
    path("Add_Staff", views.add_staff, name='add_staff'),
]
