import logging
import os
import uuid

# from django.core.exceptions import ValidationError
from datetime import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from common.utils import dummy_payment_api, response_generator

from .models import Booking, Concert, Tier, Venue
from .serializers import BookingSerializer, ConcertSerilizer, TierManagementSerializer

"""
    Venue manageement and tier management will done by the host company or
    owners of venue.
    Before starting Please creating venue and tiers for that venue.

"""


class VenueMangement(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]

    """
        venue related info was not their in requirement but still
        based on the design it has been introduced.
        There is no validation for this as this not much focused in requirment. 
    
    """

    def get(self, request):
        """
        this get request can be used to list all the venues and
        used in drpdown to select the venue.
        """

        try:
            venues_query = Venue.objects.all().values()
            return response_generator(status.HTTP_200_OK, venues_query)

        except Exception as e:
            logging.exception("Exceptions Occured in Venue Listing {}".format(e))
            return response_generator(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
            )

    def create(self, request):
        try:
            data = {
                "name": request.data.get("venue_name"),
                "address": request.data.get("address"),
            }
            Venue.objects.create(**data)
            return response_generator(
                status.HTTP_201_CREATED, "Successfully Created Venue"
            )

        except Exception as e:
            logging.exception("Exceptions Occured during Venue Creation {}".format(e))
            return response_generator(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
            )


class TierMangement(generics.CreateAPIView):
    http_method_names = ["post"]

    def create(self, request):
        try:
            data = {
                "name": request.data.get("tier_name"),
                "venue": request.data.get("venue_id"),
                "capacity": request.data.get("capacity"),
                "price": request.data.get("price"),
            }
            tier_serializer = TierManagementSerializer(data=data)
            if not tier_serializer.is_valid():
                return response_generator(
                    status.HTTP_400_BAD_REQUEST, tier_serializer.errors
                )
            tier_serializer.save()
            return response_generator(
                status.HTTP_201_CREATED, "Successfully Created Tier in Venu"
            )

        except Exception as e:
            logging.exception("Exceptions Occured is {}".format(e))
            return response_generator(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
            )


class ConcertManagement(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    # print(authentication_classes)
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ConcertSerilizer

    def get_queryset(self):
        try:
            # print(self.request.user.is_authenticated)
            query = Q(launch_date__gte=timezone.now())
            if self.request.user.is_authenticated and self.request.user.is_artist:
                query = query & Q(
                    concert_by=self.request.user,
                )

            return Concert.objects.select_related("venue").filter(query)
        except Exception as e:
            logging.exception("Exceptions Occured is {}".format(e))
            return response_generator(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
            )

    def post(self, request):
        try:
            # print(request.data)
            if not request.user.is_artist:
                return response_generator(status.HTTP_403_FORBIDDEN, "Invalid Action")

            concert_data = {
                "title": request.data.get("title"),
                "description": request.data.get("description"),
                "launch_date": datetime.fromtimestamp(
                    int(request.data.get("launch_date"))
                ).date(),
                "venue": request.data.get("venue_id"),
            }
            concert_data["concert_by"] = request.user.id

            concert_serilzer = ConcertSerilizer(data=concert_data)
            if not concert_serilzer.is_valid():
                return response_generator(
                    status.HTTP_400_BAD_REQUEST, concert_serilzer.errors
                )
            concert_obj = concert_serilzer.save()
            # if images were uploaded then those will be stored.
            images = request.data.getlist("concertimages", [])

            if images:
                fs = FileSystemStorage(settings.MEDIA_ROOT + str(concert_obj.id) + "/")
                for img in images:
                    img.name = str(uuid.uuid4()) + os.path.splitext(str(img))[1]
                    fs.save(img.name, img)

            return response_generator(
                status.HTTP_201_CREATED, "Concert has hosted successfully"
            )
        except Exception as e:
            logging.exception("Exceptions Occured is {}".format(e))
            return response_generator(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
            )


@api_view(["get"])
def Concertdetail(self, pk):
    concert_obj = get_object_or_404(Concert, pk=pk)
    data = ConcertSerilizer(concert_obj).data
    return response_generator(status.HTTP_200_OK, data)


class BookingMangement(APIView):
    authentication_classes = [JWTAuthentication]

    # def get_queryset(self):

    def get(self, request):
        # query=Q(,user=request.user)
        # print(pk)
        data = BookingSerializer(
            Booking.objects.select_related().filter(user=request.user), many=True
        ).data

        return response_generator(status.HTTP_200_OK, data)

    def post(self, request):
        print(request.data.get("concert_id"))
        booking_data = {
            "concert": request.data.get("concert_id"),
            "user": self.request.user.id,
            "tier": request.data.get("tier_id"),
            "tickets": request.data.get("tickets", 0),
        }
        booking_serializer = BookingSerializer(data=booking_data)
        if not booking_serializer.is_valid():
            return response_generator(
                status.HTTP_400_BAD_REQUEST, booking_serializer.errors
            )
        with transaction.atomic():
            booking_obj = booking_serializer.save()
            payment_status = dummy_payment_api()
            if payment_status:
                Booking.objects.filter(id=booking_obj.id).select_for_update().update(
                    payment_status="COMPLETED"
                )
                return response_generator(
                    status.HTTP_200_OK, "Ticket has been sucessfully Booked"
                )

            else:
                booking_obj.delete()
                return response_generator(status.HTTP_400_BAD_REQUEST, "Booking Failed")

        # booking_serializer.save()

    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return response_generator(
                status.HTTP_404_NOT_FOUND, "Invalid Object Reference"
            )

        if booking.concert.launch_date <= datetime.utcnow().date():
            return response_generator(
                status.HTTP_400_BAD_REQUEST, "Ticket Cannot be cancelled"
            )

        booking.is_cancelled = True
        booking.save()
        return response_generator(
            status.HTTP_200_OK, "Ticket has been sucessfully cancelled"
        )
