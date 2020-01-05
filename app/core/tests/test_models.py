from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Language


class ModelTests(TestCase):

    def test_create_user_model_with_email_successful(self):
        """Test whether creating new user with email is successful"""
        email = "test1@curesio.com"
        password = "testpassword@123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that email for new user is normalized"""
        email = "test@cuREsiO.CoM"
        user = get_user_model().objects.create_user(
            email=email,
            password='test_pass@123'
        )

        self.assertEqual(user.email, email.lower())

    def test_email_required(self):
        """Test that email is required to create a new user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testPass')
            get_user_model().objects.create_user(' ', 'testPass')

    def test_create_user_model_with_user_detail_successful(self):
        """Test that user detail is added successfully while registration"""
        first_name = 'Curesio'
        last_name = 'Pvt LTD',
        date_of_birth = '1997-12-12'        # should be in YYYY-MM-DD
        phone = '+919862878887'
        country = 'India'

        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpass@1234',
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone=phone,
            country=country
        )

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.date_of_birth, date_of_birth)
        self.assertEqual(user.phone, phone)
        self.assertEqual(user.country, country)

    def test_create_user_with_language_successful(self):
        """Test that creating user with language details is successful"""
        lang1 = Language.objects.create(name='English', code='en')
        lang2 = Language.objects.create(name='Bengali', code='ben')

        user = get_user_model().objects.create(
            email='Testname@gmail.com',
            password='testpass@123',
        )
        user.primary_language.set([lang1.pk])
        user.tertiary_language.set([lang2.pk])

        self.assertEqual(user.primary_language.get(pk=lang1.pk), lang1)
        self.assertEqual(user.tertiary_language.get(pk=lang2.pk), lang2)

    def test_create_superuser_successful(self):
        """Test that creating superuser is successful"""
        email = 'test@gmail.com'
        password = 'trst@1234a'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
