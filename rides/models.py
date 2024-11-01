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
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    driver = models.ForeignKey("Driver", on_delete=models.CASCADE)

class Booking(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)

class Driver(models.Model):
    # Define fields here, for example:
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    # other fields

