from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Ride(models.Model):
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    departure_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    available_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.departure_location} to {self.destination} at {self.departure_time}"
    
    def book_seat(self, number_of_seats):
        if number_of_seats > self.available_seats:
            raise ValueError("Not enough seats available.")
        self.available_seats -= number_of_seats
        self.save()

class Booking(models.Model):
    ride = models.ForeignKey(Ride,related_name='bookings', on_delete=models.CASCADE)
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ride', 'user')  # Prevent double booking
    
    def __str__(self):
        return f"Booking by {self.user.email} for Ride {self.ride.id}"
"""
class Driver(models.Model):
    # Define fields here, for example:
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    # other fields
"""

