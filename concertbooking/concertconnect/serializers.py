# from common.utils import convert_img_encoded
import base64
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import F
from rest_framework import serializers

from users.serializers import UserSerializer

# from rest_framework.validators import UniqueTogetherValidator
from .models import Booking, Concert, Tier


class TierManagementSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Tier

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Tier.objects.all(),
                fields=("name", "venue"),
                message="Tier name already exist for venue",
            )
        ]


class VenueSerializer(serializers.Serializer):
    def to_representation(self, instance):
        response = dict()
        response["venue_id"] = instance.id
        response["venue_nume"] = instance.name
        response["venue_address"] = instance.address
        response["tiers"] = {
            Tier.objects.filter(venue=instance.id)
            .annotate(
                total_seats=F("capacity"),
                available_seats=F("capacity")
                - Booking.objects.filter(
                    tier_id=instance.id, is_cancelled=False
                ).count(),
            )
            .values("id", "name", "total_seats", "available_seats", "price")
        }
        return response


class ConcertSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Concert

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Concert.objects.all(),
                fields=("concert_by", "launch_date"),
                message="Concert already exist for this date",
            ),
        ]

    def validate_launch_date(self, value):
        # as the value will be epoch from the interface..
        if (value - datetime.utcnow().date()) < timedelta(days=30):
            raise serializers.ValidationError(
                " Launch date must be at least one month after the current date"
            )

        return value

    def validate_venue(self, value):
        if Tier.objects.filter(venue=value).count() < 3:
            raise serializers.ValidationError("Choose Venue with atleast 3 tiers")

        return value

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["launch_date"] = datetime.combine(
            instance.launch_date, datetime.min.time()
        ).timestamp()

        response["created_on"] = instance.created_on.timestamp()
        response["venue"] = VenueSerializer(instance.venue).data
        response["concert_by"] = UserSerializer(instance.concert_by).data
        # response["concert_images"] = []

        # # converting the images related to concert into base64 encode to send to frontend.
        # fs = FileSystemStorage(settings.MEDIA_ROOT)
        # if fs:
        #     if fs.exists(str(instance.id)):
        #         for img in fs.listdir(str(instance.id) + "/")[1]:
        #             img_path = str(
        #                 settings.MEDIA_ROOT + str(instance.id) + "/" + img + "/"
        #             ).replace("\\", "/")
        #             with fs.open(img_path, "rb") as f:
        #                 img_data = f.read()
        #                 encoded_image = base64.b64encode(img_data).decode("utf-8")
        #                 response["concert_images"].append(encoded_image)
        return response


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Booking

    def validate_concert(self, value):
        if value.launch_date < datetime.utcnow().date():
            raise serializers.ValidationError(
                "Upcoming Concerts can only be selected.."
            )
        return value

    def validate(self, data):
        # print(data["tier"].venue_id, data["concert"].venue_id)
        # Edge case which is possible from payload manipulation
        if data["tier"].venue_id != data["concert"].venue_id:
            raise serializers.ValidationError("concert and tier venue should match")
        total_available_tickets = data["tier"].capacity - sum(
            Booking.objects.filter(tier=data["tier"], is_cancelled=False).values_list(
                "tickets", flat=True
            )
        )
        # print(total_available_tickets)
        if total_available_tickets < data["tickets"]:
            raise serializers.ValidationError(
                f" only {total_available_tickets} tickets available"
            )
        return data

    # def create(self,validated_data):

    #     print(validated_data)

    # def to_representation(self, instance):
    #     return super().to_representation(instance)
