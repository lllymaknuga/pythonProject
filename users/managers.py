from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Кастомный менеджер Юзера."""

    def create_user(self, phone, username, **extra_fields):
        """Создание пользователя"""
        if not phone:
            raise ValueError(_('The Phone must be set'))
        user = self.model(username=username, phone=phone, **extra_fields)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        user = self.model(username=username, email=email, password=password, **extra_fields)
        user.save()
        return user
