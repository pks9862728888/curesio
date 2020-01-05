from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_kwargs):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Email should be provided')
        user = self.model(email=self.normalize_email(email), **extra_kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_kwargs):
        """Creates and saves a new user with superuser permission"""
        user = self.create_user(email, password, **extra_kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Creates user model that supports using email as username"""
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255)
    phone = PhoneNumberField(_('Phone'), null=True, blank=True)
    date_of_birth = models.DateField(
        _('Date of Birth'), max_length=10, null=True, blank=True)
    city = models.CharField(
        _('City'), max_length=1024, null=True, blank=True)
    country = CountryField(
        _('Country'), blank_label='(Select country)', null=True, blank=True)
    postal_code = models.CharField(
        _('ZIP / Postal Code'), max_length=12, null=True, blank=True)
    address = models.TextField(
        _('Address'), max_length=1024, null=True, blank=True)
    created_date = models.DateTimeField(
        _('Created Date'), default=timezone.now, editable=False)
    primary_language = models.ManyToManyField(
        'Language', related_name='primary_language')
    secondary_language = models.ManyToManyField(
        'Language', related_name='secondary_language')
    tertiary_language = models.ManyToManyField(
        'Language', related_name='tertiary_language')
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Language(models.Model):
    """Creates language model"""
    name = models.CharField(max_length=30, unique=True)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name + '(' + self.code + ')'
