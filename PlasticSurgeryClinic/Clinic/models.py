from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    role = models.CharField(max_length=30, choices=[('ADMIN', 'Admin'), ('DOCTOR', 'Doctor'), ('NURSE', 'Nurse'), ('PATIENT', 'Patient')], default='PATIENT')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], default='M')

class Doctor(User):
    medical_degree = models.CharField(max_length=30, choices=[('Specialist', 'Specialist'), ('Consultant', 'Consultant')], default='Specialist')
    working_shift = models.CharField(max_length=8, choices=[('M', 'Morning'), ('E', 'Evening'), ('N', 'Night')])
    profile_picture = models.CharField(max_length=512, null=True, blank=True)
    rating = models.FloatField(default=5.0, blank=True)
    specialization = models.CharField(max_length=30, choices=[('Hair', 'Hair'), ('Skin', 'Skin'), ('General', 'General')], default='General')
    completed_appointments = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"Dr. {self.first_name} {self.last_name}"
    
class Nurse(User):
    specialization = models.CharField(max_length=30, choices=[('Hair', 'Hair'), ('Skin', 'Skin'), ('General', 'General')], default='General')

class Patient(User):
    age = models.IntegerField(null=True, blank=True)
    history = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=11)