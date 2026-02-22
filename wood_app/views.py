from django.shortcuts import render, redirect
from .models import quotations, contacts as ContactModel
import random
import datetime as dt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

# --- Public Views ---

@never_cache
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def projects(request):
    return render(request, 'project.html')

def featutes(request):
    return render(request, 'feature.html')

def services(request):
    return render(request, 'service.html')

def contacts(request):
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
            messages.success(request, 'Message sent — thank you!')
        except Exception as exc:
            messages.error(request, f'Could not save message: {exc}')
        
        return redirect('contact')

    return render(request, 'contact.html')

def quotes(request):
    return render(request, "quote.html")
@login_required(login_url='login')
def booking(request):
    if request.method == "POST":
        name = request.POST.get('uname', '').strip()
        mail = request.POST.get('umail', '').strip()
        mobile_raw = request.POST.get('mobile', '').strip()
        service = request.POST.get('service', '').strip()
        budget_raw = request.POST.get('budget', '').strip()
        note = request.POST.get('note', '').strip()

        if not name or not mail or not mobile_raw or service in ("", "Select A Service"):
            messages.error(request, "Please fill in all required fields.")
            return redirect('quote')

        try:
            mobile = int(''.join(ch for ch in mobile_raw if ch.isdigit()))
        except ValueError:
            messages.error(request, "Please enter a valid mobile number.")
            return redirect('quote')

        try:
            budget = int(budget_raw)
        except (ValueError, TypeError):
            budget = 0

        try:
            quotations.objects.create(
                name=name, mail=mail, mobile=mobile,
                services=service, budget=budget, note=note
            )
            
            # Prepare booking info for the success page
            bid = (name[:3] + service[:3] + str(random.randint(100, 999))).upper()
            bdate = dt.datetime.now()
            data = {
                "bid": bid,
                "cname": name,
                "bdate": bdate,
                "pdate": bdate + dt.timedelta(days=3),
                "ddate": bdate + dt.timedelta(days=13),
                "snote": note,
                "bvalue": budget,
                "staken": service,
                "cnumber": mobile,
            }
            messages.success(request, f"Quotation submitted — Booking ID: {bid}")
            return render(request, 'booking_info.html', data)

        except Exception as exc:
            messages.error(request, f"Could not save quotation: {exc}")
            return redirect('quote')

    return render(request, 'quote.html')


# --- Authentication Views ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
            
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        c_password = request.POST.get('confirm_password')

        if password != c_password:
            messages.warning(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'User already exists.')
            return redirect('signup')
        
        # Create user and log them in immediately
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, "Signup successful!")
        return redirect('home')

    return render(request, 'signup.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    # We return a redirect that explicitly tells the browser not to cache
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response