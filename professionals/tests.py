from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import Professional

User = get_user_model()


class ProfessionalAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)

        self.professional_data = {
            "social_name": "Maria Silva",
            "profession": "Psicóloga",
            "address": "Rua das Flores, 100",
            "contact": "21999999999",
        }

    def test_create_professional(self):
        url = reverse("professionals-list")

        response = self.client.post(
            url,
            self.professional_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 1)
        self.assertEqual(response.data["social_name"], "Maria Silva")

    def test_list_professionals(self):
        Professional.objects.create(**self.professional_data)

        url = reverse("professionals-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_professional(self):
        professional = Professional.objects.create(**self.professional_data)

        url = reverse(
            "professionals-detail",
            kwargs={"pk": professional.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["social_name"], "Maria Silva")

    def test_update_professional(self):
        professional = Professional.objects.create(**self.professional_data)

        updated_data = {
            "social_name": "Maria Santos",
            "profession": "Psicóloga",
            "address": "Avenida Central, 500",
            "contact": "21988888888",
        }

        url = reverse(
            "professionals-detail",
            kwargs={"pk": professional.id},
        )
        response = self.client.put(
            url,
            updated_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        professional.refresh_from_db()

        self.assertEqual(professional.social_name, "Maria Santos")
        self.assertEqual(professional.contact, "21988888888")

    def test_partial_update_professional(self):
        professional = Professional.objects.create(**self.professional_data)

        url = reverse(
            "professionals-detail",
            kwargs={"pk": professional.id},
        )
        response = self.client.patch(
            url,
            {"contact": "21977777777"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        professional.refresh_from_db()

        self.assertEqual(professional.contact, "21977777777")

    def test_delete_professional(self):
        professional = Professional.objects.create(**self.professional_data)

        url = reverse(
            "professionals-detail",
            kwargs={"pk": professional.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Professional.objects.count(), 0)

    def test_invalid_professional_data(self):
        url = reverse("professionals-list")

        invalid_data = {
            "social_name": "",
            "profession": "",
            "address": "",
            "contact": "",
        }

        response = self.client.post(
            url,
            invalid_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_request_is_rejected(self):
        self.client.force_authenticate(user=None)

        url = reverse("professionals-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)