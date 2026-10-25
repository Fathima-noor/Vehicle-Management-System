
from datetime import date

from django.utils.dateparse import parse_date

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from .models import Vehicle, Booking
from .serializers import VehicleSerializer, BookingSerializer


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all().order_by("id")
    serializer_class = VehicleSerializer

  
    filterset_fields = [
        "brand",
        "fuel_type",
        "is_available",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        start_value = self.request.query_params.get("start_date")
        end_value = self.request.query_params.get("end_date")

        
        if start_value or end_value:

            if not start_value or not end_value:
                raise ValidationError({
                    "dates": (
                        "Provide both start_date and end_date."
                    )
                })

            start_date = parse_date(start_value)
            end_date = parse_date(end_value)

            if not start_date or not end_date:
                raise ValidationError({
                    "dates": "Use YYYY-MM-DD date format."
                })

            if start_date < date.today():
                raise ValidationError({
                    "start_date": "Start date cannot be in the past."
                })

            if end_date <= start_date:
                raise ValidationError({
                    "end_date": (
                        "End date must be after start date."
                    )
                })

            booked_vehicle_ids = Booking.objects.filter(
                start_date__lt=end_date,
                end_date__gt=start_date,
            ).values_list("vehicle_id", flat=True)

            queryset = queryset.filter(
                is_available=True
            ).exclude(
                id__in=booked_vehicle_ids
            )

        return queryset


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.select_related(
        "vehicle"
    ).all().order_by("-id")

    serializer_class = BookingSerializer


class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.select_related(
        "vehicle"
    ).all()

    serializer_class = BookingSerializer
