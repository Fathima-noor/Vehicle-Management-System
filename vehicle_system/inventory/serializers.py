
import re
from datetime import date

from django.db import transaction
from rest_framework import serializers

from .models import Vehicle, Booking


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"

    def validate_year(self, value):
        if value < 1886 or value > date.today().year + 1:
            raise serializers.ValidationError(
                "Enter a valid vehicle manufacturing year."
            )
        return value

    def validate_price_per_day(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price per day must be greater than zero."
            )
        return value


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["total_amount"]

    def validate_customer_phone(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )
        return value

    def validate(self, attrs):
        vehicle = attrs.get(
            "vehicle",
            getattr(self.instance, "vehicle", None)
        )
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None)
        )
        end_date = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None)
        )

        if start_date and start_date < date.today():
            raise serializers.ValidationError({
                "start_date": "Start date cannot be in the past."
            })

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date."
            })

        if vehicle and start_date and end_date:
            if not vehicle.is_available:
                raise serializers.ValidationError({
                    "vehicle": "This vehicle is marked unavailable."
                })

            overlapping = Booking.objects.filter(
                vehicle=vehicle,
                start_date__lt=end_date,
                end_date__gt=start_date,
            )

            if self.instance:
                overlapping = overlapping.exclude(
                    pk=self.instance.pk
                )

            if overlapping.exists():
                raise serializers.ValidationError({
                    "booking": (
                        "This vehicle is already booked "
                        "for the selected dates."
                    )
                })

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            vehicle = Vehicle.objects.select_for_update().get(
                pk=validated_data["vehicle"].pk
            )

            start_date = validated_data["start_date"]
            end_date = validated_data["end_date"]

            
            if not vehicle.is_available:
                raise serializers.ValidationError({
                    "vehicle": "This vehicle is marked unavailable."
                })

            overlapping = Booking.objects.filter(
                vehicle=vehicle,
                start_date__lt=end_date,
                end_date__gt=start_date,
            )

            if overlapping.exists():
                raise serializers.ValidationError({
                    "booking": (
                        "This vehicle is already booked "
                        "for the selected dates."
                    )
                })

            days = (end_date - start_date).days
            validated_data["vehicle"] = vehicle
            validated_data["total_amount"] = (
                days * vehicle.price_per_day
            )

            return Booking.objects.create(**validated_data)
