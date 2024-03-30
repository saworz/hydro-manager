from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user_instance = self.Meta.model(**validated_data)
        if password is not None:
            user_instance.set_password(password)
        user_instance.save()
        return user_instance

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
