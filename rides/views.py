# views.py
from rest_framework.views import APIView
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Ride, Booking
from .serializer import RideSerializer, BookingSerializer
from django.db.models import F
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

# Create a new ride
class RideCreateView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

# List and filter available rides
class RideListView(generics.ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    def get_queryset(self):
        rides = Ride.objects.filter(departure_time__gte=timezone.now())
        date = self.request.query_params.get('date')
        location = self.request.query_params.get('location')
        
        if date:
            rides = rides.filter(departure_time__date=date)
        if location:
            rides = rides.filter(departure_location__icontains=location) | rides.filter(destination__icontains=location)
        
        return rides

# Retrieve details of a specific ride
class RideDetailView(generics.RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

# Book a ride
class BookRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            ride = Ride.objects.get(pk=id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)
        
        seats_requested = request.data.get('seats_booked')
        if not seats_requested or seats_requested <= 0:
            return Response({"error": "Invalid number of seats requested"}, status=status.HTTP_400_BAD_REQUEST)

        if ride.available_seats < seats_requested:
            return Response({"error": "Not enough seats available"}, status=status.HTTP_400_BAD_REQUEST)

        existing_booking = Booking.objects.filter(user=request.user, ride=ride).exists()
        if existing_booking:
            return Response({"error": "You have already booked this ride"}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed to create the booking and update available seats
        booking = Booking.objects.create(user=request.user, ride=ride, seats_booked=seats_requested)
        ride.available_seats = F('available_seats') - seats_requested
        ride.save()

        booking_serializer = BookingSerializer(booking)
        return Response(booking_serializer.data, status=status.HTTP_201_CREATED)
    
    class RideListView(ListView):
       model = Ride
       template_name = 'rides/ride_list.html'
       context_object_name = 'rides'
    


