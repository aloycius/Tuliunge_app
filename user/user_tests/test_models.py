import pytest
from django.contrib.auth import get_user_model

@pytest.mark.django_db
class TestUserModel:

    def test_user_creation(self):
        User = get_user_model()
        user = User.objects.create_user(
            name="Test User",
            email="testuser@example.com",
            phone_number="1234567890",
            password="password123"
        )
        assert user.name == "Test User"
        assert user.email == "testuser@example.com"
        assert user.phone_number == "1234567890"
        assert user.check_password("password123")
    
    def test_user_str_representation(self):
        User = get_user_model()
        user = User.objects.create_user(
            name="Test User",
            email="testuser@example.com",
            phone_number="1234567890",
            password="password123"
        )
        assert str(user) == "testuser@example.com"
