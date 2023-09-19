import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email Already Exist!",
                lookup="iexact",
            )
        ]
    )
    password = serializers.CharField()
    is_artist = serializers.BooleanField(default=0)

    class Meta:
        fields = ("name", "email", "password", "is_artist")

    def validate_password(self, value):
        # if len(value)<8:
        #     raise serializers.ValidationError('Minimum 8 character length')
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&_-]{8,}$"
        )
        if not re.fullmatch(pattern, value):
            raise serializers.ValidationError(
                "At least 8 characters long,one lowercase letter,one upper case,one digit,one special character"
            )
        return value

    def create(self, validated_data):
        validated_data["email"] = validated_data["email"].lower()
        validated_data["password"] = make_password(validated_data["password"])
        user = User(**validated_data)
        user.save()
        return user

    # def to_representation(self, instance):
    #     response=super().to_representation(instance)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "is_artist")
        model = User
