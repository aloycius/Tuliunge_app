import pytest
from datetime import datetime, timedelta
from rest_framework import status
from rides.models import Ride  # Replace with your actual Ride model path


@pytest.mark.django_db
def test_create_ride(auth_client):
    """Test creating a ride."""
    client = auth_client()  # Get an authenticated client
    data = {
        "departure_location": "Location A",
        "destination": "Location B",
        "departure_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "available_seats": 3,
        "price": 50.0
    }
    response = client.post("/api/rides/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["departure_location"] == "Location A"
    assert response.data["available_seats"] == 3


@pytest.mark.django_db
def test_list_rides(api_client, sample_rides):
    """Test listing rides."""
    sample_rides()  # Create sample rides
    response = api_client.get("/api/rides/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["departure_location"] == "Location A"


@pytest.mark.django_db
def test_filter_rides_by_date(api_client, sample_rides):
    """Test filtering rides by date."""
    rides = sample_rides()  # Create sample rides
    filter_date = rides[0].departure_time.date().isoformat()
    response = api_client.get(f"/api/rides/?departure_time={filter_date}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["departure_location"] == rides[0].departure_location


@pytest.mark.django_db
def test_get_ride_details(api_client, sample_rides):
    """Test getting ride details."""
    rides = sample_rides()  # Create sample rides
    ride_id = rides[0].id
    response = api_client.get(f"/api/rides/{ride_id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["departure_location"] == "Location A"


@pytest.mark.django_db
def test_book_ride(auth_client, sample_rides):
    """Test booking a ride."""
    client = auth_client()  # Get an authenticated client
    rides = sample_rides()  # Create sample rides
    ride_id = rides[0].id

    response = client.post(f"/api/rides/{ride_id}/book/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Ride booked successfully."

    # Verify seat availability decreased
    ride = Ride.objects.get(id=ride_id)
    assert ride.available_seats == 2


@pytest.mark.django_db
def test_book_ride_no_seats(auth_client, sample_rides):
    """Test booking a ride with no available seats."""
    client = auth_client()  # Get an authenticated client
    rides = sample_rides()  # Create sample rides
    ride = rides[0]
    ride.available_seats = 0
    ride.save()

    response = client.post(f"/api/rides/{ride.id}/book/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "No seats available."


@pytest.mark.django_db
def test_double_booking(auth_client, sample_rides):
    """Test preventing double booking."""
    client = auth_client()  # Get an authenticated client
    rides = sample_rides()  # Create sample rides
    ride_id = rides[0].id

    # First booking
    response = client.post(f"/api/rides/{ride_id}/book/")
    assert response.status_code == status.HTTP_200_OK

    # Second booking attempt
    response = client.post(f"/api/rides/{ride_id}/book/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "You have already booked this ride."
