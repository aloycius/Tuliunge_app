from django.test import TestCase

# Create your tests here.
# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Ride, Booking
from django.utils import timezone
from datetime import timedelta
from rides.models import Driver, Ride

User = get_user_model()

class RideManagementTests(APITestCase):
    
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(email="testuser@example.com", password="testpassword", 
                                             name="Test User", phone_number="1234567890")
        self.client.login(email="testuser@example.com", password="testpassword")

        # Create a driver object if it's required by the Ride model.
        self.driver1 = Driver.objects.create(
            name="John Doe",
            license_number="XYZ12345" 
            # Add any other required fields here
        )
        
        # Create sample rides
        self.ride1 = Ride.objects.create(
            driver = self.driver1,
            departure_location="City A",
            destination="City B",
            departure_time=timezone.now() + timedelta(days=1),
            available_seats=3,
            date=timezone.now(),
            price=15.0
        )

        self.ride2 = Ride.objects.create(
            departure_location="City C",
            destination="City D",
            departure_time=timezone.now() + timedelta(days=2),
            available_seats=5,
            date=timezone.now(),
            price=20.0,
            driver = self.driver1  # Assign the created driver here
        )

    def test_create_ride(self):
        """Test creating a new ride."""
        url = reverse('create_ride')
        data = {
            "departure_location": "City E",
            "destination": "City F",
            "departure_time": (timezone.now() + timedelta(days=3)).isoformat(),
            "available_seats": 4,
            "price": 25.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ride.objects.count(), 3)  # 2 initial rides + 1 new

    def test_list_rides(self):
        """Test listing available rides."""
        url = reverse('rides:list_rides')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 initial rides

    def test_list_rides_with_filter(self):
        """Test filtering rides by date and location."""
        url = reverse('rides:list_rides')
        
        # Filter by location
        response = self.client.get(url, {'location': 'City A'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only ride1 should match

        # Filter by date
        target_date = (timezone.now() + timedelta(days=1)).date().isoformat()
        response = self.client.get(url, {'date': target_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only ride1 should match

    def test_ride_detail(self):
        """Test retrieving details of a specific ride."""
        ##url = reverse('ride_detail', kwargs={'pk': self.ride1.pk})
        url = reverse('rides:ride_detail', kwargs={'pk': self.ride1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['departure_location'], "City A")

    def test_book_ride_success(self):
        """Test booking a ride with available seats."""
        url = reverse('book_ride', kwargs={'id': self.ride1.pk})
        data = {"seats_booked": 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.ride1.refresh_from_db()
        self.assertEqual(self.ride1.available_seats, 1)  # 3 - 2 seats booked

    def test_book_ride_insufficient_seats(self):
        """Test booking a ride with insufficient seats."""
        url = reverse('book_ride', kwargs={'id': self.ride1.pk})
        data = {"seats_booked": 4}  # Requesting more seats than available
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Not enough seats available")

    def test_double_booking_prevention(self):
        """Test preventing double booking by the same user."""
        #url = reverse('book_ride', kwargs={'id': self.ride1.pk})
        #data = {"seats_booked": 1}
        data = {
        "id": self.ride1.pk,
        "destination": self.ride1.destination,
        "date": self.ride1.date,
        # Add any other fields that should be included in the response
    }
        url = reverse('rides:book_ride', kwargs={'id': self.ride1.pk})  # Correct the reverse call
        response = self.client.post(url)  # Assuming you're making a POST request to book a ride
        self.assertEqual(response.status_code, 201)  # Check for successful booking
        response = self.client.post(url)  # Attempt to book again
        self.assertEqual(response.status_code, 400)  # Expect a bad request or conflict
        # Access the date attribute correctly
        self.assertEqual(response.data['date'], self.ride1.date)

        # First booking attempt
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Second booking attempt on the same ride
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You have already booked this ride")



