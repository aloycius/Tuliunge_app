# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ride, Booking
from .serializer import RideSerializer, RideDetailSerializer, BookingSerializer

# POST /api/rides - Create a new ride
class RideCreateView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

# GET /api/rides - List available rides (with optional filters)
class RideListView(generics.ListAPIView):
    serializer_class = RideSerializer

    def get_queryset(self):
        queryset = Ride.objects.all()
        departure_location = self.request.query_params.get('departure_location')
        destination = self.request.query_params.get('destination')
        date = self.request.query_params.get('date')

        if departure_location:
            queryset = queryset.filter(departure_location__icontains=departure_location)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if date:
            queryset = queryset.filter(departure_time__date=date)

        return queryset

# GET /api/rides/{id} - Get ride details
class RideDetailView(generics.RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideDetailSerializer

# POST /api/rides/{id}/book - Book a ride
class RideBookingView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ride_id = kwargs.get('id')
        ride = Ride.objects.filter(id=ride_id).first()

        if not ride:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)

        if ride.available_seats < 1:
            return Response({"error": "No seats available"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already booked this ride
        if Booking.objects.filter(ride=ride, user=request.user).exists():
            return Response({"error": "You have already booked this ride"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a booking
        booking = Booking.objects.create(ride=ride, user=request.user)
        ride.available_seats -= 1
        ride.save()

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

"""
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

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])  # Set your auth classes here
@permission_classes([IsAuthenticatedOrReadOnly])  # Or another appropriate permission class
def list_rides(request):
   #list
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
    
    
    class RideListView(ListView):
       model = Ride
       template_name = 'rides/ride_list.html'
       context_object_name = 'rides'
    

    
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
"""  


    
    


