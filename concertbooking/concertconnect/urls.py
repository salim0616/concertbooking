from django.urls import path

from .views import (BookingMangement, Concertdetail, ConcertManagement,
                    TierMangement, VenueMangement,)#Booking)

urlpatterns = [
    path("venues/", VenueMangement.as_view(), name="venues"),
    path("tiers/", TierMangement.as_view(), name="tiers"),
    path("concerts/", ConcertManagement.as_view(), name="concerts"),
    path("concert/<int:pk>", Concertdetail, name="concert"),
    path("bookings/", BookingMangement.as_view(), name="bookings"),
    path("bookings/<int:pk>", BookingMangement.as_view(), name="bookings"),


    # path("booking/<int:pk>",Booking.as_view(),name="booking"),
]
