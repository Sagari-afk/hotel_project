from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from hotel_app.models import (
    Hotel,
    Booking,
    City
)

from hotel_app.utils.common import find_room


class HotelSerializer(serializers.ModelSerializer):
    rooms_bed = serializers.ReadOnlyField(source="get_rooms_beds")
    city = serializers.CharField(source="city.title")

    class Meta:
        model = Hotel
        fields = ("title", "city", "rooms_bed")


class BookingSerializer(serializers.ModelSerializer):
    city = serializers.CharField(read_only=True)
    hotel = serializers.CharField(read_only=True)
    booking_id = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = (
            "booking_id",
            "guest_name",
            "booking_start",
            "booking_end",
            "city",
            "hotel",
            "persons",
        )

    @staticmethod
    def get_hotel(city, hotel):
        try:
            city = City.objects.get(title=city)
            hotel = city.hotels.get(title=hotel)
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError(
                {"error": f"{city}:{hotel} - {e}"}
            )
        print(f"Hotel Detected {hotel}")
        return hotel

    # First
    def to_internal_value(self, data):
        print(f"Raw Booking data: {data}")
        self.hotel = self.get_hotel(data.get("city"), data.get("hotel"))
        internal_data = super().to_internal_value(data)
        print(f"Internal Booking Data: {internal_data}")
        return internal_data

    def create(self, validated_data):
        print(f"Validated Data: {validated_data}")
        booking_start = validated_data.pop("booking_start")
        booking_end = validated_data.pop("booking_end")
        persons = validated_data.pop("persons")
        room = find_room(persons, booking_start, booking_end, self.hotel)
        print(f"ROOM from find_room method: {room}")
        booking = Booking.objects.create(
            guest_name=validated_data.pop("guest_name"),
            persons=persons,
            booking_start=booking_start,
            booking_end=booking_end,
            room=room,
        )
        booking.booking_id = booking.generate_booking_id()
        print(f"Booking Instance: {booking}")
        return booking
