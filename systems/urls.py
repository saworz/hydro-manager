from django.urls import path

from .views import (SystemCreateView, SystemDeleteView, SystemDetailView,
                    SystemListView, SystemUpdateView)

urlpatterns = [
    path("create/", SystemCreateView.as_view(), name="system-create"),
    path("detail/<int:id>/", SystemDetailView.as_view(), name="system-detail"),
    path("update/<int:id>/", SystemUpdateView.as_view(), name="system-update"),
    path("delete/<int:id>/", SystemDeleteView.as_view(), name="system-delete"),
    path("list/", SystemListView.as_view(), name="system-list"),
]
