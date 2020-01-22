import os
import datetime

from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Languages, UserProfile, Doctor
from core import models


class UserModelTests(TestCase):

    def test_create_user_model_with_email_successful(self):
        """Test whether creating new user with email is successful"""
        email = "test1@curesio.com"
        password = "testpassword@123"
        username = "testuser"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that email for new user is normalized"""
        email = "test@cuREsiO.CoM"
        user = get_user_model().objects.create_user(
            email=email,
            password='test_pass@123',
            username='testuser'
        )

        self.assertEqual(user.email, email.lower())

    def test_email_required(self):
        """Test that email is required to create a new user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '', 'testPass', 'testuser')
            get_user_model().objects.create_user(
                ' ', 'testPass', 'testuser')

    def test_username_required(self):
        """Test that username is required to create a new user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'test@gmail.com', 'testPass', ''
            )
            get_user_model().objects.create_user(
                'test@gmail.com', 'testPass', ' '
            )

    def test_create_user_model_with_default_language_successful(self):
        """Test creating user model with default english language success"""
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpass@1234',
            username='usernameiscool'
        )
        self.assertEqual(user.profile.primary_language, None)
        self.assertEqual(user.profile.secondary_language, None)
        self.assertEqual(user.profile.tertiary_language, None)

    def test_create_user_model_with_user_detail_successful(self):
        """Test that user detail is added successfully while registration"""
        first_name = 'Curesio'
        last_name = 'Pvt LTD'
        date_of_birth = '1997-12-12'        # should be in YYYY-MM-DD
        phone = '+919862878887'
        country = 'IN'
        tertiary_language = Languages.HINDI

        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpass@1234',
            username='testuser'
        )
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.date_of_birth = date_of_birth
        user.profile.phone = phone
        user.profile.country = country
        user.profile.tertiary_language = Languages.HINDI
        user.save()
        user.refresh_from_db()

        self.assertEqual(user.profile.first_name, first_name)
        self.assertEqual(user.profile.last_name, last_name)
        self.assertEqual(str(user.profile.date_of_birth), date_of_birth)
        self.assertEqual(user.profile.phone, phone)
        self.assertEqual(user.profile.country, country)
        self.assertEqual(user.profile.tertiary_language, tertiary_language)

    def test_create_superuser_successful(self):
        """Test that creating superuser is successful"""
        email = 'test@gmail.com'
        password = 'trst@1234a'
        username = 'testuser'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            username=username
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_user_string_representation(self):
        """Test the string representation of user model"""
        email = 'test@gmail.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='test@pass2',
            username='sampleuser'
        )

        self.assertEqual(str(user), email)

    def test_string_representation_of_user_profile(self):
        """Test the string representation of user profile model"""
        email = 'test@gmail.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='testpass@1234',
            username='testuser'
        )
        user_profile = UserProfile.objects.get(user=user)

        self.assertEqual(str(user_profile), email)

    @patch('uuid.uuid4')
    def test_image_upload_url_uuid(self, mock_url):
        """Test that user image is uploaded in the correct location"""
        uuid = 'test-uuid'
        mock_url.return_value = uuid

        file_path = models.user_image_upload_file_path(None, 'myimage.jpg')

        date = datetime.date.today()
        ini_path = f'pictures/uploads/user/{date.year}/{date.month}/{date.day}'
        expected_path = os.path.join(ini_path, f'{uuid}.jpg')

        self.assertEqual(file_path, expected_path)


class DoctorTests(TestCase):
    """Tests cases related to doctor model"""

    def test_create_doctor_successful(self):
        """
        Test that creating doctor successful,
        with minimal requirements.
        """
        email = 'doctor@gmail.com'
        username = 'doctorname'
        password = 'doctorname@curesio.com'
        get_user_model().objects.create_doctor(
            email=email,
            username=username,
            password=password
        )
        user = get_user_model().objects.get(email=email)

        self.assertTrue(user.is_doctor)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_doctor_string_representation(self):
        """Test string representation of doctor table"""
        email = 'doctor@curesio.com'
        doctor = get_user_model().objects.create_doctor(
            email=email,
            username='testdoctor',
            password='testdoctorname@4'
        )
        doctor_profile = Doctor.objects.get(user=doctor)

        self.assertEqual(str(doctor_profile), email)

    def test_doctor_model(self):
        """Test that doctor model creation is successful"""
        email = 'doctor@gmail.com'
        username = 'doctorname'
        password = 'doctorname@curesio.com'
        doctor = get_user_model().objects.create_doctor(
            email=email,
            username=username,
            password=password
        )
        doctor.doctor_profile.experience = 5.0
        doctor.save()

        doctor_profile = Doctor.objects.get(user=doctor)

        self.assertEqual(doctor_profile.experience, 5.0)
        self.assertEqual(doctor_profile.qualification, '')
        self.assertEqual(doctor_profile.highlights, '')


class ProcedureTests(TestCase):
    """Tests the procedure model"""

    def test_procedure_add_success(self):
        """Test that adding procedure is success"""
        payload = {
            'name': "Knee Replacement",
            'speciality': "Orthopedics",
            'days_in_hospital': 2,
            'days_in_destination': 2,
            'duration_minutes': 120,
            'overview': '<strong>Bla</strong> bla bla',
            'other_details': "none"
        }

        models.Procedure.objects.create(
            name=payload['name'],
            speciality=payload['speciality'],
            days_in_hospital=payload['days_in_hospital'],
            days_in_destination=payload['days_in_destination'],
            duration_minutes=payload['duration_minutes'],
            overview=payload['overview'],
            other_details=payload['other_details']
        )

        procedure = models.Procedure.objects.get(
            name=payload['name'].lower()
        )

        self.assertEqual(procedure.name,
                         payload['name'].lower())
        self.assertEqual(procedure.speciality,
                         payload['speciality'].lower())
        self.assertEqual(procedure.days_in_hospital,
                         payload['days_in_hospital'])
        self.assertEqual(procedure.days_in_destination,
                         payload['days_in_destination'])
        self.assertEqual(procedure.duration_minutes,
                         payload['duration_minutes'])
        self.assertEqual(procedure.overview, payload['overview'])
        self.assertEqual(procedure.other_details,
                         payload['other_details'])
