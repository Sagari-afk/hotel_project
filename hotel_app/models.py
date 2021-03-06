import string

from django.db import models
from random import choices


class City(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title


class Hotel(models.Model):
    title = models.CharField(max_length=30, unique=True)
    city = models.ForeignKey(
        "City",
        on_delete=models.CASCADE,
        related_name="hotels",
    )

    class Meta:
        unique_together = "title", "city"

    def get_rooms_beds(self):
        rooms_by_beds = {}
        rooms = self.rooms.all()
        for room in rooms:
            rooms_by_beds[room.beds] = rooms_by_beds.setdefault(room.beds, 0) + 1
        return rooms_by_beds

    def __str__(self):
        return f"{self.city}:{self.title}"


class Room(models.Model):
    room_number = models.IntegerField()
    beds = models.IntegerField()
    hotel = models.ForeignKey(
        "Hotel",
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    class Meta:
        unique_together = "hotel", "room_number"


class Booking(models.Model):
    booking_id_length = 4
    booking_id = models.CharField(max_length=booking_id_length)
    guest_name = models.CharField(max_length=120)
    persons = models.IntegerField()
    booking_start = models.DateField()
    booking_end = models.DateField()
    price = models.FloatField(default=0.0)
    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    @staticmethod
    def generate_booking_id():
        n = Booking.booking_id_length
        return "".join(choices(string.ascii_uppercase + string.digits, k=n))
