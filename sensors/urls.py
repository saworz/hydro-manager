from django.urls import path

from .views import MeasurementCreateView, SensorCreateView, SensorRemoveView

urlpatterns = [
    path("add/", SensorCreateView.as_view(), name="add-sensor"),
    path("remove/<int:id>/", SensorRemoveView.as_view(), name="remove-sensor"),
    path("measurement/", MeasurementCreateView.as_view(), name="new-measurement"),
]
