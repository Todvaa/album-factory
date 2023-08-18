from datetime import timedelta
from enum import Enum

from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.utils import timezone

from common.utils import generate_random_passcode
from studio.constants import CODE_LIFETIME


class ConfirmationType(Enum):
    RESET = 'reset'
    SIGNUP = 'signup'


class Studio(models.Model):
    is_authenticated = True

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

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

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
                fields=('email', 'action_type',),
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
    studio = models.ForeignKey(
        'common.Studio',
        on_delete=models.CASCADE,
        related_name='school'
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
    is_authenticated = True
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
        'common.Studio',
        on_delete=models.CASCADE,
        related_name='order'
    )
    school = models.ForeignKey(
        'common.School',
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
        'common.School',
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
