from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import TelephoneNumberValidator
from .managers import UserManager


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=13, unique=True, verbose_name='Номер телефона',
                             validators=[TelephoneNumberValidator()])
    objects = UserManager()


class OtpToken(models.Model):
    phone = models.CharField(max_length=13, verbose_name='Номер телефона',
                             validators=[])
    data_send = models.DateTimeField(auto_now=True)
    otp_code = models.IntegerField()
    # attempts = models.IntegerField(default=0)
    # is_active = models.BooleanField(default=True)
