from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import UserProfile, Languages


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_new_user(**kwargs):
    """Creates a new user"""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Test the users api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test that creating user with valid credential success"""
        payload = {
            'email': 'test@curesio.com',
            'password': 'Appis@404wrong',
            'username': 'testusername'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=res.data['email'])
        self.assertEqual(user.username, payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists_fails(self):
        """Test that creating new user which already exists fails"""
        payload = {
            'email': 'abck22@gmail.com',
            'password': 'Test@123lifeisabitch',
            'username': 'testuser4'
        }
        create_new_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_password_too_short(self):
        """Test that user creation with password too short fails"""
        payload = {
            'email': 'test1@gmail.com',
            'password': 'pas',
            'username': 'testusername'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(**payload).exists()
        self.assertFalse(user_exists)

    def test_create_token_valid_user(self):
        """Test that token is created for user"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test@1234is_very_bad',
            'username': 'testusername'
        }
        create_new_user(**payload)
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
        create_new_user(**payload)
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
        create_new_user(**payload)
        res = self.client.post(
            TOKEN_URL, {'email': 'test@gmail.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_email(self):
        """Test that no token is created if no email is provided"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test@122443d',
            'username': 'testuser'
        }
        create_new_user(**payload)
        res = self.client.post(
            TOKEN_URL, {'email': '', 'password': 'test@122443d'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user_fails(self):
        """Test that no token is generated if no user is registered"""
        res = self.client.post(
            TOKEN_URL, {'email': 'test@gmail.com', 'password': 'test@562ddg'})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_not_allowed_on_create_user_url(self):
        """Test that retrieving profile details of others fails"""
        create_new_user(**{
            'email': 'temp@curesio.com',
            'password': 'testpass@123df',
            'username': 'tempusername'
        })

        res = self.client.get(CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that requires authentication"""

    def setUp(self):
        self.user = create_new_user(**{
            'email': 'test@curesio.com',
            'password': 'testpass@1234',
            'username': 'testuser'
        })
        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.last_name = 'Lastname'
        self.profile.save()

        self.profile.refresh_from_db()
        self.user.refresh_from_db()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_not_allowed_on_create_user_url(self):
        """Test that retrieving profile details of others fails"""
        create_new_user(**{
            'email': 'temp@curesio.com',
            'password': 'testpass@123df',
            'username': 'testuser12'
        })

        res = self.client.get(CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_profile_success(self):
        """Test that retrieving user profile success"""
        res = self.client.get(ME_URL)
        res_profile = dict(res.data['profile'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], str(self.user))
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

    def test_post_me_not_allowed(self):
        """Test that post is not allowed on me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_user_profile(self):
        """Test updating the user for authenticated user"""
        payload = {
            'email': 'test@curesio.com',
            'password': 'thenew@password44',
            'username': 'newusername',
            'profile': {
                'first_name': 'DarkKnight',
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
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(self.user.username, payload['username'])
        self.assertTrue(self.user.check_password(payload['password']))

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

    def test_cannot_update_details_of_another_user(self):
        """Test that details of another user can not be changed"""
        payload = {
            'email': 'otheruseremail@gmail.com',
            'password': 'testpassword1',
            'username': 'oldusername'
        }
        create_new_user(**payload)

        changed_payload = {
            'email': 'otheruseremail@gmail.com',
            'password': 'testpassword2',
            'username': 'newusername'
        }

        res = self.client.patch(ME_URL, changed_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
