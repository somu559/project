from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingListCreateView, MenuItemViewSet, UserRegisterView

router = DefaultRouter()
router.register(r"menu", MenuItemViewSet, basename="menuitem")

urlpatterns = [
    path("", include(router.urls)),
    path("bookings/", BookingListCreateView.as_view(), name="booking-list"),
    path("users/", UserRegisterView.as_view(), name="user-register"),
]
