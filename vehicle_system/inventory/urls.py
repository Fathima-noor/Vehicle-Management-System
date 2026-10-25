from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    VehicleViewSet,
    BookingListCreateView,
    BookingDetailView,
)

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicle")

urlpatterns = [
    path("", include(router.urls)),
    path("bookings/", BookingListCreateView.as_view(),
         name="booking-list-create"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(),
         name="booking-detail"),
]