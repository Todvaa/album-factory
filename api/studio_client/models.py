from datetime import timedelta
from enum import Enum

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone

from .constants import CODE_LIFETIME


class ConfirmationType(Enum):
    RESET = 'reset'
    SIGNUP = 'signup'


class StudioManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Необходимо указать почту')
        if not password:
            raise ValueError('Необходимо указать пароль')
        email = self.normalize_email(email)
        studio = self.model(email=email, **extra_fields)
        studio.set_password(password)
        studio.save(using=self._db)

        return studio

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Studio(AbstractUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        validators=(EmailValidator(message='Incorrect email'),)
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    username = None
    last_name = None
    last_login = None
    first_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = StudioManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'{self.id} / {self.name} / {self.email}'
        )


class ConfirmationCode(models.Model):
    email = models.EmailField(
        max_length=255,
        validators=(EmailValidator(message='Incorrect email'),)
    )
    code = models.CharField(
        max_length=6,
        blank=False,
        null=False,
    )
    date = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(
        max_length=10,
        choices=[(type.value, type.value) for type in ConfirmationType],
        null=False,
        blank=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'action_type', ),
                name='unique pair'
            )
        ]
        ordering = ['id']

    def __str__(self):
        return (
            f'{self.id} / {self.email} / {self.code} / {self.date}'
        )

    def valid_code(self) -> bool:
        return (timezone.now() - self.date) < timedelta(minutes=CODE_LIFETIME)


class School(models.Model):
    full_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'{self.id} / {self.full_name}'
        )