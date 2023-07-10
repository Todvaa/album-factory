import random

import factory
from django.db import models
from django.utils import timezone

from customer_client.models import Order, OrderStatus
from studio_client.models import Studio, ConfirmationCode
from tests.utils import fake


# see https://factoryboy.readthedocs.io/en/stable/index.html


class StudioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Studio

    name = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.unique.email())

    password = factory.PostGenerationMethodCall('set_password', 'password')


class ConfirmationCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ConfirmationCode

    code = random.randint(100000, 999999)
    action_type = factory.Iterator(['signup', 'reset'])
    email = factory.LazyAttribute(lambda _: fake.unique.email())
    date = factory.LazyAttribute(lambda _: timezone.now())

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        date = kwargs.pop('date', None)
        code = super()._create(target_class, *args, **kwargs)

        if date is not None:
            code.date = date
            models.Model.save(code)

        return code


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    class_index = factory.LazyAttribute(lambda _: str(random.randint(1, 11)) + random.choice('АБВГДЕЖЗИКЛ'))
    customer_first_name = factory.LazyAttribute(lambda _: fake.first_name())
    customer_last_name = factory.LazyAttribute(lambda _: fake.last_name())
    customer_middle_name = factory.LazyAttribute(lambda _: fake.middle_name())
    phone_number = factory.LazyAttribute(lambda _: fake.phone())
    albums_count = factory.LazyAttribute(lambda _: random.randint(1, 50))
    password = factory.LazyAttribute(lambda _: random.randint(100000, 999999))
    status = factory.LazyAttribute(lambda _: OrderStatus.created.value)

    studio = factory.SubFactory(StudioFactory)
    school = factory.SubFactory(SchoolFactory)
