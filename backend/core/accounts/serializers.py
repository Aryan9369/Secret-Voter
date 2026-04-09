from rest_framework import serializers
from .models import User, phone_validator

class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[phone_validator])

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[phone_validator])
    otp = serializers.CharField(max_length=6, min_length=6)