import os
import uuid
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from rest_framework.authtoken.models import Token


def user_image_upload_file_path(instance, filename):
    """Generates file path for uploading user images"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    date = datetime.date.today()
    ini_path = f'pictures/uploads/user/{date.year}/{date.month}/{date.day}/'
    full_path = os.path.join(ini_path, file_name)

    return full_path


# Languages available as options in language field
class Languages:
    ENGLISH = 'EN'
    BENGALI = 'BN'
    HINDI = 'HI'
    LANGUAGE_IN_LANGUAGE_CHOICES = [
        (ENGLISH, _(u'English')),
        (BENGALI, _(u'Bengali')),
        (HINDI, _(u'Hindi'))
    ]


class UserManager(BaseUserManager):

    def create_user(self, email, password, username, **extra_kwargs):
        """Creates and saves a new user"""

        if not email:
            raise ValueError(_('Email cannot be empty'))

        if not username:
            raise ValueError(_('Username cannot be empty'))

        user = self.model(email=self.normalize_email(email),
                          username=username, **extra_kwargs)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)

        return user

    def create_superuser(self, email, password, username, **extra_kwargs):
        """Creates and saves a new user with superuser permission"""
        user = self.create_user(
            email, password, username, **extra_kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Creates user model that supports using email as username"""
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    username = models.CharField(_('Username'), max_length=30, unique=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)
    created_date = models.DateTimeField(
        _('Created Date'), default=timezone.now, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        """String representation of user model"""
        return self.email


class UserProfile(models.Model, Languages):
    """Creates user profile model"""
    user = models.OneToOneField(
        'User',
        related_name='profile',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        _('First Name'), max_length=255, blank=True)
    last_name = models.CharField(
        _('Last Name'), max_length=255, blank=True)
    phone = PhoneNumberField(_('Phone'), null=True, blank=True)
    date_of_birth = models.DateField(
        _('Date of Birth'), max_length=10, null=True, blank=True)
    city = models.CharField(
        _('City'), max_length=1024, blank=True)
    country = CountryField(
        _('Country'), blank=True)
    postal_code = models.CharField(
        _('ZIP / Postal Code'), max_length=12, blank=True)
    address = models.TextField(
        _('Address'), max_length=1024, blank=True)
    primary_language = models.CharField(
        _('Primary language'),
        max_length=3,
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES,
        null=True, blank=True
    )
    secondary_language = models.CharField(
        _('Secondary language'),
        max_length=3,
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES,
        null=True, blank=True
    )
    tertiary_language = models.CharField(
        _('Tertiary language'),
        max_length=3,
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES,
        null=True, blank=True
    )
    image = models.ImageField(
        _('Image'),
        upload_to=user_image_upload_file_path,
        null=True,
        blank=True,
        max_length=1024
    )

    def __str__(self):
        """String representation"""
        return str(self.user)


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
