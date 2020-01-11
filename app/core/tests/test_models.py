from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Languages, UserProfile


class ModelTests(TestCase):

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
