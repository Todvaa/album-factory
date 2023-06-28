from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class Studio(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name='user email',
        help_text='user email',
        validators=(EmailValidator(message='Incorrect email'),)
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    # Точно необязательное?
    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='user first name',
        help_text='user first name',
    )
    order = models.ForeignKey(
        'customer_client.Order',
        on_delete=models.CASCADE,
        related_name='studio'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'{self.id} / {self.name} / {self.email}'
        )
