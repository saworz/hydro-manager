from rest_framework import serializers

from sensors.serializers import MeasurementSerializer

from .models import HydroSystem


class HydroMeasurementsSerializer(serializers.ModelSerializer):
    newest_measurements = serializers.SerializerMethodField()

    def get_newest_measurements(self, obj):
        measurements = obj.get_last_ten_measurements()
        serializer = MeasurementSerializer(measurements, many=True)
        return serializer.data

    class Meta:
        model = HydroSystem
        fields = ["id", "owner", "description", "created_at", "newest_measurements"]


class HydroSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroSystem
        fields = "__all__"


class CreateSystemSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class ErrorMessageSerializer(serializers.Serializer):
    error = serializers.CharField()
    errorMessage = serializers.CharField()
    name = serializers.CharField()
