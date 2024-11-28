import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def api_client():
    """Fixture for creating an API client."""
    return APIClient()

@pytest.fixture
def create_user():
    """Fixture to create a test user."""
    def _create_user(**kwargs):
        User = get_user_model()
        return User.objects.create_user(**kwargs)
    return _create_user

@pytest.fixture
def auth_urls():
    """Fixture for authentication URLs."""
    return {
        "register": reverse("register"),
        "login": reverse("login"),
        "logout": reverse("logout"),
        "refresh": reverse("token_refresh")
    }
