from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class OrderStatus(Enum):
    created = 'Создан'
    portraits_uploaded = 'Портреты загружены'
    portraits_processed = 'Портреты обработаны'
    create_layout = 'Создать макет'
    agreement = 'Согласование'
    printing = 'Печать'
    completed = 'Завершен'


class Order(AbstractUser):
    class_index = models.CharField(
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^(?:[1-9]|1[0-1])[А-Я]$',
                message='Некорректный номер класса',
            ),
        ]
    )
    customer_first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='customer first name',
    )
    customer_last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='customer last name',
    )
    customer_patronymic = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='customer patronymic',
    )
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^9\d{9}$',
                message='Некорректный номер телефона',
            ),
        ]
    )
    albums_count = models.IntegerField(
        blank=False,
        null=False,
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    status = models.CharField(
        max_length=25,
        choices=[(status.name, status.value) for status in OrderStatus],
        default=OrderStatus.created.value
    )
