import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rides.models import Ride  # Replace with your actual Ride model path
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model


@pytest.fixture
def api_client():
    """Fixture to provide an unauthenticated API client."""
    return APIClient()

""""
@pytest.fixture
def auth_client(api_client):
    ##Fixture to provide an authenticated API client.
    def _auth_client(user_data=None):
        if user_data is None:
            user_data = {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "testpassword"
            }
        user = User.objects.create_user(**user_data)
        login_response = api_client.post('/user/auth/login/', {
            "email": user_data["email"],
            "password": user_data["password"]
        })
        token = login_response.data.get("access")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return api_client
    return _auth_client
"""

@pytest.fixture
def auth_client(create_user):
    """
    Provides an authenticated APIClient instance.
    """
    user = create_user(
        name="Test User",
        email="testuser@example.com",
        phone_number="1234567890",
        password="password123"
    )
    client = APIClient()
    # Log in the user to get tokens
    response = client.post("auth/login/", {"email": user.email, "password": "password123"})
    access_token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client

@pytest.fixture
def create_user(db):
    from django.contrib.auth import get_user_model

    def _create_user(name, email, phone_number, password):
        User = get_user_model()
        return User.objects.create_user(
            name=name,
            email=email,
            phone_number=phone_number,
            password=password,
        )

    return _create_user


@pytest.fixture
def sample_rides():
    """Fixture to create sample rides."""
    def _sample_rides():
        now = datetime.now()
        rides = [
            Ride.objects.create(
                departure_location="Location A",
                destination="Location B",
                departure_time=now + timedelta(days=1),
                available_seats=3,
                price=50.0
            ),
            Ride.objects.create(
                departure_location="Location C",
                destination="Location D",
                departure_time=now + timedelta(days=2),
                available_seats=4,
                price=75.0
            )
        ]
        return rides
    return _sample_rides
