from django.urls import path

from .views import (MeasurementCreateView, SensorCreateView, SensorListView,
                    SensorRemoveView)

urlpatterns = [
    path("add/", SensorCreateView.as_view(), name="add-sensor"),
    path("remove/<int:id>/", SensorRemoveView.as_view(), name="remove-sensor"),
    path("list/<int:id>/", SensorListView.as_view(), name="list-sensors"),
    path(
        "measurement/<int:id>/", MeasurementCreateView.as_view(), name="new-measurement"
    ),
]
