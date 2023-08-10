from datetime import timedelta
from enum import Enum

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.utils import timezone

from customer.utils import generate_random_passcode
from studio.constants import CODE_LIFETIME


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


class OrderStatus(Enum):
    created = 'Создан'
    portraits_uploading = 'Загрузка портретов'
    portraits_uploaded = 'Портреты загружены'
    portraits_processing = 'Обработка портретов'
    portraits_processed = 'Портреты обработаны'
    layout = 'Верстка'
    agreement = 'Согласование'
    printing = 'Печать'
    completed = 'Завершен'
    rejected = 'Отменен'


class Order(models.Model):
    class_index = models.CharField(
        max_length=4,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^(?:[1-9]|1[0-1]) [А-Я]$',
                message=(
                    'Номер класса должен содержать число '
                    '1-11 и заглавную букву через пробел'
                ),
            ),
        ]
    )
    customer_first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    customer_last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    customer_middle_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=10,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^9\d{9}$',
                message=(
                    'Номер телефона должен состоять'
                    ' из 10 цифр и начинаться с 9'
                ),
            ),
        ]
    )
    albums_count = models.IntegerField(
        blank=False,
        null=False,
    )
    passcode = models.IntegerField(
        null=False,
        default=generate_random_passcode
    )
    status = models.CharField(
        max_length=25,
        choices=[(status.name, status.value) for status in OrderStatus],
        default=OrderStatus.created.name
    )
    studio = models.ForeignKey(
        'studio.Studio',
        on_delete=models.CASCADE,
        related_name='order'
    )
    school = models.ForeignKey(
        'studio.School',
        on_delete=models.CASCADE,
        related_name='order',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'{self.id} / {self.customer_last_name} / {self.class_index}'
        )


class PersonStaff(models.Model):
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    middle_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    school_subject = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    photo = models.ImageField(
        upload_to='person_staff_photo/',
        blank=False,
        null=False,
    )
    school = models.ForeignKey(
        'studio.School',
        on_delete=models.CASCADE,
        related_name='person_staff'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'{self.last_name} / {self.school.full_name}'
            f' / {self.school_subject}'
        )
