from django.contrib import admin
from django.urls import  path
from account.views.user_views import RegisterUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterUserView.as_view(), name="sign_up"),
]