from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from restaurant.models import Booking, MenuItem


class MenuAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse("menuitem-list")
        self.user = User.objects.create_user(username="staff", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.item = MenuItem.objects.create(
            title="Bruschetta",
            price=Decimal("6.00"),
            inventory=15,
        )

    def test_anonymous_can_list_menu(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get("results", response.data)), 1)

    def test_anonymous_cannot_create_menu(self):
        response = self.client.post(
            self.list_url,
            {"title": "Pasta", "price": "14.00", "inventory": 5},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_can_create_menu(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            self.list_url,
            {"title": "Pasta", "price": "14.00", "inventory": 5},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_update_delete_require_auth_for_writes(self):
        detail_url = reverse("menuitem-detail", args=[self.item.pk])
        get_resp = self.client.get(detail_url)
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)

        self.assertEqual(
            self.client.put(
                detail_url,
                {"title": "Bruschetta", "price": "7.00", "inventory": 10},
                format="json",
            ).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        put_resp = self.client.put(
            detail_url,
            {"title": "Bruschetta", "price": "7.00", "inventory": 10},
            format="json",
        )
        self.assertEqual(put_resp.status_code, status.HTTP_200_OK)

        self.client.credentials()
        self.assertEqual(self.client.delete(detail_url).status_code, status.HTTP_401_UNAUTHORIZED)


class BookingAPITests(APITestCase):
    def setUp(self):
        self.url = reverse("booking-list")
        self.user = User.objects.create_user(username="booker", password="testpass123")
        self.token = Token.objects.create(user=self.user)

    def test_list_bookings_public(self):
        Booking.objects.create(
            name="Guest",
            no_of_guests=2,
            booking_date=timezone.now(),
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_booking_requires_auth(self):
        response = self.client.post(
            self.url,
            {
                "name": "New Guest",
                "no_of_guests": 3,
                "booking_date": timezone.now().isoformat(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            self.url,
            {
                "name": "New Guest",
                "no_of_guests": 3,
                "booking_date": timezone.now().isoformat(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserRegistrationAPITests(APITestCase):
    def test_register_user(self):
        url = reverse("user-register")
        response = self.client.post(
            url,
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "securepass1",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())
