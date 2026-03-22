from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from restaurant.models import Booking, MenuItem


class MenuItemModelTests(TestCase):
    def test_create_menu_item(self):
        item = MenuItem.objects.create(
            title="Greek Salad",
            price=Decimal("12.50"),
            inventory=20,
        )
        self.assertEqual(str(item), "Greek Salad")
        self.assertEqual(item.inventory, 20)


class BookingModelTests(TestCase):
    def test_create_booking(self):
        when = timezone.now()
        booking = Booking.objects.create(
            name="Ada Lovelace",
            no_of_guests=4,
            booking_date=when,
        )
        self.assertIn("Ada Lovelace", str(booking))
        self.assertEqual(booking.no_of_guests, 4)
