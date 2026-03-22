from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guests = models.PositiveSmallIntegerField()
    booking_date = models.DateTimeField()

    class Meta:
        ordering = ["booking_date"]

    def __str__(self):
        return f"{self.name} ({self.booking_date})"
