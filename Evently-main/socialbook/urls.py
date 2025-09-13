
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # project/urls.py

    path("", include("accounts.urls")),

]


# http://localhost:8000/accounts