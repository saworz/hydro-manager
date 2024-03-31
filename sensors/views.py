from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Measurement, Sensor, SensorTypes
from .serializers import SensorSerializer


class SensorCreateView(APIView):
    def post(self, request):
        data, error = self.clean(request.data)
        if error:
            return Response(data, status=error)

        user_systems = request.user.systems.all()
        system = user_systems.filter(id=data.get("system_id")).first()

        if not system:
            response_data = {
                "error": "INVALID_SYSTEM_ID",
                "error_message": "System with this ID does not exist or you don't have permission to access it",
                "system_id": data.get("system_id"),
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        sensor = Sensor.objects.create(
            system=system,
            sensor_type=data.get("sensor_type"),
            description=data.get("description"),
        )
        serializer = SensorSerializer(sensor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def clean(self, data: dict) -> (dict, int | None):
        system_id = data.get("system_id")
        if not system_id:
            response_data = {
                "error": "MISSING_SYSTEM_ID",
                "error_message": "Please provide id for the system to assign sensor to.",
            }
            return response_data, status.HTTP_400_BAD_REQUEST

        sensor_type = data.get("sensor_type")
        if not sensor_type:
            response_data = {
                "error": "MISSING_SENSOR_TYPE",
                "error_message": "Please provide sensor type",
            }
            return response_data, status.HTTP_400_BAD_REQUEST

        if not sensor_type.lower() in SensorTypes.values:
            response_data = {
                "error": "Invalid_SENSOR_TYPE",
                "error_message": "Please provide correct sensor type",
                "sensor_types": SensorTypes.values,
            }
            return response_data, status.HTTP_400_BAD_REQUEST

        cleaned_data = {
            "system_id": system_id,
            "sensor_type": sensor_type,
            "description": data.get("description"),
        }
        return cleaned_data, None


class SensorRemoveView(APIView):
    def delete(self, request, id):
        user_systems = request.user.systems.all()
        sensors = Sensor.objects.filter(system__in=user_systems)
        target_sensor = sensors.filter(id=id).first()

        if not target_sensor:
            response_data = {
                "error": "INVALID_ID",
                "error_message": "Sensor with this ID does not exist or you don't have permission to remove it.",
                "id": id,
            }
            return Response(response_data, status.HTTP_404_NOT_FOUND)

        target_sensor.delete()
        response_data = {"message": f"Sensor with id {id} has been deleted."}
        return Response(response_data, status=status.HTTP_200_OK)


class SensorListView(APIView):
    def get(self, request, id):
        user_systems = request.user.systems.all()
        target_system = user_systems.filter(id=id)
        if not target_system:
            response_data = {
                "error": "INVALID_ID",
                "errorMessage": "System with this ID doesn't exist or you don't have permission to access it.",
                "id": id,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        sensors = Sensor.objects.filter(system__in=target_system)
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MeasurementCreateView(APIView):
    def post(self, request, id):
        data, error = self.clean(request.data)
        if error:
            return Response(data, status=error)

        user_systems = request.user.systems.all()
        target_system = user_systems.filter(id=id)
        if not target_system:
            response_data = {
                "error": "INVALID_ID",
                "errorMessage": "System with this ID doesn't exist or you don't have permission to access it.",
                "id": id,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        sensors = Sensor.objects.filter(system__in=target_system)
        sensor = sensors.filter(id=data.get("sensor_id")).first()

        if not sensor:
            response_data = {
                "error": "INVALID_SENSOR_ID",
                "errorMessage": "Sensor with this ID doesn't exist in this system.",
                "sensor_id": data.get("sensor_id"),
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        Measurement.objects.create(sensor=sensor, value=data.get("value"))
        return Response(status=status.HTTP_201_CREATED)

    def clean(self, data: dict) -> (dict, int | None):
        sensor_id = data.get("sensor_id")
        if not sensor_id:
            error_data = {
                "error": "MISSING_SENSOR_ID",
                "errorMessage": "Please provide a valid sensor id for this system.",
            }
            return error_data, status.HTTP_400_BAD_REQUEST

        value = data.get("value")
        clean_data = {"sensor_id": sensor_id, "value": value}
        return clean_data, None
