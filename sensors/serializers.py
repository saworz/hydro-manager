from rest_framework import serializers

from .models import Measurement, Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"


class AddSensorSerializer(serializers.Serializer):
    system_id = serializers.IntegerField()
    sensor_type = serializers.CharField()
    description = serializers.CharField()


class AddMeasurementSerializer(serializers.Serializer):
    sensor_id = serializers.IntegerField()
    value = serializers.DecimalField(max_digits=5, decimal_places=2)
