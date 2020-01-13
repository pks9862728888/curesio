# Generated by Django 2.2.9 on 2020-01-13 10:36

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is Staff')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created Date')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='Last Name')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone')),
                ('date_of_birth', models.DateField(blank=True, max_length=10, null=True, verbose_name='Date of Birth')),
                ('city', models.CharField(blank=True, max_length=1024, verbose_name='City')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Country')),
                ('postal_code', models.CharField(blank=True, max_length=12, verbose_name='ZIP / Postal Code')),
                ('address', models.TextField(blank=True, max_length=1024, verbose_name='Address')),
                ('primary_language', models.CharField(blank=True, choices=[('EN', 'English'), ('BN', 'Bengali'), ('HI', 'Hindi')], max_length=3, null=True, verbose_name='Primary language')),
                ('secondary_language', models.CharField(blank=True, choices=[('EN', 'English'), ('BN', 'Bengali'), ('HI', 'Hindi')], max_length=3, null=True, verbose_name='Secondary language')),
                ('tertiary_language', models.CharField(blank=True, choices=[('EN', 'English'), ('BN', 'Bengali'), ('HI', 'Hindi')], max_length=3, null=True, verbose_name='Tertiary language')),
                ('image', models.ImageField(blank=True, max_length=1024, null=True, upload_to=core.models.user_image_upload_file_path, verbose_name='Image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, core.models.Languages),
        ),
    ]
