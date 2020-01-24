import tempfile
from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from staff import serializer

PROCEDURE_URL = reverse("staff:procedure-list")


def get_item_url(pk):
    """Used to get item delete url"""
    return reverse('staff:procedure-detail', args=[pk])


def create_new_user():
    """Creates a new user"""
    return get_user_model().objects.create_user(
        email='test@gmail.com',
        password='test@londodnjisdjfois',
        username='tempusername'
    )


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

    def test_list_procedure_success_unauthenticated_user(self):
        """Test that list procedure is success"""
        models.Procedure.objects.create(
            name="procedure1",
            speciality='Orthopedics',
            overview='bla bla bla'
        )
        models.Procedure.objects.create(
            name="procedure2",
            speciality='Orthopedics',
            overview='bla bla bla'
        )

        res = self.client.get(PROCEDURE_URL)

        procedures = models.Procedure.objects.all().order_by("-name")
        ser = serializer.ProcedureSerializer(procedures, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, ser.data)

    def test_unauthenticated_user_post_request_failure(self):
        """Test that post request fails for unauthenticated user"""

        res = self.client.post(PROCEDURE_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_delete_procedure_failure(self):
        """Test that deleting procedure by unauthenticated user fails"""
        models.Procedure.objects.create(
            name='temp',
            speciality='tempspecila',
            overview='bla bla bla'
        )

        res = self.client.get(PROCEDURE_URL)

        url = get_item_url(res.data[0]['id'])
        del_procedure = self.client.delete(url)

        self.assertEqual(del_procedure.status_code,
                         status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test for authenticated user"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_new_user()
        self.client.force_authenticate(user=self.user)

        self.payload = {
            'name': 'payload',
            'speciality': 'orthopedics',
            'overview': 'bla bla bla'
        }

    def test_list_procedure_success_authenticated_user(self):
        """Test that list procedure is success"""
        models.Procedure.objects.create(
            name="procedure1",
            speciality='Orthopedics',
            overview='bla bla bla'
        )
        models.Procedure.objects.create(
            name="procedure2",
            speciality='Orthopedics',
            overview='bla bla bla'
        )

        res = self.client.get(PROCEDURE_URL)

        procedures = models.Procedure.objects.all().order_by("-name")
        ser = serializer.ProcedureSerializer(procedures, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, ser.data)

    def test_authenticated_user_post_request_failure(self):
        """Test that post request fails for authenticated user"""

        res = self.client.post(PROCEDURE_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_procedure_failure(self):
        """Test that deleting procedure by user fails"""
        models.Procedure.objects.create(
            name='temp',
            speciality='tempspecila',
            overview='bla bla bla'
        )

        res = self.client.get(PROCEDURE_URL)

        url = get_item_url(res.data[0]['id'])
        del_procedure = self.client.delete(url)

        self.assertEqual(del_procedure.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_user_update_procedure_failure(self):
        """Test that updating procedure by user fails"""
        models.Procedure.objects.create(
            name='temp',
            speciality='tempspecila',
            overview='bla bla bla'
        )

        res = self.client.get(PROCEDURE_URL)

        url = get_item_url(res.data[0]['id'])
        new_payload = {
            'other_details': 'new details'
        }

        response = self.client.patch(url, new_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StaffAPITests(TestCase):
    """Tests for staff API"""

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
            'overview': '<strong>Bla</strong> bla bla',
        }

    def test_list_procedure_success_for_staff(self):
        """Test that list procedure is success"""
        models.Procedure.objects.create(
            name="procedure1",
            speciality='Orthopedics',
            overview='bla bla bla'
        )
        models.Procedure.objects.create(
            name="procedure2",
            speciality='Orthopedics',
            overview='bla bla bla'
        )

        res = self.client.get(PROCEDURE_URL)

        procedures = models.Procedure.objects.all().order_by("-name")
        ser = serializer.ProcedureSerializer(procedures, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, ser.data)

    def test_create_valid_procedure_authenticated_staff_success(self):
        """Test creating valid procedure by staff success"""

        res = self.client.post(PROCEDURE_URL, self.payload, format='json')

        exists = models.Procedure.objects.filter(
            name=self.payload['name'].lower()
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'],
                         self.payload['name'].lower())
        self.assertEqual(res.data['speciality'],
                         self.payload['speciality'].lower())
        self.assertEqual(res.data['days_in_hospital'], None)
        self.assertEqual(res.data['days_in_destination'], None)
        self.assertEqual(res.data['duration_minutes'], None)
        self.assertEqual(res.data['overview'], self.payload['overview'])
        self.assertEqual(res.data['other_details'], '')

    def test_create_invalid_procedure_authenticated_staff_failure(self):
        """Test creating invalid procedure by staff failure"""
        payload = {'name': ''}

        res = self.client.post(PROCEDURE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_procedure_failure(self):
        """Test that creating duplicate procedure fails"""
        self.client.post(PROCEDURE_URL, self.payload, format='json')

        res = self.client.post(PROCEDURE_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_staff_delete_procedure_success(self):
        """Test that deleting procedure by staff is success"""
        res = self.client.post(PROCEDURE_URL, self.payload, format='json')

        url = get_item_url(res.data['id'])
        del_procedure = self.client.delete(url)

        procedure_exists = models.Procedure.objects.filter(
            name=self.payload['name'].lower()
        ).exists()

        self.assertEqual(del_procedure.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(procedure_exists)

    def test_staff_update_procedure_success(self):
        """Test that updating procedure by staff is success"""
        res = self.client.post(PROCEDURE_URL, self.payload, format='json')

        url = get_item_url(res.data['id'])
        new_payload = {
            'other_details': 'new details'
        }

        response = self.client.patch(url, new_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'],
                         self.payload['name'].lower())
        self.assertEqual(response.data['other_details'],
                         new_payload['other_details'])

    def test_staff_update_duplicate_procedure_fails(self):
        """Test that updating procedure by duplicate content fails"""
        res = self.client.post(PROCEDURE_URL, self.payload, format='json')
        second_payload = {
            'name': 'abc',
            'speciality': 'orthopedics',
            'overview': 'bla bla bla'
        }
        self.client.post(PROCEDURE_URL, second_payload, format='json')

        url = get_item_url(res.data['id'])
        new_payload = {
            'name': 'abc',
        }

        response = self.client.patch(url, new_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProcedureImageUploadTests(TestCase):
    """Tests for uploading procedure picture"""

    def setUp(self):
        """Setup for running all the tests"""
        self.staff = get_user_model().objects.create_doctor(
            email='temp@curesio.com',
            password='testpass@4',
            username='tempuser4'
        )
        self.staff.is_staff = True
        self.staff.save()
        self.staff.refresh_from_db()

        self.client = APIClient()
        self.client.force_authenticate(self.staff)

    def test_procedure_picture_upload(self):
        """Test that uploading procedure picture is successful"""
        image_upload_url = PROCEDURE_URL

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)

            payload = {
                'name': 'temp',
                'speciality': 'orthopedics',
                'image': ntf,
                'overview': 'bla bla bla'
            }

            res = self.client.post(
                image_upload_url,
                payload,
                format="multipart"
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)

    def test_user_profile_picture_invalid_image_fails(self):
        """Test that invalid image upload fails"""
        image_upload_url = PROCEDURE_URL

        payload = {
            'name': 'temp',
            'speciality': 'orthopedics',
            'image': 'invalid image',
            'overview': 'bla bla bla'
        }

        res = self.client.post(
            image_upload_url,
            payload,
            format="multipart"
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
