import os
import uuid
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin
from django.core.validators import validate_image_file_extension, \
                                   EmailValidator
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save

from phonenumber_field.modelfields import PhoneNumberField
from django_countries import Countries
from django_countries.fields import CountryField

from rest_framework.authtoken.models import Token


class OperationalCountries(Countries):
    """Overriding countries to include only operational countries."""
    only = ['IN', ]


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


# States available as options in state field
class States_And_Union_Territories:
    ANDAMAN_AND_NICOBAR_ISLANDS = 'AN'
    ANDHRA_PRADESH = 'AP'
    ARUNACHAL_PRADESH = 'AR'
    ASSAM = 'AS'
    BIHAR = 'BR'
    CHANDIGARH = 'CH'
    CHHATTISGARH = 'CT'
    DADRA_AND_NAGAR_HAVELI = 'DN'
    DAMAN_AND_DIU = 'DD'
    DELHI = 'DL'
    GOA = 'GA'
    GUJARAT = 'GJ'
    HARYANA = 'HR'
    HIMACHAL_PRADESH = 'HP'
    JAMMU_AND_KASHMIR = 'JK'
    JHARKHAND = 'JH'
    KARNATAKA = 'KA'
    KERALA = 'KL'
    LAKSHADWEEP = 'LD'
    MADHYA_PRADESH = 'MP'
    MAHARASHTRA = 'MH'
    MANIPUR = 'MP'
    MEGHALAYA = 'ML'
    MIZORAM = 'MZ'
    NAGALAND = 'NL'
    ODISHA = 'OR'
    PONDICHERRY = 'PD'
    PUNJAB = 'PB'
    RAJASHTAN = 'RJ'
    SIKKIM = 'SK'
    TAMIL_NADU = 'TN'
    TELANGANA = 'TG'
    TRIPURA = 'TR'
    UTTAR_PRADESH = 'UP'
    UTTARAKHAND = 'UK'
    WEST_BENGAL = 'WB'

    STATE_IN_STATE_CHOICES = [
        (ANDAMAN_AND_NICOBAR_ISLANDS,
         _(u'Andaman and Nicobar Islands')),
        (ANDHRA_PRADESH, _(u'Andhra Pradesh')),
        (ARUNACHAL_PRADESH, _(u'Arunachal Pradesh')),
        (ASSAM, _(u'Assam')),
        (BIHAR, _(u'Bihar')),
        (CHANDIGARH, _(u'Chandigarh')),
        (CHHATTISGARH, _(u'Chhattishgarh')),
        (DADRA_AND_NAGAR_HAVELI, _(u'Dadra and Nagar Haveli')),
        (DAMAN_AND_DIU, _(u'Daman and Diu')),
        (GOA, _(u'Goa')),
        (GUJARAT, _(u'Gujarat')),
        (HARYANA, _(u'Haryana')),
        (HIMACHAL_PRADESH, _(u'Himachal Pradesh')),
        (JAMMU_AND_KASHMIR, _(u'Jammu and Kashmir')),
        (JHARKHAND, _(u'Jharkhand')),
        (KARNATAKA, _(u'Karnataka')),
        (KERALA, _(u'Kerala')),
        (LAKSHADWEEP, _(u'Lakshadweep')),
        (MADHYA_PRADESH, _(u'Madhya Pradesh')),
        (MAHARASHTRA, _(u'Maharashtra')),
        (MANIPUR, _(u'Manipur')),
        (MEGHALAYA, _(u'Meghalaya')),
        (MIZORAM, _(u'Mizoram')),
        (NAGALAND, _(u'Nagaland')),
        (ODISHA, _(u'Odisha')),
        (PONDICHERRY, _(u'Pondicherry')),
        (PUNJAB, _(u'Punjab')),
        (RAJASHTAN, _(u'Rajasthan')),
        (SIKKIM, _(u'Sikkim')),
        (TAMIL_NADU, _(u'Tamil Nadu')),
        (TELANGANA, _(u'Telangana')),
        (TRIPURA, _(u'Tripura')),
        (UTTAR_PRADESH, _(u'Uttar Pradesh')),
        (UTTARAKHAND, _(u'Uttarakhand')),
        (WEST_BENGAL, _(u'West Bengal')),
    ]


def user_image_upload_file_path(instance, filename):
    """Generates file path for uploading user images in user profile"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    date = datetime.date.today()
    ini_path = f'pictures/uploads/user/{date.year}/{date.month}/{date.day}/'
    full_path = os.path.join(ini_path, file_name)

    return full_path


def procedure_image_upload_file_path(instance, filename):
    """Generates file path for uploading user images in user profile"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    dt = datetime.date.today()
    ini_path = f'pictures/uploads/procedure/{dt.year}/{dt.month}/{dt.day}/'
    full_path = os.path.join(ini_path, file_name)

    return full_path


def hospital_image_upload_file_path(instance, filename):
    """Generates file path for uploading hospital images"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    dt = datetime.date.today()
    ini_path = f'pictures/uploads/hospital/{dt.year}/{dt.month}/{dt.day}/'
    full_path = os.path.join(ini_path, file_name)

    return full_path


def hospital_accreditation_image_upload_file_path(instance, filename):
    """Generates file path for uploading hospital accreditation images"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    dt = datetime.date.today()
    ini_path = f'pictures/uploads/hospital/accreditation/'
    ini_path = ini_path + f'{dt.year}/{dt.month}/{dt.day}/'
    full_path = os.path.join(ini_path, file_name)

    return full_path


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

    def create_doctor(self, email, password, username, **extra_kwargs):
        """Creates and saves a new doctor in inactive state"""

        if not email:
            raise ValueError(_('Email cannot be empty'))

        if not username:
            raise ValueError(_('Username cannot be empty'))

        doctor = self.model(email=self.normalize_email(email),
                            username=username, **extra_kwargs)
        doctor.set_password(password)
        doctor.is_doctor = True
        doctor.is_active = False
        doctor.save(using=self._db)

        Token.objects.create(user=doctor)
        return doctor


class User(AbstractBaseUser, PermissionsMixin):
    """Creates user model that supports using email as username"""
    email = models.EmailField(_('Email'),
                              max_length=255, unique=True,
                              validators=(EmailValidator, ))
    username = models.CharField(_('Username'), max_length=30, unique=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)
    is_doctor = models.BooleanField(_('Is Doctor'), default=False)
    created_date = models.DateTimeField(
        _('Created Date'), default=timezone.now, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        """String representation of user model"""
        return self.email

    class Meta:
        permissions = (
            ('is_active', 'User is active'),
            ('is_staff', 'User is staff'),
            ('is_doctor', 'User is doctor')
        )


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
        _('ZIP / Postal Code'), max_length=12, default='', blank=True)
    address = models.TextField(
        _('Address'), max_length=1024, blank=True, default='')
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
        max_length=1024,
        validators=(validate_image_file_extension,)
    )

    def __str__(self):
        """String representation"""
        return str(self.user)


class Speciality(models.Model):
    """Creates model to store specialities"""
    name = models.CharField(_('Name'), max_length=30, unique=True)

    class Meta:
        verbose_name_plural = 'Specialities'

    def __str__(self):
        return self.name.capitalize()

    def save(self, *args, **kwargs):
        """Overwriting save method to save fields in lower case"""
        self.name = self.name.lower()
        super(Speciality, self).save(*args, **kwargs)


class Doctor(models.Model):
    """Creates model to store details specific to doctor"""
    user = models.OneToOneField(
        'User',
        related_name='doctor_profile',
        on_delete=models.CASCADE,
    )
    experience = models.DecimalField(
        _('Experience'), max_digits=3, decimal_places=1,
        blank=True, null=True
    )
    qualification = models.TextField(
        _('Qualification'), max_length=1024, blank=True, default='')
    highlights = models.TextField(
        _('Highlights'), max_length=1024, blank=True, default='')
    speciality1 = models.ManyToManyField(
        to='Speciality', blank=True, related_name='speciality1')
    speciality2 = models.ManyToManyField(
        to='Speciality', blank=True, related_name='speciality2')
    speciality3 = models.ManyToManyField(
        to='Speciality', blank=True, related_name='speciality3')
    speciality4 = models.ManyToManyField(
        to='Speciality', blank=True, related_name='speciality4')

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        # Creating user profile
        UserProfile.objects.create(user=instance)

        # Creating doctor profile
        if instance.is_doctor:
            Doctor.objects.create(user=instance)
    else:
        instance.profile.save()

        # Saving doctor model
        if instance.is_doctor:
            instance.doctor_profile.save()


class Procedure(models.Model):
    """Model to store procedure details"""
    name = models.CharField(_('Name'), max_length=50, unique=True)
    speciality = models.ManyToManyField(
        to='Speciality',
        blank=True,
        related_name='speciality'
    )
    days_in_hospital = models.IntegerField(
        _('Days in hospital'), blank=True, null=True)
    days_in_destination = models.IntegerField(
        _('Days in destination'), blank=True, null=True)
    duration_minutes = models.IntegerField(
        _('Duration in minutes'), blank=True, null=True)
    overview = models.TextField(_('Overview'), max_length=1000)
    other_details = models.TextField(
        _('Other details'), max_length=1000, blank=True
    )
    image = models.ImageField(
        _('Image'),
        upload_to=procedure_image_upload_file_path,
        null=True,
        blank=True,
        max_length=1024,
        validators=(validate_image_file_extension,)
    )

    def save(self, *args, **kwargs):
        """Overwriting save method to save fields in lower case"""
        self.name = self.name.lower()
        super(Procedure, self).save(*args, **kwargs)

    def __str__(self):
        """Returns string representation of the model"""
        return self.name.capitalize()


class Hospital(models.Model):
    """Model to store hospital details."""
    name = models.CharField(_('Name'), max_length=100)
    state = models.CharField(
        _('State'),
        max_length=2,
        choices=States_And_Union_Territories.STATE_IN_STATE_CHOICES
    )
    country = CountryField(
        _('Country'), countries=OperationalCountries, default='IN')
    postal_code = models.CharField(
        _('ZIP / Postal Code'), max_length=12, default='', blank=True)
    street_name = models.CharField(_('Street Name'), max_length=40)
    location_details = models.TextField(
        _('Location details'), max_length=300, blank=True)
    overview = models.TextField(
        _('overview'), max_length=3000, blank=True)
    staff_details = models.TextField(
        _('Staff Details'), max_length=500, blank=True)
    content_approver_name = models.CharField(
        _('Content Approver Name'), max_length=100, blank=True)
    image1 = models.ImageField(
        _('Image1'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image2 = models.ImageField(
        _('Image2'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image3 = models.ImageField(
        _('Image3'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image4 = models.ImageField(
        _('Image4'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image5 = models.ImageField(
        _('Image5'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image6 = models.ImageField(
        _('Image6'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image7 = models.ImageField(
        _('Image7'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image8 = models.ImageField(
        _('Image8'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image9 = models.ImageField(
        _('Image9'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image10 = models.ImageField(
        _('Image10'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image11 = models.ImageField(
        _('Image11'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )
    image12 = models.ImageField(
        _('Image12'),
        upload_to=hospital_image_upload_file_path,
        blank=True,
        null=True,
        max_length=1024,
        validators=(validate_image_file_extension, )
    )

    def __str__(self):
        return self.name


class Accreditation(models.Model):
    """Model for hospital accreditation"""
    hospital = models.ForeignKey(
        to='Hospital',
        on_delete=models.CASCADE,
        related_name='accreditation'
    )
    name = models.CharField(
        _('Name'), max_length=30)
    image = models.ImageField(
        _('Accreditation image'),
        max_length=1024,
        upload_to=hospital_accreditation_image_upload_file_path,
        blank=True,
        null=True,
        validators=(validate_image_file_extension, )
    )

    def __str__(self):
        return self.name


class Service(models.Model):
    """Model for hospital services"""
    hospital = models.ForeignKey(
        to='Hospital',
        on_delete=models.CASCADE,
        related_name='service'
    )
    name = models.CharField(
        _('Name'), max_length=30)

    def __str__(self):
        return self.name


class HospitalLanguage(models.Model):
    """Model for hospital languages"""
    hospital = models.ForeignKey(
        to='Hospital',
        on_delete=models.CASCADE,
        related_name='hospital_language'
    )
    language = models.CharField(
        _('Language'),
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES,
        max_length=3
    )

    def __str__(self):
        return self.language


class HospitalProcedure(models.Model):
    """Model for hospital procedure"""
    hospital = models.ForeignKey(
        to='Hospital',
        on_delete=models.CASCADE,
        related_name='hospital_procedure'
    )
    procedure = models.ManyToManyField(to='Procedure')

    def __str__(self):
        return ', '.join([p.name for p in self.procedure.all()])


class HospitalDoctor(models.Model):
    """Model for hospital doctor"""
    hospital = models.ForeignKey(
        to='Hospital',
        on_delete=models.CASCADE,
        related_name='hospital_doctor'
    )
    doctor = models.ManyToManyField(to='User')

    def __str__(self):
        string_rep = ''
        for doc in self.doctor.all():
            profile = UserProfile.objects.get(user=doc)
            if profile.first_name:
                if string_rep:
                    string_rep = string_rep + ', ' + \
                                profile.first_name + ' ' + profile.last_name
                else:
                    string_rep = profile.first_name + ' ' + profile.last_name
            else:
                if string_rep:
                    string_rep = string_rep + ', ' + doc.email
                else:
                    string_rep = doc.email

        return string_rep
