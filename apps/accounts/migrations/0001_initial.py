# Generated by Django 4.0.1 on 2022-01-27 23:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('mobile_number', models.CharField(help_text='Mobile Number', max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^[6-9]\\d{9}$', 'Please enter a valid mobile number')])),
                ('name', models.CharField(help_text='Name of User', max_length=50)),
                ('is_staff', models.BooleanField(default=False, help_text='This user can access admin panel')),
                ('is_admin', models.BooleanField(default=False, help_text='This user has all permissions without explicitly assigning them')),
                ('password', models.CharField(max_length=150)),
                ('summary', models.CharField(blank=True, help_text='Summary of the user', default="Hi there! I'm using gossip", max_length=500)),
                ('profile_pic', models.CharField(blank=True, default='https://www.iiitdm.ac.in/Profile/images/Profile/mdm17d002.png', help_text='Profile pic url of the user', max_length=300)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
