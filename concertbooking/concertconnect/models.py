from django.db import models

from users.models import User


class Venue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    # is_active=models.BooleanField(default=True)

    class Meta:
        db_table = "venues"

    def __str__(self):
        return self.name


class Tier(models.Model):
    name = models.CharField(max_length=50)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        db_table = "tiers"
        unique_together = ("name", "venue")

    def __str__(self):
        return f"{self.name} at {self.venue.name}"


class Concert(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    launch_date = models.DateField()
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name="concert_at"
    )
    concert_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="concert_artist"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    # is_active=models.BooleanField

    class Meta:
        db_table = "concerts"

    def __str__(self):
        return self.title


class Booking(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tier = models.ForeignKey(Tier, on_delete=models.DO_NOTHING)
    tickets = models.PositiveIntegerField()
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    booking_choices = ((PENDING, "PENDING"), (COMPLETED, "COMPLETED"))
    payment_status = models.CharField(
        choices=booking_choices, default=PENDING, max_length=15
    )
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        db_table = "bookings"
