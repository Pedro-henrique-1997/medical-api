from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from professionals.models import Professional

from .models import Appointment

User = get_user_model()


class AppointmentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)

        self.professional = Professional.objects.create(
            social_name="João da Silva",
            profession="Médico",
            address="Rua das Flores, 100",
            contact="21999999999",
        )

        self.appointment_data = {
            "date": "2026-09-01T14:30:00Z",
            "professional": str(self.professional.id),
        }

    def test_create_appointment(self):
        url = reverse("appointments-list")

        response = self.client.post(
            url,
            self.appointment_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(
            str(response.data["professional"]),
            str(self.professional.id),
        )

    def test_list_appointments(self):
        Appointment.objects.create(
            date=timezone.now(),
            professional=self.professional,
        )

        url = reverse("appointments-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_appointment(self):
        appointment = Appointment.objects.create(
            date=timezone.now(),
            professional=self.professional,
        )

        url = reverse(
            "appointments-detail",
            kwargs={"pk": appointment.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            str(response.data["professional"]),
            str(self.professional.id),
        )

    def test_update_appointment(self):
        appointment = Appointment.objects.create(
            date=timezone.now(),
            professional=self.professional,
        )

        updated_data = {
            "date": "2026-09-02T16:00:00Z",
            "professional": str(self.professional.id),
        }

        url = reverse(
            "appointments-detail",
            kwargs={"pk": appointment.id},
        )
        response = self.client.put(
            url,
            updated_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.date.isoformat(),
            "2026-09-02T16:00:00+00:00",
        )

    def test_partial_update_appointment(self):
        appointment = Appointment.objects.create(
            date=timezone.now(),
            professional=self.professional,
        )

        url = reverse(
            "appointments-detail",
            kwargs={"pk": appointment.id},
        )
        response = self.client.patch(
            url,
            {"date": "2026-09-03T10:00:00Z"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.date.isoformat(),
            "2026-09-03T10:00:00+00:00",
        )

    def test_delete_appointment(self):
        appointment = Appointment.objects.create(
            date=timezone.now(),
            professional=self.professional,
        )

        url = reverse(
            "appointments-detail",
            kwargs={"pk": appointment.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_invalid_professional(self):
        url = reverse("appointments-list")

        invalid_data = {
            "date": "2026-09-01T14:30:00Z",
            "professional": "00000000-0000-0000-0000-000000000000",
        }

        response = self.client.post(
            url,
            invalid_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("professional", response.data)

    def test_invalid_date(self):
        url = reverse("appointments-list")

        invalid_data = {
            "date": "isso-nao-e-uma-data",
            "professional": str(self.professional.id),
        }

        response = self.client.post(
            url,
            invalid_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)

    def test_missing_required_data(self):
        url = reverse("appointments-list")

        response = self.client.post(
            url,
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)
        self.assertIn("professional", response.data)

    def test_filter_appointments_by_professional(self):
        other_professional = Professional.objects.create(
            social_name="Ana Souza",
            profession="Nutricionista",
            address="Avenida Central, 200",
            contact="21988888888",
        )

        Appointment.objects.create(
            date=timezone.now(),
            professional=self.professional,
        )
        Appointment.objects.create(
            date=timezone.now(),
            professional=other_professional,
        )

        url = reverse("appointments-list")
        response = self.client.get(
            url,
            {"professional": str(self.professional.id)},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            str(response.data[0]["professional"]),
            str(self.professional.id),
        )    

    def test_unauthenticated_request_is_rejected(self):
        self.client.force_authenticate(user=None)

        url = reverse("appointments-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)