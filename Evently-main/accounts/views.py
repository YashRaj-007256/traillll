from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from .models import Event, Registration     #custom h ye 
from django.contrib.auth.hashers import make_password, check_password
import jwt
import datetime
from django.utils.timezone import now
from django.contrib.auth.decorators import user_passes_test    
  #6th 
SECRET_KEY = "iamsecretkey" 


# html views

def signup(request):
    return render(request,'signup.html')
def login(request):
    return render(request,'login.html')
def dashboard(request):
    return render(request,'dashboard.html')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def home(request):
    # Ideally fetch events from DB; for now, use a few examples to bind IDs
    events = Event.objects.all().order_by('date')[:10]
    return render(request,'home.html', {"events": events})

# Create your views here
@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({
            "error":"Wrong method"
        })
    print("hello")
    
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    try:
        if not username or not email or not password:
           return JsonResponse({
            "error":"All Fields are Required"
            })
        if User.objects.filter(username=username).exists():
             return JsonResponse({
            "error":"User Already Exist"
            }) 
        
        if User.objects.filter(email=email).exists():
             return JsonResponse({
            "error":"User Already Exist"
            }) 
        user  = User(username=username,email=email,password=make_password(password))
        user.save()
        return JsonResponse({
            "message":"User has been created successfully",
            "status":True
            })
    
    except Exception as e:
      return JsonResponse({
          "error":e
      })

   

@csrf_exempt
def login_user(request):
    print("hello")
    if request.method != 'POST':
        return JsonResponse({"error": "Wrong method"})

    
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            payload = {
                "id": user.id,
                "username": user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) # token expiry
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return JsonResponse({"token": token, "status": True})
        else:
            return JsonResponse({"error": "Invalid password"})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"})
    
    # pip install PyJWT

    # events/views.py


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    ...

def admin_dashboard(request):
    upcoming_events = Event.objects.filter(date__gte=now().date()).order_by("date")[:5]
    total_registrations = Registration.objects.count()
    recent_registrations = Registration.objects.select_related("student", "event").order_by("-registered_at")[:5]

    context = {
        "upcoming_events": upcoming_events,
        "total_registrations": total_registrations,
        "recent_registrations": recent_registrations,
    }
    return render(request, "admin_dashboard.html", context)



def dashboard_data(request):
    data = {
        "events": [
            {"name": "Tech Fest", "date": "2025-09-20"},
            {"name": "Cultural Night", "date": "2025-09-25"},
        ],
        "registrations": 128,
        "activities": [
            "Rahul registered for Tech Fest",
            "Ananya uploaded project details",
            "Vikram joined Cultural Night"
        ]
    }
    return JsonResponse(data)
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {"event": event})

@csrf_exempt
def event_register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        # In a real app, bind to the logged-in user. For now, use the first user if exists.
        try:
            student = User.objects.first()
            Registration.objects.create(event=event, student=student)
            return JsonResponse({"status": True, "message": "Registered successfully"})
        except Exception as e:
            return JsonResponse({"status": False, "error": str(e)})
    # GET shows a simple confirmation page
    return render(request, 'event_register.html', {"event": event})

