# serializers.py
from rest_framework import serializers
from .models import Ride, Booking

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'departure_location', 'destination', 'departure_time', 'available_seats', 'price']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'ride', 'seats_booked']

