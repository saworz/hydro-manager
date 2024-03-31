from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.serializers import UserLoginSerializer, UserRegisterSerializer


class UserRegisterView(APIView):
    """Register new user with username and password."""

    permission_classes = []
    authentication_classes = []

    @extend_schema(
        request=UserRegisterSerializer,
        responses={
            200: inline_serializer(
                name="RegisterValidResponse",
                fields={
                    "message": serializers.CharField(
                        default="User created successfully."
                    ),
                },
            ),
            400: inline_serializer(
                name="RegisterInvalidResponse",
                fields={
                    "username": serializers.ListField(
                        child=serializers.CharField(
                            default="user with this username already exists."
                        )
                    )
                },
            ),
        },
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {"message": "User created successfully."}
        return Response(response_data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    """Login user with username and password."""

    permission_classes = []
    authentication_classes = []

    @extend_schema(
        request=UserLoginSerializer,
        responses={
            200: inline_serializer(
                name="LoginValidResponse",
                fields={
                    "message": serializers.CharField(default="Login successful."),
                    "user": inline_serializer(
                        name="User",
                        fields={
                            "id": serializers.IntegerField(default=1),
                            "username": serializers.CharField(default="test_user"),
                        },
                    ),
                    "jwt_access_token": serializers.CharField(default="jwt_access"),
                    "jwt_refresh_token": serializers.CharField(default="jwt_refresh"),
                },
            ),
            400: inline_serializer(
                name="LoginInvalidResponse",
                fields={
                    "message": serializers.CharField(
                        default="Missing username or password."
                    ),
                },
            ),
        },
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = authenticate(
                username=validated_data["username"], password=validated_data["password"]
            )

            if not user:
                response_data = {"message": "Invalid username or password."}
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

            user_data = {
                "id": user.pk,
                "username": user.username,
            }

            login(request, user)
            jwt_access_token = str(AccessToken.for_user(user))
            jwt_refresh_token = str(RefreshToken.for_user(user))
            response_data = {
                "message": "Login successful",
                "user": user_data,
                "jwt_access_token": jwt_access_token,
                "jwt_refresh_token": jwt_refresh_token,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            {"message": "Missing username or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLogoutView(APIView):
    """Logout currently authenticated user."""

    permission_classes = []
    authentication_classes = []
    serializer_class = None

    @extend_schema(
        responses={
            200: inline_serializer(
                name="LogoutValidResponse",
                fields={
                    "message": serializers.CharField(default="User logged out."),
                },
            )
        }
    )
    def post(self, request):
        logout(request)
        response_data = {"message": "User logged out."}
        return Response(response_data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """Get currently authenticated user's details."""

    serializer_class = None

    @extend_schema(
        responses={
            200: inline_serializer(
                name="UserDetailValidResponse",
                fields={
                    "id": serializers.IntegerField(default=1),
                    "username": serializers.CharField(default="test_user"),
                },
            ),
        }
    )
    def get(self, request):
        response_data = {"id": request.user.id, "username": request.user.username}
        return Response(response_data, status=status.HTTP_200_OK)
