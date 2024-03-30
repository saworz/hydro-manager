from django.db import models

from systems.models import HydroSystem


class SensorTypes(models.TextChoices):
    PH = "ph"
    TEMPERATURE = "temperature"
    TDS = "tds"


class Sensor(models.Model):
    system = models.ForeignKey(
        HydroSystem, on_delete=models.CASCADE, related_name="sensor"
    )
    sensor_type = models.CharField(max_length=11, choices=SensorTypes.choices)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.sensor_type} sensor with ID {self.id} in system {self.system.id}"


class Measurement(models.Model):
    sensor = models.ForeignKey(
        Sensor, on_delete=models.CASCADE, related_name="measurement"
    )
    value = models.DecimalField(max_digits=5, decimal_places=2)
