# Generated by Django 4.2.3 on 2023-09-02 11:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[
                django.core.validators.RegexValidator(
                    message='Номер телефона должен состоять из 10 цифр и начинаться с 9', regex='^9\\d{9}$')]),
        ),
    ]
