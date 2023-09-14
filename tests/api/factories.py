from random import randint, choice

import factory
from django.db import models
from django.utils import timezone

from common.models import (
    Studio, ConfirmationCode, School, OrderStatus, Order, Template
)
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

    code = randint(100000, 999999)
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


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    full_name = factory.LazyAttribute(lambda _: 'Школа #' + str(randint(100, 999999)))

    studio = factory.SubFactory(StudioFactory)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    class_index = factory.LazyAttribute(lambda _: str(randint(1, 11)) + ' ' + choice('АБВГДЕЖЗИКЛ'))
    customer_first_name = factory.LazyAttribute(lambda _: fake.first_name())
    customer_last_name = factory.LazyAttribute(lambda _: fake.last_name())
    customer_middle_name = factory.LazyAttribute(lambda _: fake.middle_name())
    phone_number = factory.LazyAttribute(lambda _: str(randint(9000000000, 9999999999)))
    albums_count = factory.LazyAttribute(lambda _: randint(1, 50))
    passcode = factory.LazyAttribute(lambda _: randint(100000, 999999))
    status = factory.LazyAttribute(lambda _: OrderStatus.created.name)

    studio = factory.SubFactory(StudioFactory)
    school = factory.SubFactory(SchoolFactory)


class TemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Template

    name = factory.LazyAttribute(lambda _: fake.word())
    public = False
    cover = factory.Faker('text')
    portrait_student_single = factory.Faker('text')
    portrait_student_multi = factory.Faker('text')
    portrait_staff_multi = factory.Faker('text')
    gallery = factory.Faker('text')

    studio = factory.SubFactory(StudioFactory)
