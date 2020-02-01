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

        dt = datetime.date.today()
        ini_path = f'pictures/uploads/user/{dt.year}/{dt.month}/{dt.day}'
        expected_path = os.path.join(ini_path, f'{uuid}.jpg')

        self.assertEqual(file_path, expected_path)


class DoctorTests(TestCase):
    """Tests cases related to doctor model"""

    def setUp(self):
        self.speciality1 = models.Speciality.objects.create(
            name='Speciality1'
        )
        self.speciality2 = models.Speciality.objects.create(
            name='Speciality2'
        )

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
        doctor.doctor_profile.speciality1.set([self.speciality1])
        doctor.doctor_profile.speciality2.set([self.speciality2])
        doctor.save()

        doctor_profile = Doctor.objects.get(user=doctor)

        self.assertEqual(doctor_profile.experience, 5.0)
        self.assertEqual(doctor_profile.qualification, '')
        self.assertEqual(doctor_profile.speciality1.get(
            pk=self.speciality1.pk), self.speciality1)
        self.assertEqual(doctor_profile.speciality2.get(
            pk=self.speciality2.pk), self.speciality2)
        self.assertEqual(
            str(doctor_profile.speciality3), 'core.Speciality.None')
        self.assertEqual(
            str(doctor_profile.speciality4), 'core.Speciality.None')


class SpecialityTests(TestCase):
    """Tests the speciality model"""

    def test_speciality_success(self):
        """Tests that speciality creation success"""
        speciality = models.Speciality.objects.create(
            name='temp'
        )

        self.assertEqual(speciality.name, 'temp')


class ProcedureTests(TestCase):
    """Tests the procedure model"""

    def test_procedure_add_success(self):
        """Test that adding procedure is success"""
        payload = {
            'name': "Knee Replacement",
            'days_in_hospital': 2,
            'days_in_destination': 2,
            'duration_minutes': 120,
            'overview': '<strong>Bla</strong> bla bla',
            'other_details': "none"
        }

        speciality = models.Speciality.objects.create(name='temp')

        procedure_temp = models.Procedure.objects.create(
            name=payload['name'],
            days_in_hospital=payload['days_in_hospital'],
            days_in_destination=payload['days_in_destination'],
            duration_minutes=payload['duration_minutes'],
            overview=payload['overview'],
            other_details=payload['other_details']
        )
        procedure_temp.speciality.set([speciality])
        procedure_temp.save()

        procedure = models.Procedure.objects.get(
            name=payload['name'].lower()
        )

        self.assertEqual(procedure.name,
                         payload['name'].lower())
        self.assertEqual(procedure.speciality.get(pk=speciality.pk),
                         speciality)
        self.assertEqual(procedure.days_in_hospital,
                         payload['days_in_hospital'])
        self.assertEqual(procedure.days_in_destination,
                         payload['days_in_destination'])
        self.assertEqual(procedure.duration_minutes,
                         payload['duration_minutes'])
        self.assertEqual(procedure.overview, payload['overview'])
        self.assertEqual(procedure.other_details,
                         payload['other_details'])

    @patch('uuid.uuid4')
    def test_procedure_image_upload_url_uuid(self, mock_url):
        """Test that procedure image is uploaded in correct location"""
        uuid = 'test-uuid'
        mock_url.return_value = uuid

        file_path = models.procedure_image_upload_file_path(None, 'proc.jpg')

        dt = datetime.date.today()
        in_path = f'pictures/uploads/procedure/{dt.year}/{dt.month}/{dt.day}'
        expected_path = os.path.join(in_path, f'{uuid}.jpg')

        self.assertEqual(file_path, expected_path)


class HospitalModelTests(TestCase):
    """Tests for Hospital model"""

    def test_create_hospital_min_details_success(self):
        """Test that creating hospital with minimum details is success."""
        payload = {
            'name': 'Test hospital',
            'state': models.States_And_Union_Territories.TRIPURA,
            'country': 'IN',
            'street_name': 'xyz street'
        }

        models.Hospital.objects.create(
            name=payload['name'],
            state=payload['state'],
            country=payload['country'],
            street_name=payload['street_name'],
        )

        hospital = models.Hospital.objects.get(name=payload['name'])

        self.assertEqual(hospital.name, payload['name'])
        self.assertEqual(hospital.state, payload['state'])
        self.assertEqual(hospital.country, payload['country'])

    def test_create_hospital_full_details_success(self):
        """Test that creating hospital is with_full_details_is_success."""
        payload = {
            'name': 'Test hospital',
            'state': models.States_And_Union_Territories.TRIPURA,
            'country': 'IN',
            'postal_code': 799250,
            'street_name': 'xyz street',
            'overview': 'bla bla bla',
            'location_details': 'bla bla bla',
            'staff_details': 'bla bla bla',
            'content_approver_name': 'Anup kumar dey'
        }

        models.Hospital.objects.create(
            name=payload['name'],
            state=payload['state'],
            country=payload['country'],
            postal_code=payload['postal_code'],
            street_name=payload['street_name'],
            overview=payload['overview'],
            location_details=payload['location_details'],
            staff_details=payload['staff_details'],
            content_approver_name=payload['content_approver_name']
        )

        hospital = models.Hospital.objects.get(name=payload['name'])

        self.assertEqual(hospital.name, payload['name'])
        self.assertEqual(hospital.state, payload['state'])
        self.assertEqual(hospital.country, payload['country'])

    @patch('uuid.uuid4')
    def test_hospital_image_upload_file_path_success(self, mock_url):
        """Test that hospital image is uploaded in correct location"""
        uuid = 'test-uuid'
        mock_url.return_value = uuid

        file_path = models.hospital_image_upload_file_path(None, 'img.png')

        dt = datetime.date.today()
        ini_path = f'pictures/uploads/hospital/{dt.year}/{dt.month}/{dt.day}'
        expected_path = os.path.join(ini_path, f'{uuid}.png')

        self.assertEqual(expected_path, file_path)


class AccreditationModelTest(TestCase):
    """Test accreditation model"""

    def setUp(self):
        self.hospital = models.Hospital.objects.create(
            name='name',
            state=models.States_And_Union_Territories.TRIPURA,
            country='IN',
            street_name='street name'
        )

    def test_accreditation_model_creation_success(self):
        """Test that accreditation model creation is success"""

        accreditation = models.Accreditation.objects.create(
            hospital=self.hospital,
            name='bla bla bla'
        )

        self.assertEqual(accreditation.name, 'bla bla bla')

    @patch('uuid.uuid4')
    def test_accreditation_image_upload_file_path_success(self, mock_url):
        """Test that accreditation image is uploaded in correct location"""
        uuid = 'test-uuid'
        mock_url.return_value = uuid

        file_path = models.hospital_accreditation_image_upload_file_path(
            None, 'myimage.png')

        dt = datetime.date.today()
        ini_path = f'pictures/uploads/hospital/accreditation/'
        ini_path = ini_path + f'{dt.year}/{dt.month}/{dt.day}'
        expected_path = os.path.join(ini_path, f'{uuid}.png')

        self.assertEqual(expected_path, file_path)


class ServiceModelTest(TestCase):
    """Tests for service model"""

    def setUp(self):
        self.hospital = models.Hospital.objects.create(
            name='name',
            state=models.States_And_Union_Territories.TRIPURA,
            country='IN',
            street_name='street name'
        )

    def test_service_creation_success(self):
        """Test that service creation is success for hospitals"""
        service = models.Service.objects.create(
            hospital=self.hospital,
            name='test bla bla'
        )

        self.assertEqual(service.name, 'test bla bla')


class HospitalLanguageModelTest(TestCase):
    """Tests for hospital language model"""

    def setUp(self):
        self.hospital = models.Hospital.objects.create(
            name='name',
            state=models.States_And_Union_Territories.TRIPURA,
            country='IN',
            street_name='street name'
        )

    def test_hospital_language_model(self):
        """Test hospital language add success"""
        hospital_language = models.HospitalLanguage.objects.create(
            hospital=self.hospital,
            language=Languages.ENGLISH
        )

        self.assertEqual(hospital_language.language, Languages.ENGLISH)


class HospitalProcedureModelTest(TestCase):
    """Tests for hospital procedure model"""

    def setUp(self):
        self.hospital = models.Hospital.objects.create(
            name='name',
            state=models.States_And_Union_Territories.TRIPURA,
            country='IN',
            street_name='street name'
        )

        self.speciality = models.Speciality.objects.create(
            name='Tempname'
        )

        self.procedure = models.Procedure.objects.create(
            name="Knee Replacement",
            days_in_hospital=2,
            days_in_destination=2,
            duration_minutes=123,
            overview='<strong>Bla</strong> bla bla',
            other_details="none"
        )
        self.procedure.speciality.set([self.speciality])
        self.procedure.save()
        self.procedure.refresh_from_db()

    def test_hospital_procedure_model_success(self):
        """Test hospital procedure add success"""
        hospital_pro = models.HospitalProcedure.objects.create(
            hospital=self.hospital,
        )
        hospital_pro.procedure.set([self.procedure])
        hospital_pro.save()
        hospital_pro.refresh_from_db()

        self.assertEqual(hospital_pro.procedure.get(
            pk=self.procedure.pk), self.procedure
        )


class HospitalDoctorModelTest(TestCase):
    """Tests for hospital doctor model"""

    def setUp(self):
        self.hospital = models.Hospital.objects.create(
            name='name',
            state=models.States_And_Union_Territories.TRIPURA,
            country='IN',
            street_name='street name'
        )
        self.doctor = get_user_model().objects.create_doctor(
            email='test@gmail.com',
            username='testuser',
            password='testpassword@4'
        )

    def test_hospital_doctor_creation_success(self):
        """Test that hospital doctor creation success"""
        hospital_doc = models.HospitalDoctor.objects.create(
            hospital=self.hospital
        )
        hospital_doc.doctor.set([self.doctor])

        self.assertEqual(hospital_doc.hospital, self.hospital)
        self.assertEqual(hospital_doc.doctor.get(
            pk=self.doctor.pk), self.doctor
        )
