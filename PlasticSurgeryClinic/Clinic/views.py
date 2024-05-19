from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Doctor, Patient, Nurse, Appointment, Department
import datetime, requests
# Create your views here.

def index(request):
    doctors = Doctor.objects.all()
    return render(request, "index.html", {"doctors": doctors})


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
        date_of_birth = request.POST["date"]
        phone = request.POST["phone_number"]

        # Attempt to create new user
        try:
            patient = Patient.objects.create_user(role="PATIENT", first_name=fName, last_name=LName, username= username, password=password, email=email, 
                                                  sex = "M" if gender == "Male" else "F", date_of_birth=date_of_birth, phone_number=phone)
            patient.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
    return render(request, "register.html")

def cancel_appointment(request):
    if request.method == "POST":
        appointment = Appointment.objects.get(pk = request.POST.get('appointment_id'))
        appointment.delete()
    return HttpResponseRedirect(reverse("patient"))

def patient_view(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if request.method == "POST":
        time = request.POST.get('time')
        date = request.POST.get('date')
        doctor = Doctor.objects.get(pk = request.POST.get('doctor'))  
        patient = Patient.objects.get(pk = request.user.id)
        
        app = Appointment.objects.create(patient=patient, time=time, date=date, doctor=doctor)
        app.save()

    user_id = request.user.id
    Appointments = Appointment.objects.filter(patient_id = user_id)

    today = datetime.date.today()
    past_appointments = Appointments.filter(date__lt=today)
    future_appointments = Appointments.filter(date__gte=today)

    

    Doctors = Doctor.objects.all()
    dict = {
        'doctors': Doctors,
        'past_app': past_appointments,
        'future_app': future_appointments
    }
    return render(request, "patientportal.html", dict)
    
def doctor_view(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if request.method == "POST":
        appointment = Appointment.objects.get(pk = request.POST.get('appointment'))
        notes = request.POST.get('notes')
        print(appointment)
        print(notes)
        appointment.remarks = notes
        appointment.save()
    
    user_id = request.user.id
    today = datetime.date.today()

    Appointments = Appointment.objects.filter(doctor_id = user_id, date=today)
    dict = {
        'apps': Appointments,
        'doctor': Doctor.objects.get(pk = user_id)
    }
    return render(request, "DoctorPortal.html", dict)
        
def nurse_view(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    nurse = Nurse.objects.get(pk = request.user.id)
    return render(request, "nurseportal.html", {"nurse": nurse})

def admin(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if request.method == "POST":
        # TODO: Update the patient's data in the databse with the new data
        pass
    else:
        total_patients = Patient.objects.all().count()
        total_appointments = Appointment.objects.all().count()
        return render(request, "admin.html", {"total_patients": total_patients, "total_appointments": total_appointments})
    
def edit_profile(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    user = request.user
    if request.method == "POST":
        user.email = request.POST.get("email", user.email)
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
        if old_password and new_password and confirm_password:
            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    logout(request)
                    return HttpResponseRedirect(reverse("staff_login"))
                else:
                    return render(request, "editProfile.html",
                                  {"user": user, "error_message": "New passwords do not match."})
            else:
                return render(request, "editProfile.html",
                              {"user": user, "error_message": "Old password is incorrect."})

        user.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "editProfile.html", {"user": user})


def doctors(request):
    if request.method == "POST":
        pass
    else:
        doctors = Doctor.objects.all()
        return render(request, "admin_view_doctors.html", {"doctors": doctors})
    
def nurses(request):
    if request.method == "POST":
        pass
    else:
        nurses = Nurse.objects.all()
        return render(request, "admin_view_nurses.html", {"nurses": nurses})

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

def add_nurses(request):
    if request.method == "POST":
        fName = request.POST["fname"]
        LName = request.POST["lname"]
        username = request.POST["uname"]
        email = request.POST["email"]
        password = request.POST["password"]
        profile_pic = request.POST["image_link"]
        gender = request.POST["gender"]
        department = Department.objects.get(pk=int(request.POST.get('dept')))
        workingShift = request.POST.get('workingShift')
        shiftOptions = {"Morning": 'M', "Evening": 'E', "Night": 'N'}
        chosenShift = shiftOptions[workingShift]

        # Attempt to create new user
        try:
            nurse = Nurse.objects.create_user(role="NURSE", first_name=fName, last_name=LName, username= username, password=password, email=email, 
                                                  sex = "M" if gender == "Male" else "F", department=department, working_shift=chosenShift, profile_picture=profile_pic)
            nurse.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("view nurses"))
    else:
        return render(request, "add-staff-nurses.html")

def disease_info(request):
    query = request.GET.get('query', 'COVID-19').lower()
    if query == 'covid-19':
        url = "https://disease.sh/v3/covid-19/continents"
    elif query == 'influenza':
        url = "https://disease.sh/v3/influenza/cdc/ILINet"
    else:
        return JsonResponse({'error': 'Invalid query'}, status=400)

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        return JsonResponse({'error': 'Failed to retrieve data'}, status=response.status_code)

    return render(request, 'disease_info.html', {'disease_data': data, 'query': query})

