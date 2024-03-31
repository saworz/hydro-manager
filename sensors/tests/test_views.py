import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from sensors.models import Sensor, SensorTypes
from systems.models import HydroSystem


@pytest.mark.django_db
class SensorAddTest(APITestCase):
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

        request_body = {
            "system_id": system.id,
            "sensor_type": "ph",
            "description": "description",
        }

        response = self.client.post(
            reverse("add-sensor"),
            data=json.dumps(request_body),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = json.loads(response.content.decode("utf-8"))
        sensor = system.sensor.first()

        expected_response = {
            "id": sensor.id,
            "sensor_type": "ph",
            "description": "description",
            "system": system.id,
        }

        assert response_data == expected_response

    def test_missing_system_id_request(self):
        request_body = {"sensor_type": "ph", "description": "description"}

        response = self.client.post(
            reverse("add-sensor"),
            data=json.dumps(request_body),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = json.loads(response.content.decode("utf-8"))

        expected_response = {
            "error": "MISSING_SYSTEM_ID",
            "error_message": "Please provide id for the system to assign sensor to.",
        }

        assert response_data == expected_response


class SensorRemoveTest(APITestCase):
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

        sensor = Sensor.objects.create(
            system=system, sensor_type=SensorTypes.PH, description="test_description"
        )

        response = self.client.delete(
            reverse("remove-sensor", kwargs={"id": sensor.id})
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = json.loads(response.content.decode("utf-8"))

        expected_response = {"message": f"Sensor with id {sensor.id} has been deleted."}

        assert response_data == expected_response

    def test_invalid_sensor_id_request(self):
        invalid_sensor_id = 999999
        response = self.client.delete(
            reverse("remove-sensor", kwargs={"id": invalid_sensor_id})
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = json.loads(response.content.decode("utf-8"))

        expected_response = {
            "error": "INVALID_ID",
            "error_message": "Sensor with this ID does not exist or you don't have permission to remove it.",
            "id": invalid_sensor_id,
        }

        assert response_data == expected_response
