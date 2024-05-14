from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Doctor, Patient, Nurse, Appointment, Department
# Create your views here.

def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if user.role == 'ADMIN':
                return HttpResponseRedirect(reverse("admin"))
            elif user.role == 'DOCTOR':
                return HttpResponseRedirect(reverse("doctor"))
            elif user.role == 'NURSE':
                return HttpResponseRedirect(reverse("nurse"))
            else:
                return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_patient(request):
    if request.method == "POST":
        fName = request.POST["Fname"]
        LName = request.POST["Lname"]
        username = request.POST["uname"]
        email = request.POST["mail"]
        password = request.POST["patient_password"]
        gender = request.POST["sex"]
        age = request.POST["age"]
        phone = request.POST["phone_number"]

        # Attempt to create new user
        try:
            patient = Patient.objects.create_user(role="PATIENT", first_name=fName, last_name=LName, username= username, password=password, email=email, 
                                                  sex = "M" if gender == "Male" else "F", age=age, phone_number=phone)
            patient.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
    return render(request, "register.html")

def patient_view(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if request.method == "POST":
        time = request.POST.get('time')
        day = request.POST.get('day')
        doctor = Doctor.objects.get(pk = request.POST.get('doctor'))  
        patient = Patient.objects.get(id = request.POST.get('id'))
        
        app = Appointment.objects.create(patient=patient, time=time, day=day, doctor=doctor)
        app.save()

    user_id = request.user.id
    Appointments = Appointment.objects.filter(patient_id = user_id)
    dict = {
        'app': Appointments
    }
    return render(request, "patientportal.html", dict)
    
def doctor_view(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if request.method == "POST":
        return render(request, "doctor.html")
    
    user_id = request.user.id
    Appointments = Appointment.objects.filter(doctor_id = user_id)
    dict = {
        'app': Appointments
    }
    return render(request, "doctor.html", dict)
        
def nurse_view(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if request.method == "POST":
        time = request.POST.get('time')
        day = request.POST.get('day')
        doctor = Doctor.objects.get(pk = request.POST.get('doctor'))  
        patient = Patient.objects.get(id = request.POST.get('id'))
        
        app = Appointment.objects.create(patient=patient, time=time, day=day, doctor=doctor)
        app.save()

    Doctors = Doctor.objects.all()
    Appointments = Appointment.objects.all()

    dict = {
        'doctors': Doctors,
        'appointments': Appointments
    }
    return render(request, "nurseportal.html", dict)

def admin(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if request.method == "POST":
        pass
    else:
        return render(request, "admin.html")
    
def edit_profile(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if request.method == "POST":
        pass
    return render(request, "editProfile.html")

def doctors(request):
    if request.method == "POST":
        pass
    else:
        doctors = Doctor.objects.all()
        return render(request, "admin_view_doctors.html", {"doctors": doctors})

def add_staff(request):
    if request.method == "POST":
        fName = request.POST["fname"]
        LName = request.POST["lname"]
        username = request.POST["uname"]
        email = request.POST["email"]
        password = request.POST["password"]
        profile_pic = request.POST["image_link"]
        gender = request.POST["gender"]
        department = Department.objects.get(pk=int(request.POST.get('dept')))
        medicalDegree = request.POST.get('medicalDegree')
        workingShift = request.POST.get('workingShift')
        shiftOptions = {"Morning": 'M', "Evening": 'E', "Night": 'N'}
        chosenShift = shiftOptions[workingShift]

        # Attempt to create new user
        try:
            doctor = Doctor.objects.create_user(role="DOCTOR", first_name=fName, last_name=LName, username= username, password=password, email=email, 
                                                  sex = "M" if gender == "Male" else "F", department=department, medical_degree=medicalDegree, working_shift=chosenShift, profile_picture=profile_pic)
            doctor.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("view doctors"))
    else:
        return render(request, "add-staff.html")