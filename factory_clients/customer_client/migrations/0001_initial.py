# Generated by Django 3.2.19 on 2023-06-30 16:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_index', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message='Номер класса должен содержать цифру 1-11 и заглавную букву', regex='^(?:[1-9]|1[0-1]) [А-Я]$')])),
                ('customer_first_name', models.CharField(max_length=150)),
                ('customer_last_name', models.CharField(max_length=150)),
                ('customer_middle_name', models.CharField(blank=True, max_length=150, null=True)),
                ('phone_number', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен состоять из 10 цифр и начинаться с 9', regex='^9\\d{9}$')])),
                ('albums_count', models.IntegerField()),
                ('password', models.CharField(max_length=150)),
                ('status', models.CharField(choices=[('created', 'Создан'), ('portraits_uploaded', 'Портреты загружены'), ('portraits_processed', 'Портреты обработаны'), ('layout', 'Верстка'), ('agreement', 'Согласование'), ('printing', 'Печать'), ('completed', 'Завершен')], default='Создан', max_length=25)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
