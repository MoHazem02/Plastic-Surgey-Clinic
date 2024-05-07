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

# Although there is no register page, I think you may find this code useful (almost same lines will be recalled)
def register(request):
    if request.method == "POST":
        fName = request.POST["fname"]
        LName = request.POST["lname"]
        username = request.POST["uname"]
        email = request.POST["email"]
        gender = request.POST["gender"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        # try:
        #     patient = Patient.objects.create_user(role="PATIENT", first_name=fName, last_name=LName, username= username, password=password, email=email, sex = "M" if gender == "Male" else "F")
        #     patient.save()
        # except IntegrityError:
        #     return render(request, "register.html", {
        #         "message": "Username already taken."
        #     })
        # login(request, patient)
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