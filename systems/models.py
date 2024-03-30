from django.db import models

from users.models import User


class HydroSystem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="systems")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def last_update(self):
        pass

    def __str__(self):
        return f"System with ID {self.id} owned by {self.owner}"

    class Meta:
        unique_together = ["owner", "name"]
