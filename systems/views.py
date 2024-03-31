from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import MessageSerializer

from .models import HydroSystem
from .serializers import (CreateSystemSerializer, ErrorMessageSerializer,
                          HydroMeasurementsSerializer, HydroSystemSerializer)


class SystemCreateView(APIView):
    """Create new hydro system for authenticated user."""

    serializer_class = CreateSystemSerializer

    @extend_schema(
        responses={201: HydroSystemSerializer, 400: ErrorMessageSerializer},
    )
    def post(self, request):
        data, error = self.clean(request.data)
        if error:
            return Response(data, status=error)

        system, created = HydroSystem.objects.get_or_create(
            owner=request.user,
            name=data["name"],
            defaults={"description": data["description"]},
        )

        if not created:
            response_data = {
                "error": "INVALID_NAME",
                "errorMessage": "System with this name already exists.",
                "name": data["name"],
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = HydroSystemSerializer(system)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def clean(self, data: dict) -> (dict, int | None):
        name = data.get("name")
        if not name:
            error_data = {
                "error": "MISSING_NAME",
                "errorMessage": "Please provide a name for your system.",
            }
            return error_data, status.HTTP_400_BAD_REQUEST

        description = data.get("description")

        cleaned_data = {"name": name, "description": description}
        return cleaned_data, None


class SystemDetailView(APIView):
    """Get system's details for specified system id."""

    serializer_class = None

    @extend_schema(
        responses={
            200: HydroMeasurementsSerializer,
            400: ErrorMessageSerializer,
            404: ErrorMessageSerializer,
        },
    )
    def get(self, request, id):
        user_systems = request.user.systems.all()
        system = user_systems.filter(id=id).first()

        if not system:
            response_data = {
                "error": "INVALID_ID",
                "errorMessage": "System with this ID doesn't exist or you don't have permission to access it.",
                "id": id,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = HydroMeasurementsSerializer(system)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SystemUpdateView(APIView):
    """Update an existing system's data."""

    serializer_class = None

    @extend_schema(
        responses={
            200: HydroSystemSerializer,
            400: ErrorMessageSerializer,
            404: ErrorMessageSerializer,
        },
    )
    def patch(self, request, id):
        user_systems = request.user.systems.all()
        system = user_systems.filter(id=id).first()

        if not system:
            response_data = {
                "error": "INVALID_ID",
                "errorMessage": "System with this ID doesn't exist or you don't have permission to access it.",
                "id": id,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get("name")
        if name:
            if user_systems.filter(name=name):
                response_data = {
                    "error": "INVALID_NAME",
                    "errorMessage": "System with this name already exists.",
                    "name": name,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            system.name = name

        if request.data.get("description"):
            system.description = request.data.get("description")

        system.save()
        serializer = HydroSystemSerializer(system)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SystemDeleteView(APIView):
    """Delete an existing user's system."""

    serializer_class = None

    @extend_schema(
        responses={
            200: MessageSerializer,
            400: ErrorMessageSerializer,
            404: ErrorMessageSerializer,
        },
    )
    def delete(self, request, id):
        user_systems = request.user.systems.all()
        system = user_systems.filter(id=id).first()

        if not system:
            response_data = {
                "error": "INVALID_ID",
                "errorMessage": "System with this ID doesn't exist or you don't have permission to access it.",
                "id": id,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        system.delete()
        response_data = {"message": f"System with id {id} has been deleted."}
        return Response(response_data, status=status.HTTP_200_OK)


class SystemListView(APIView):
    """List all systems that belong to the authenticated user."""

    serializer_class = None

    @extend_schema(
        responses={
            200: HydroSystemSerializer(many=True),
        },
    )
    def get(self, request):
        user_systems = request.user.systems.all()
        serializer = HydroSystemSerializer(user_systems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
