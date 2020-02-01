import tempfile
from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import UserProfile, Languages, Speciality

# Creating urls for making various api calls
DOCTOR_SIGNUP_URL = reverse("doctor:doctor-signup")
TOKEN_URL = reverse("doctor:token")
ME_URL = reverse("doctor:me")


def create_doctor_image_upload_url():
    """Creates url for uploading image for doctor"""
    return reverse('doctor:doctor-image-upload')


def create_new_doctor(**kwargs):
    """Creates a new doctor"""
    doctor = get_user_model().objects.create_doctor(**kwargs)
    doctor.is_active = True
    doctor.save()
    doctor.refresh_from_db()
    return doctor


class PublicUserApiTests(TestCase):
    """Test the doctors api"""

    def setUp(self):
        self.client = APIClient()

        self.speciality = Speciality.objects.create(name='lol')

    def test_create_valid_doctor_success(self):
        """Test that creating doctor with valid credential success"""
        payload = {
            'email': 'test@curesio.com',
            'password': 'Appis@404wrong',
            'username': 'testusername',
            'profile': {
                'first_name': 'first_name',
                'last_name': 'last name',
                'city': 'Tamil Nadu',
                'country': 'IN',
                'primary_language': Languages.ENGLISH
            },
            'doctor_profile': {
                'qualification': 'MBBS',
                'speciality1': [self.speciality.pk]
            }
        }

        res = self.client.post(DOCTOR_SIGNUP_URL, payload, format='json')

        profile_data = dict(res.data['profile'])
        doc_profile = dict(res.data['doctor_profile'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['email'], payload['email'])
        self.assertEqual(res.data['username'], payload['username'])

        self.assertEqual(profile_data['first_name'],
                         payload['profile']['first_name'])
        self.assertEqual(profile_data['last_name'],
                         payload['profile']['last_name'])
        self.assertEqual(profile_data['city'],
                         payload['profile']['city'])
        self.assertEqual(profile_data['country'],
                         payload['profile']['country'])
        self.assertEqual(profile_data['primary_language'],
                         payload['profile']['primary_language'])

        self.assertEqual(doc_profile['qualification'],
                         payload['doctor_profile']['qualification'])
        self.assertEqual(doc_profile['speciality1'],
                         payload['doctor_profile']['speciality1'])
        self.assertEqual(doc_profile['speciality2'], [])

        doctor = get_user_model().objects.get(email=res.data['email'])

        self.assertTrue(doctor.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        self.assertTrue(doctor.is_doctor)
        self.assertFalse(doctor.is_active)
        self.assertFalse(doctor.is_staff)

    def test_create_valid_doctor_full_details_success(self):
        """Test that creating doctor with full credential success"""
        payload = {
            'email': 'test@curesio.com',
            'password': 'Appis@404wrong',
            'username': 'testusername',
            'profile': {
                'first_name': 'first_name',
                'last_name': 'last name',
                'city': 'Tamil Nadu',
                'country': 'IN',
                'primary_language': Languages.ENGLISH
            },
            'doctor_profile': {
                'qualification': 'MBBS',
                'experience': 3.0,
                'highlights': 'test',
                'speciality1': [self.speciality.pk],
                'speciality2': [self.speciality.pk],
                'speciality3': [self.speciality.pk],
                'speciality4': [self.speciality.pk]
            }
        }

        res = self.client.post(
            DOCTOR_SIGNUP_URL,
            payload,
            format='json'
        )
        profile_data = dict(res.data['profile'])
        doc_profile_data = dict(res.data['doctor_profile'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(profile_data['first_name'],
                         payload['profile']['first_name'])
        self.assertEqual(doc_profile_data['qualification'],
                         payload['doctor_profile']['qualification'])
        self.assertEqual(doc_profile_data['experience'],
                         str(payload['doctor_profile']['experience']))
        self.assertEqual(doc_profile_data['highlights'],
                         payload['doctor_profile']['highlights'])
        self.assertEqual(doc_profile_data['speciality1'],
                         payload['doctor_profile']['speciality1'])
        self.assertEqual(doc_profile_data['speciality2'],
                         payload['doctor_profile']['speciality2'])
        self.assertEqual(doc_profile_data['speciality3'],
                         payload['doctor_profile']['speciality3'])
        self.assertEqual(doc_profile_data['speciality4'],
                         payload['doctor_profile']['speciality4'])

    def test_doctor_exists_fails(self):
        """Test that creating new doctor which already exists fails"""
        payload = {
            'email': 'abck22@gmail.com',
            'password': 'Test@123lifeisabitch',
            'username': 'testdoctor4'
        }
        create_new_doctor(**payload)

        res = self.client.post(DOCTOR_SIGNUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_valid_doctor(self):
        """Test that token is created for doctor"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test@1234is_very_bad',
            'username': 'testusername'
        }
        create_new_doctor(**payload)
        payload.pop('username')
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """Test that no token is created invalid credentials"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test@1234is_very_bad',
            'username': 'testusername'
        }
        create_new_doctor(**payload)
        res = self.client.post(TOKEN_URL, {'email': 'test@gmail.com',
                                           'password': 'wrong'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_password(self):
        """Test that no token is created if no password is provided"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test@1234fk',
            'username': 'testusername'
        }
        create_new_doctor(**payload)
        res = self.client.post(
            TOKEN_URL, {'email': 'test@gmail.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_email(self):
        """Test that no token is created if no email is provided"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test@122443d',
            'username': 'testdoctor'
        }
        create_new_doctor(**payload)
        res = self.client.post(
            TOKEN_URL, {'email': '', 'password': 'test@122443d'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_doctor_fails(self):
        """Test that no token is generated if no doctor is registered"""
        res = self.client.post(
            TOKEN_URL, {'email': 'test@gmail.com', 'password': 'test@562ddg'})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_inactive_doctor_fails(self):
        """Test that creating token for inactive doctor fails"""
        payload = {
            'email': 'test@curesio.com',
            'password': 'Appis@404wrong',
            'username': 'testusername',
            'profile': {
                'first_name': 'first_name',
                'last_name': 'last name',
                'city': 'Tamil Nadu',
                'country': 'IN',
                'primary_language': Languages.ENGLISH
            },
            'doctor_profile': {
                'qualification': 'MBBS',
            }
        }

        self.client.post(DOCTOR_SIGNUP_URL, payload, format='json')

        res = self.client.post(
            TOKEN_URL, {'email': payload['email'],
                        'password': payload['password']}
        )

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_not_allowed_on_doctor_signup_url(self):
        """Test that retrieving profile details of others fails"""
        create_new_doctor(**{
            'email': 'temp@curesio.com',
            'password': 'testpass@123df',
            'username': 'tempusername'
        })

        res = self.client.get(DOCTOR_SIGNUP_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_doctor_unauthorized(self):
        """Test that authentication is required for doctor"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that requires authentication"""

    def setUp(self):
        self.doctor = create_new_doctor(**{
            'email': 'test@curesio.com',
            'password': 'testpass@1234',
            'username': 'testdoctor'
        })
        self.doctor.is_active = True
        self.doctor.save()
        self.doctor.refresh_from_db()

        self.profile = UserProfile.objects.get(user=self.doctor)
        self.profile.last_name = 'Lastname'
        self.profile.save()

        self.profile.refresh_from_db()

        self.client = APIClient()
        self.client.force_authenticate(user=self.doctor)

    def test_get_not_allowed_on_doctor_signup_url(self):
        """Test that retrieving profile details of others fails"""
        create_new_doctor(**{
            'email': 'temp@curesio.com',
            'password': 'testpass@123df',
            'username': 'testdoctor12'
        })

        res = self.client.get(DOCTOR_SIGNUP_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_profile_success(self):
        """Test that retrieving doctor profile success"""
        res = self.client.get(ME_URL)
        res_profile = dict(res.data['profile'])
        res_doc_profile = dict(res.data['doctor_profile'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], str(self.doctor))
        self.assertIn('created_date', res.data)
        self.assertEqual(res_profile['first_name'], self.profile.first_name)
        self.assertEqual(res_profile['last_name'], self.profile.last_name)
        self.assertEqual(res_profile['phone'], self.profile.phone)
        self.assertEqual(res_profile['date_of_birth'],
                         self.profile.date_of_birth)
        self.assertEqual(res_profile['city'], self.profile.city)
        self.assertEqual(res_profile['country'], self.profile.country)
        self.assertEqual(res_profile['postal_code'], self.profile.postal_code)
        self.assertEqual(res_profile['address'], self.profile.address)
        self.assertEqual(res_profile['primary_language'], None)
        self.assertEqual(res_profile['secondary_language'], None)
        self.assertEqual(res_profile['tertiary_language'], None)

        self.assertEqual(res_doc_profile['qualification'], '')
        self.assertEqual(res_doc_profile['experience'], None),
        self.assertEqual(res_doc_profile['highlights'], '')
        self.assertEqual(res_doc_profile['speciality1'], [])
        self.assertEqual(res_doc_profile['speciality2'], [])
        self.assertEqual(res_doc_profile['speciality3'], [])
        self.assertEqual(res_doc_profile['speciality4'], [])

    def test_post_me_not_allowed(self):
        """Test that post is not allowed on me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_doctor_profile(self):
        """Test updating the doctor for authenticated doctor"""
        payload = {
            'username': 'newusername',
            'profile': {
                'first_name': 'DarkKnight',
                'last_name': 'lastname',
                'country': "NZ",
                'date_of_birth': '1997-12-23',
                'postal_code': '799250',
                'primary_language': Languages.HINDI,
                'secondary_language': Languages.BENGALI
            }
        }
        res = self.client.patch(ME_URL, payload, format='json')
        res_profile = dict(res.data['profile'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.doctor.username, payload['username'])

        self.assertIn('created_date', res.data)
        self.assertEqual(res_profile['first_name'],
                         payload['profile']['first_name'])
        self.assertEqual(res_profile['date_of_birth'],
                         payload['profile']['date_of_birth'])
        self.assertEqual(res_profile['country'],
                         payload['profile']['country'])
        self.assertEqual(res_profile['postal_code'],
                         payload['profile']['postal_code'])
        self.assertEqual(res_profile['primary_language'],
                         payload['profile']['primary_language'])
        self.assertEqual(res_profile['secondary_language'],
                         payload['profile']['secondary_language'])
        self.assertEqual(res_profile['tertiary_language'],
                         None)

    def test_cannot_update_email_on_manage_user_url(self):
        """Test that email cannot be changed on manage user url"""
        payload = {
            'email': 'otherdoctoremail@gmail.com',
        }

        res = self.client.patch(ME_URL, payload)

        self.assertFalse(res.data['email'] == payload['email'])


class DoctorImageUploadTests(TestCase):
    """Tests for uploading doctor profile picture"""

    def setUp(self):
        """Setup for running all the tests"""
        self.doctor = get_user_model().objects.create_doctor(
            email='temp@curesio.com',
            password='testpass@4',
            username='tempdoctor4'
        )
        self.doctor.is_active = True
        self.doctor.save()
        self.doctor.refresh_from_db()

        self.client = APIClient()
        self.client.force_authenticate(self.doctor)

    def tearDown(self):
        """Clean up code after running the tests"""
        self.doctor.profile.image.delete()

    def test_doctor_profile_picture_upload(self):
        """Test that uploading profile picture is successful"""
        image_upload_url = create_doctor_image_upload_url()

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(
                image_upload_url,
                {'image': ntf},
                format="multipart"
            )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)

    def test_doctor_profile_picture_invalid_image_fails(self):
        """Test that invalid image upload fails"""
        image_upload_url = create_doctor_image_upload_url()

        res = self.client.post(
            image_upload_url,
            {'image': 'invalid image'},
            format="multipart"
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateDotorAPITests(TestCase):
    """Tests for private doctor api"""

    def setUp(self):
        self.client = APIClient()
        self.doctor = get_user_model().objects.create_doctor(
            email='doctor@curesio.com',
            password='testpass@1234',
            username='testusername'
        )
        self.doctor.is_active = True
        self.doctor.save()
        self.doctor.refresh_from_db()

        self.profile = UserProfile.objects.get(user=self.doctor)
        self.profile.last_name = 'Lastname'
        self.profile.save()

        self.profile.refresh_from_db()

        self.client.force_authenticate(user=self.doctor)

    def test_retrieve_doctor_profile_success(self):
        """Test that retrieving doctor profile success"""
        res = self.client.get(ME_URL)
        res_profile = dict(res.data['profile'])
        res_doctor_profile = dict(res.data['doctor_profile'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], str(self.doctor))
        self.assertIn('created_date', res.data)
        self.assertEqual(res_profile['first_name'], self.profile.first_name)
        self.assertEqual(res_profile['last_name'], self.profile.last_name)
        self.assertEqual(res_profile['phone'], self.profile.phone)
        self.assertEqual(res_profile['date_of_birth'],
                         self.profile.date_of_birth)
        self.assertEqual(res_profile['city'], self.profile.city)
        self.assertEqual(res_profile['country'], self.profile.country)
        self.assertEqual(res_profile['postal_code'], self.profile.postal_code)
        self.assertEqual(res_profile['address'], self.profile.address)
        self.assertEqual(res_profile['primary_language'], None)
        self.assertEqual(res_profile['secondary_language'], None)
        self.assertEqual(res_profile['tertiary_language'], None)

        # Doctor specific tests
        self.assertEqual(res_doctor_profile['qualification'], '')
        self.assertEqual(res_doctor_profile['highlights'], '')
        self.assertEqual(res_doctor_profile['experience'], None)
        self.assertEqual(res_doctor_profile['speciality1'], [])
        self.assertEqual(res_doctor_profile['speciality2'], [])
        self.assertEqual(res_doctor_profile['speciality3'], [])
        self.assertEqual(res_doctor_profile['speciality4'], [])

    def test_partial_update_doctor_profile(self):
        """Test updating the doctor for authenticated doctor"""
        payload = {
            'username': 'newusername',
            'profile': {
                'first_name': 'DarkKnight',
                'country': "NZ",
                'date_of_birth': '1997-12-23',
                'postal_code': '799250',
                'primary_language': Languages.HINDI,
                'secondary_language': Languages.BENGALI
            },
            'doctor_profile': {
                'experience': 5.5,
                'qualification': 'MBBS',
                'highlights': 'Achieved award'
            }
        }
        res = self.client.patch(ME_URL, payload, format='json')
        res_profile = dict(res.data['profile'])
        res_doctor_profile = dict(res.data['doctor_profile'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.doctor.username, payload['username'])

        self.assertIn('created_date', res.data)
        self.assertEqual(res_profile['first_name'],
                         payload['profile']['first_name'])
        self.assertEqual(res_profile['date_of_birth'],
                         payload['profile']['date_of_birth'])
        self.assertEqual(res_profile['country'],
                         payload['profile']['country'])
        self.assertEqual(res_profile['postal_code'],
                         payload['profile']['postal_code'])
        self.assertEqual(res_profile['primary_language'],
                         payload['profile']['primary_language'])
        self.assertEqual(res_profile['secondary_language'],
                         payload['profile']['secondary_language'])
        self.assertEqual(res_profile['tertiary_language'],
                         None)

        self.assertEqual(res_doctor_profile['experience'],
                         str(payload['doctor_profile']['experience']))
        self.assertEqual(res_doctor_profile['qualification'],
                         payload['doctor_profile']['qualification'])
        self.assertEqual(res_doctor_profile['highlights'],
                         payload['doctor_profile']['highlights'])
        self.assertEqual(res_doctor_profile['speciality1'], [])


class DoctorUserImageUploadTests(TestCase):
    """Tests for uploading doctor profile picture"""

    def setUp(self):
        """Setup for running all the tests"""
        self.doctor = get_user_model().objects.create_doctor(
            email='temp@curesio.com',
            password='testpass@4',
            username='tempuser4'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.doctor)

    def tearDown(self):
        """Clean up code after running the tests"""
        self.doctor.profile.image.delete()

    def test_doctor_user_profile_picture_upload(self):
        """Test that uploading profile picture is successful"""
        image_upload_url = create_doctor_image_upload_url()

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(
                image_upload_url,
                {'image': ntf},
                format="multipart"
            )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)

    def test_user_profile_picture_invalid_image_fails(self):
        """Test that invalid image upload fails"""
        image_upload_url = create_doctor_image_upload_url()

        res = self.client.post(
            image_upload_url,
            {'image': 'invalid image'},
            format="multipart"
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
