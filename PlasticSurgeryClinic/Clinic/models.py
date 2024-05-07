from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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
    completed_appointments = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

class Nurse(User):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    profile_picture = models.CharField(max_length=512, null=True, blank=True)
    working_shift = models.CharField(max_length=8, choices=[('M', 'Morning'), ('E', 'Evening'), ('N', 'Night')], null=True)

class Patient(User):
    age = models.IntegerField(null=True, blank=True)
    history = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=11)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    day = models.CharField(max_length=10, default='Thursday')
    time = models.CharField(max_length=10, default='10:00')
    remarks = models.CharField(max_length=255, null=True, blank=True)