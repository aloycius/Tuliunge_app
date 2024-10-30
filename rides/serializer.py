from rest_framework import serializers
from .models import Ride, Booking

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'driver', 'departure_location', 'destination', 'departure_time', 'available_seats', 'price']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'ride', 'passenger', 'booked_on']
