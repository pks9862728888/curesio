from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

# from core import models

PROCEDURE_URL = reverse("staff:procedure-add")


class PublicUserAPITests(TestCase):
    """Tests for public users"""

    def setUp(self):
        """Setup code for running public tests"""
        self.client = APIClient()

        self.payload = {
            'name': "Knee Replacement",
            'speciality': "Orthopedics",
            'days_in_hospital': 2,
            'days_in_destination': 2,
            'duration_minutes': 120,
            'overview': '<strong>Bla</strong> bla bla',
        }

    def test_create_procedure_by_unauthenticated_staff_fails(self):
        """Test creating procedure by unauthenticated staff fails"""
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpassword',
            username='testusername'
        )
        user.is_staff = True
        user.save()
        user.refresh_from_db()

        res = self.client.post(PROCEDURE_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_procedure_by_user_failure(self):
        """Test creating procedure by user failure"""
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpassword',
            username='testusername'
        )
        self.client.force_authenticate(user=user)

        res = self.client.post(PROCEDURE_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class StaffAPITests(TestCase):
    """Tests for staff"""

    def setUp(self):
        """Setup code for running all the tests"""
        self.staff = get_user_model().objects.create_user(
            email='staff@curesio.com',
            password='staffpassword1234',
            username='staffusername'
        )
        self.staff.is_staff = True
        self.staff.save()
        self.staff.refresh_from_db()

        self.client = APIClient()
        self.client.force_authenticate(user=self.staff)

        self.payload = {
            'name': "Knee Replacement",
            'speciality': "Orthopedics",
            'days_in_hospital': 2,
            'days_in_destination': 2,
            'duration_minutes': 120,
            'overview': '<strong>Bla</strong> bla bla',
        }

    def test_create_procedure_success(self):
        """Test creating valid procedure by staff success"""

        res = self.client.post(PROCEDURE_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'],
                         self.payload['name'].lower())
        self.assertEqual(res.data['speciality'],
                         self.payload['speciality'].lower())
        self.assertEqual(res.data['days_in_hospital'],
                         self.payload['days_in_hospital'])
        self.assertEqual(res.data['days_in_destination'],
                         self.payload['days_in_destination'])
        self.assertEqual(res.data['duration_minutes'],
                         self.payload['duration_minutes'])
        self.assertEqual(
            res.data['overview'], self.payload['overview'])
        self.assertEqual(res.data['other_details'], '')
