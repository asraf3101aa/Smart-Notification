from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('notifications/', include('v1.notifications.urls')),
    path('users/', include('v1.users.urls')),
]
