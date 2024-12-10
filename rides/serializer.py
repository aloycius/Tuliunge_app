# serializers.py
from rest_framework import serializers
from .models import Ride, Booking

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'departure_location', 'destination', 'departure_time', 'available_seats', 'price']

class RideDetailSerializer(serializers.ModelSerializer):
    bookings = serializers.StringRelatedField(many=True)

    class Meta:
        model = Ride
        fields = ['id', 'departure_location', 'destination', 'departure_time', 'available_seats', 'price', 'bookings']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'ride', 'user', 'booked_at']
"""
class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'departure_location', 'destination', 'departure_time', 'available_seats', 'price']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'ride', 'seats_booked']
"""

