from enum import Enum

from django.core.validators import RegexValidator
from django.db import models


class OrderStatus(Enum):
    created = 'Создан'
    portraits_uploaded = 'Портреты загружены'
    portraits_processed = 'Портреты обработаны'
    layout = 'Верстка'
    agreement = 'Согласование'
    printing = 'Печать'
    completed = 'Завершен'


class Order(models.Model):
    class_index = models.CharField(
        max_length=4,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^(?:[1-9]|1[0-1]) [А-Я]$',
                message=(
                    'Номер класса должен содержать '
                    'цифру 1-11 и заглавную букву'
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
        unique=True,
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
    studio = models.ForeignKey(
        'studio_client.Studio',
        on_delete=models.CASCADE,
        related_name='order'
    )
    school = models.ForeignKey(
        'studio_client.School',
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
        'studio_client.School',
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
