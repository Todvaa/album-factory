# Generated by Django 4.2.3 on 2023-09-01 12:31

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import common.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, validators=[
                    django.core.validators.EmailValidator(message='Incorrect email')])),
                ('code', models.CharField(max_length=6)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('action_type', models.CharField(choices=[('reset', 'reset'), ('signup', 'signup')], max_length=10)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_index', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(
                    message='Номер класса должен содержать число 1-11 и заглавную букву через пробел',
                    regex='^(?:[1-9]|1[0-1]) [А-Я]$')])),
                ('customer_first_name', models.CharField(max_length=150)),
                ('customer_last_name', models.CharField(max_length=150)),
                ('customer_middle_name', models.CharField(blank=True, max_length=150, null=True)),
                ('phone_number', models.CharField(max_length=10, null=True, validators=[
                    django.core.validators.RegexValidator(
                        message='Номер телефона должен состоять из 10 цифр и начинаться с 9', regex='^9\\d{9}$')])),
                ('albums_count', models.IntegerField()),
                ('passcode', models.IntegerField(default=common.utils.generate_random_passcode)),
                ('status', models.CharField(
                    choices=[('created', 'Создан'), ('portraits_uploading', 'Загрузка портретов'),
                             ('portraits_uploaded', 'Портреты загружены'),
                             ('portraits_processing', 'Обработка портретов'),
                             ('portraits_processed', 'Портреты обработаны'), ('layout', 'Верстка'),
                             ('agreement', 'Согласование'), ('printing', 'Печать'), ('completed', 'Завершен'),
                             ('rejected', 'Отменен')], default='created', max_length=25)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PersonStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vector', models.TextField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s3_url', models.CharField(max_length=255, unique=True)),
                ('faces_count', models.IntegerField()),
                ('focus', models.FloatField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('type',
                 models.CharField(blank=True, choices=[('staged', 'staged'), ('reportage', 'reportage')], max_length=10,
                                  null=True)),
                ('horizont', models.IntegerField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.order')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True, validators=[
                    django.core.validators.EmailValidator(message='Incorrect email')])),
                ('password', models.CharField(max_length=150)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school',
                                             to='common.studio')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PhotoPersonStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_fill_percent', models.IntegerField(blank=True, null=True)),
                ('blink', models.BooleanField(blank=True, null=True)),
                ('look_to_camera', models.BooleanField(blank=True, null=True)),
                ('person_student',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.personstudent',
                                   verbose_name='person_student')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.photo',
                                            verbose_name='photo')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='personstudent',
            name='main_photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_photo',
                                    to='common.photo'),
        ),
        migrations.AddField(
            model_name='personstudent',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.order'),
        ),
        migrations.AddField(
            model_name='personstudent',
            name='photos',
            field=models.ManyToManyField(related_name='photo', through='common.PhotoPersonStudent', to='common.photo',
                                         verbose_name='student photos'),
        ),
        migrations.CreateModel(
            name='PersonStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=150)),
                ('first_name', models.CharField(max_length=150)),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True)),
                ('school_subject', models.CharField(max_length=150)),
                ('photo', models.ImageField(upload_to='person_staff_photo/')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_staff',
                                             to='common.school')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='order', to='common.school'),
        ),
        migrations.AddField(
            model_name='order',
            name='studio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order',
                                    to='common.studio'),
        ),
        migrations.AddConstraint(
            model_name='confirmationcode',
            constraint=models.UniqueConstraint(fields=('email', 'action_type'), name='unique pair'),
        ),
        migrations.AddConstraint(
            model_name='photopersonstudent',
            constraint=models.UniqueConstraint(fields=('photo', 'person_student'),
                                               name='unique pair for photo and person_student'),
        ),
    ]
