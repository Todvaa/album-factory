from random import randint

import factory
from faker import Faker

from customer_client.models import School
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


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = factory.LazyAttribute(lambda _: 'Школа #' + str(randint(100, 999999)))
