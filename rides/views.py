# views.py
from rest_framework.views import APIView
from django.views.generic import ListView
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics
from .models import Ride, Booking
from .serializer import RideSerializer, BookingSerializer
from django.db.models import F
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly



@require_POST  # Ensures that this view can only be accessed via POST requests
def book_ride(request, id):
    ride = get_object_or_404(Ride, id=id)
    
    # Extract the number of seats requested from the request body
    seats_requested = request.POST.get('seats')  # Make sure this matches the key in your request

    # Validate input
    if not seats_requested or not seats_requested.isdigit():
        return JsonResponse({"error": "Invalid number of seats requested."}, status=400)
    
    seats_requested = int(seats_requested)

    # Check if enough seats are available
    if seats_requested > ride.available_seats:
        return JsonResponse({"error": "Not enough seats available."}, status=400)
    
    # Update available seats
    ride.available_seats -= seats_requested
    ride.save()  # Save the updated ride

    # Return a success response
    return JsonResponse({"message": f"You have successfully booked {seats_requested} seat(s)!"}, status=200)
"""
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])  # Set your auth classes here
@permission_classes([IsAuthenticatedOrReadOnly])  # Or another appropriate permission class
def list_rides(request):
   #list
"""

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
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get(self, request, *args, **kwargs):
        # Add custom logic if needed
        return super().get(request, *args, **kwargs)

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
    
    """"
    class RideListView(ListView):
       model = Ride
       template_name = 'rides/ride_list.html'
       context_object_name = 'rides'
    """
    
    class RideListView(ListView):
     queryset = Ride.objects.all()
     serializer_class = RideSerializer
     authentication_classes = [SessionAuthentication, BasicAuthentication]
     permission_classes = [IsAuthenticatedOrReadOnly]

     def get_queryset(self):
        # Filtering logic by date and location
        return Ride.objects.filter(  # Example filter logic
            departure_location=self.request.query_params.get('departure_location'),
            date=self.request.query_params.get('date')
        )
    


    
    


