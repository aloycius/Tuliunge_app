from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ride, Booking
from .serializer import RideSerializer, BookingSerializer

class RideListView(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

class RideDetailView(generics.RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

class BookRideView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ride = Ride.objects.get(id=kwargs['id'])
        if ride.available_seats > 0:
            ride.available_seats -= 1
            ride.save()
            Booking.objects.create(ride=ride, passenger=request.user)
            return Response({"message": "Booking successful"}, status=status.HTTP_201_CREATED)
        return Response({"message": "No seats available"}, status=status.HTTP_400_BAD_REQUEST)

