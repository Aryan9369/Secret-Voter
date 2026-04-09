from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from .managers import UserManager
import random
from django.utils import timezone
from datetime import timedelta

# Regex for Indian Phone Numbers: +91 followed by 10 digits
phone_validator = RegexValidator(
    regex=r'^\+91\d{10}$',
    message="Phone number must be entered in the format: '+919999999999'."
)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        validators=[phone_validator], 
        max_length=13, 
        unique=True
    )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # No other required fields for createsuperuser

    def __str__(self):
        return self.phone_number



class OTPVerification(models.Model):
    phone_number = models.CharField(max_length=13)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        # OTP expires in 5 minutes
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone_number} - {self.otp}"