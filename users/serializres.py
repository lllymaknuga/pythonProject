from abc import ABC

from rest_framework import serializers

from users.models import CustomUser
from users.validators import TelephoneNumberValidator


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class PhoneRegistrationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, validators=[])


class PhoneValidatorSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    otp_code = serializers.IntegerField()
    username = serializers.CharField(max_length=20)
