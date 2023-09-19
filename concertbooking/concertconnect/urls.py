from django.urls import path

from .views import (BookingMangement, Concertdetail, ConcertManagement,
                    TierMangement, VenueMangement)

urlpatterns = [
    path("venues/", VenueMangement.as_view(), name="venues"),
    path("tiers/", TierMangement.as_view(), name="tiers"),
    path("concerts/", ConcertManagement.as_view(), name="concerts"),
    path("concert/<int:pk>", Concertdetail, name="concert"),
    path("bookings/", BookingMangement.as_view(), name="bookings"),
]
