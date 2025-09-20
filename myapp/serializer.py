from rest_framework import serializers
from .models import Perfil, Casa
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = "__all__"


class CasaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casa
        fields = "__all__"


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
