# Generated by Django 4.2.5 on 2023-09-19 00:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("concertconnect", "0003_booking_booking_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="booking",
            old_name="booking_status",
            new_name="payment_status",
        ),
    ]
