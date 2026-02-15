from django.shortcuts import render, redirect
from .models import quotations, contacts as ContactModel
import random
import datetime as dt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contacts(request):
    # Handle contact form POST and save to DB (model `contacts`)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not (name and email and subject and message):
            messages.error(request, 'Please fill in all fields.')
            return redirect('contact')

        try:
            ContactModel.objects.create(name=name, email=email, subject=subject, message=message)
        except Exception as exc:
            messages.error(request, f'Could not save message: {exc}')
            return redirect('contact')

        messages.success(request, 'Message sent — thank you!')
        return redirect('contact')

    return render(request, 'contact.html')
def projects(request):
    return render(request,'project.html')

def featutes(request):
    return render(request,'feature.html')

def services(request):
    return render(request,'service.html')

def quotes(request):
    return render(request,"quote.html")

def booking(request):
    # Public quote form — validate and save safely
    if request.method == "POST":
        name = request.POST.get('uname', '').strip()
        mail = request.POST.get('umail', '').strip()
        mobile_raw = request.POST.get('mobile', '').strip()
        service = request.POST.get('service', '').strip()
        budget_raw = request.POST.get('budget', '').strip()
        note = request.POST.get('note', '').strip()

        # Basic validation
        if not name or not mail or not mobile_raw or service in ("", "Select A Service"):
            messages.error(request, "Please fill in all required fields.")
            return redirect('quote')

        # Normalize mobile to digits only and convert to int
        try:
            mobile = int(''.join(ch for ch in mobile_raw if ch.isdigit()))
        except ValueError:
            messages.error(request, "Please enter a valid mobile number.")
            return redirect('quote')

        # Convert budget to int (fallback to 0)
        try:
            budget = int(budget_raw)
        except (ValueError, TypeError):
            budget = 0

        # Save to database with error handling
        try:
            row = quotations.objects.create(
                name=name,
                mail=mail,
                mobile=mobile,
                services=service,
                budget=budget,
                note=note,
            )
        except Exception as exc:
            messages.error(request, f"Could not save quotation: {exc}")
            return redirect('quote')

        # Prepare booking info
        bid = (name[:3] + service[:3] + str(random.randint(100, 999))).upper()
        bdate = dt.datetime.now()
        pdate = bdate + dt.timedelta(days=3)
        ddate = pdate + dt.timedelta(days=10)

        data = {
            "bid": bid,
            "cname": name,
            "bdate": bdate,
            "pdate": pdate,
            "ddate": ddate,
            "snote": note,
            "bvalue": budget,
            "staken": service,
            "cnumber": mobile,
        }

        messages.success(request, f"Quotation submitted — Booking ID: {bid}")
        return render(request, 'booking_info.html', data)

    return render(request, 'quote.html')



def login_view(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(request, username=username, password=password)

        if user is not None:
             login(request,user)
             return redirect('home')
        else:
            messages.error(request,"User Not Found!!!")
            return redirect('login')
    return render(request,'login.html')

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        c_password=request.POST['confirm_password']

        if password==c_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'User Already Exists')
                return render(request,'signup.html')
            else:
                user=User.objects.create_user(username=username,password=password)
                login(request,user)
                messages.info(request,"Signup Succeesfull")
                return redirect('login')

        else:
            messages.warning(request,"Passwords Doesnot Match")
    return render(request,'signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')