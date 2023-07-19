from faker import Faker
from rest_framework.test import APIClient

fake = Faker(locale='ru-RU')
client = APIClient()
