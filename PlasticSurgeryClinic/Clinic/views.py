from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Doctor, Patient, Nurse
# Create your views here.

def index(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("login"))
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    
@login_required    
def doctor_view(request):
    if request.method == "POST":
        pass
    else:
        pass
    
@login_required    
def nurse_view(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "nurseportal.html")

@login_required
def admin(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "doctor.html")