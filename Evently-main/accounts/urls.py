from django.contrib import admin
from django.urls import path
from .views import (
    register,
    signup,
    login,
    login_user,
    dashboard,
    admin_dashboard,
    home,
    event_detail,
    event_register,
)
from django.http import JsonResponse, HttpResponse



urlpatterns = [
   path('', home),
   path('signup/',signup), #signup html page
   path('login/',login), #login hmtl page
   path('dashboard/',dashboard),
   path('register/', register ),
   path('loguser/', login_user ),
   path('admin-dashboard/', admin_dashboard, name="admin_dashboard"),
   # Event routes
   path('events/<int:event_id>/', event_detail, name='event_detail'),
   path('events/<int:event_id>/register/', event_register, name='event_register'),


]
# events/urls.py
