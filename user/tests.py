from django.test import TestCase

# Create your tests here.
# user/test_authentication.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User

class UserAuthenticationTests(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_user_registration(self):
        data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "phone_number": "1234567890",
            "password": "password123"
        }
        response = self.client.post(self.register_url, data)
        
        # Check if registration is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "User registered successfully")
        
        # Verify user creation in the database
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, data["email"])

    def test_registration_with_missing_fields(self):
        data = {
            "email": "testuser@example.com",
            # Missing "name", "phone_number", "password"
        }
        response = self.client.post(self.register_url, data)
        
        # Check for bad request due to missing fields
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)  # Assuming password field is required

    def test_user_login(self):
        # Register a user for testing login
        user = User.objects.create_user(
            email="loginuser@example.com", name="Login User", 
            phone_number="0987654321", password="password123"
        )
        data = {
            "email": "loginuser@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data)
        
        # Check if login is successful and token is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self):
        data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        
        # Check for bad request due to invalid credentials
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)  # Adjust if serializer uses another error field

