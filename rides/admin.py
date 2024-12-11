from django.contrib import admin
from .models import Ride,Booking,User
#from django.conf import User

# Register your models here.

admin.site.register(Ride)
admin.site.register(User)
admin.site.register(Booking)
