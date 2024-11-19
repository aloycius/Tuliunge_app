from django.contrib import admin
from .models import Ride, Driver, Booking
# Register your models here.


admin.site.register(Ride)
admin.site.register(Driver)
admin.site.register(Booking)
