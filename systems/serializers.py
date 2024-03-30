from rest_framework import serializers

from .models import HydroSystem


class HydroSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroSystem
        fields = "__all__"
