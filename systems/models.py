from django.db import models

from sensors.models import Measurement, Sensor
from users.models import User


class HydroSystem(models.Model):
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="systems"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_last_ten_measurements(self) -> list[Measurement]:
        sensors = Sensor.objects.filter(system=self)
        measurements = Measurement.objects.filter(sensor__in=sensors).order_by(
            "measured_at"
        )
        return measurements[:10]

    def __str__(self):
        return f"System with ID {self.id} owned by {self.owner}"

    class Meta:
        unique_together = ["owner", "name"]
