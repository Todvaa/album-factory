from random import randint

import factory
from django.db import models
from django.utils import timezone
from faker import Faker

from studio_client.models import Studio, ConfirmationCode


# see https://factoryboy.readthedocs.io/en/stable/index.html


class StudioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Studio

    name = factory.LazyAttribute(lambda _: Faker().name())
    email = factory.LazyAttribute(lambda _: Faker().unique.email())

    password = factory.PostGenerationMethodCall('set_password', 'password')


class ConfirmationCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ConfirmationCode

    code = randint(100000, 999999)
    action_type = factory.Iterator(['signup', 'reset'])
    email = factory.LazyAttribute(lambda _: Faker().unique.email())
    date = factory.LazyAttribute(lambda _: timezone.now())

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        date = kwargs.pop('date', None)
        code = super()._create(target_class, *args, **kwargs)

        if date is not None:
            code.date = date
            models.Model.save(code)

        return code
