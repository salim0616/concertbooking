# from django.shortcuts import render
import logging

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from common.utils import response_generator
from users.models import User
from users.serializers import RegisterSerializer

# import stripe


@api_view(["post"])
@permission_classes([AllowAny])
def register(request):
    try:
        registerserializer = RegisterSerializer(data=request.data)
        if not registerserializer.is_valid():
            return response_generator(
                status.HTTP_400_BAD_REQUEST, registerserializer.errors
            )
        registerserializer.save()
        return response_generator(status.HTTP_200_OK, "Successfully Registered")

    except Exception as e:
        logging.exception("Exceptions Occured is {}".format(e))
        return response_generator(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
        )


@api_view(["post"])
@permission_classes([AllowAny])
def login(request):
    try:
        """

        generating new token on each login request.
        The logic here was one login should have only token working at a time.
        As concurrent sessions are not enabled.

        """
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if not user:
            return response_generator(
                status.HTTP_401_UNAUTHORIZED, "Invalid Credentials.."
            )
        token_data = RefreshToken.for_user(user)
        user.last_login = timezone.now()
        user.save()

        data = {"access_key": str(token_data.access_token)}
        return response_generator(status.HTTP_200_OK, data)

    except Exception as e:
        logging.exception("Exceptions Occured is {}".format(e))

        return response_generator(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
        )
