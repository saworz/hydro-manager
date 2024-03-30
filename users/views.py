from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.serializers import UserLoginSerializer, UserSerializer


class UserRegisterView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {"message": "User created successfully."}
        return Response(response_data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    permission_classes = []
    authentication_classes = []

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
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        logout(request)
        response_data = {"message": "User logged out."}
        return Response(response_data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self, request):
        response_data = {"id": request.user.id, "username": request.user.username}
        return Response(response_data, status=status.HTTP_200_OK)
