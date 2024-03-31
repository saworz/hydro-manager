import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from systems.models import HydroSystem


@pytest.mark.django_db
class SystemDetailTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test_user", password="testpassword123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_correct_request(self):
        system = HydroSystem.objects.create(
            owner=self.user, name="test_system", description="test_description"
        )

        response = self.client.get(reverse("system-detail", kwargs={"id": system.id}))
        assert response.status_code == status.HTTP_200_OK
        response_data = json.loads(response.content.decode("utf-8"))

        expected_response = {
            "id": system.id,
            "owner": self.user.id,
            "name": "test_system",
            "description": "test_description",
            "created_at": system.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "newest_measurements": [],
        }

        assert response_data == expected_response

    def test_invalid_id_request(self):
        invalid_id = 999999
        response = self.client.get(reverse("system-detail", kwargs={"id": invalid_id}))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = json.loads(response.content.decode("utf-8"))

        expected_response = {
            "error": "INVALID_ID",
            "errorMessage": "System with this ID doesn't exist or you don't have permission to access it.",
            "id": invalid_id,
        }

        assert response_data == expected_response


@pytest.mark.django_db
class SystemCreateTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test_user", password="testpassword123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_correct_request(self):
        request_body = {
            "name": "test_system",
            "description": "test_description",
        }

        response = self.client.post(
            reverse("system-create"),
            data=json.dumps(request_body),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        response_data = json.loads(response.content.decode("utf-8"))

        system = HydroSystem.objects.filter(name="test_system").first()

        expected_response = {
            "id": system.id,
            "name": "test_system",
            "description": "test_description",
            "created_at": system.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "owner": self.user.id,
        }

        assert response_data == expected_response


@pytest.mark.django_db
class SystemListTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test_user", password="testpassword123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_correct_request(self):
        system = HydroSystem.objects.create(
            owner=self.user, name="test_system", description="test_description"
        )

        response = self.client.get(reverse("system-list"))
        assert response.status_code == status.HTTP_200_OK
        response_data = json.loads(response.content.decode("utf-8"))

        expected_response = [
            {
                "id": system.id,
                "owner": self.user.id,
                "name": "test_system",
                "description": "test_description",
                "created_at": system.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            }
        ]

        assert response_data == expected_response


@pytest.mark.django_db
class SystemDeleteTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test_user", password="testpassword123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_correct_request(self):
        system = HydroSystem.objects.create(
            owner=self.user, name="test_system", description="test_description"
        )

        response = self.client.delete(
            reverse("system-delete", kwargs={"id": system.id})
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = json.loads(response.content.decode("utf-8"))

        expected_response = {"message": f"System with id {system.id} has been deleted."}
        assert response_data == expected_response

    def test_invalid_id_request(self):
        invalid_id = 999999
        response = self.client.get(reverse("system-detail", kwargs={"id": invalid_id}))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = json.loads(response.content.decode("utf-8"))

        expected_response = {
            "error": "INVALID_ID",
            "errorMessage": "System with this ID doesn't exist or you don't have permission to access it.",
            "id": invalid_id,
        }

        assert response_data == expected_response
