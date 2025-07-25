from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserLoggedInDevices(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='logged_in_devices')
    device_token = models.CharField(max_length=150)
    device_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    first_name = models.CharField(blank=False, null=False, max_length=20)
    is_deleted = models.BooleanField(default=False)
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
    phone_number = PhoneNumberField(blank=True , unique=True, null=True)

    REQUIRED_FIELDS = ['email','first_name']