from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class StudioManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
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
