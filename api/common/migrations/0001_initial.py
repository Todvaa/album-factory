# Generated by Django 4.2.3 on 2023-08-10 21:35

import django.core.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import customer.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True,
                                                  help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                                                  verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
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
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['id'],
            },
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
                ('passcode', models.IntegerField(default=customer.utils.generate_random_passcode)),
                ('status', models.CharField(
                    choices=[('created', 'Создан'), ('portraits_uploading', 'Загрузка портретов'),
                             ('portraits_uploaded', 'Портреты загружены'),
                             ('portraits_processing', 'Обработка портретов'),
                             ('portraits_processed', 'Портреты обработаны'), ('layout', 'Верстка'),
                             ('agreement', 'Согласование'), ('printing', 'Печать'), ('completed', 'Завершен'),
                             ('rejected', 'Отменен')], default='created', max_length=25)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             related_name='order', to='common.school')),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order',
                                             to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddConstraint(
            model_name='confirmationcode',
            constraint=models.UniqueConstraint(fields=('email', 'action_type'), name='unique pair'),
        ),
        migrations.AddField(
            model_name='studio',
            name='groups',
            field=models.ManyToManyField(blank=True,
                                         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                         related_name='user_set', related_query_name='user', to='auth.group',
                                         verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='studio',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                         related_name='user_set', related_query_name='user', to='auth.permission',
                                         verbose_name='user permissions'),
        ),
    ]
