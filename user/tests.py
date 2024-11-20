from django.test import TestCase

# Create your tests here.
# user/test_authentication.py

from django.urls import reverse
#from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
import json
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


"""
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
        respData = json.loads(response)
        
        # Check for bad request due to missing fields
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", respData.data)  # Assuming password field is required

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
"""

class AuthTests(APITestCase):

    def setUp(self):
        # Setup test data
        self.register_url = reverse('register')  # The URL name you used for registration
        self.login_url = reverse('login')        # The URL name you used for login
        self.logout_url = reverse('logout')      # The URL name you used for logout

        # Create a test user
        self.test_user = {
            'name': 'testuser',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password': 'strongpassword123'
        }
        
        # Register a user to use in tests
        self.client.post(self.register_url, self.test_user, format='json')

    def get_token(self):
        # Helper function to get a JWT token for the user
        response = self.client.post(self.login_url, {
            'email': self.test_user['email'],
            'password': self.test_user['password']
        }, format='json')
        return response.data.get('access')
    

    #test_user_registration
    def test_user_registration(self):
        response = self.client.post(self.register_url, {
            'name': 'winny',
            'email': 'winny@example.com',
            'phone_number': '1234567890',
            'password': 'strongpassword123'
        }, format='json')
        
        # Check that the registration was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
    
    #test_user_login
    def test_user_login(self):
        """
        response = self.client.post(self.login_url, {
            'email': self.test_user['email'],
            'password': self.test_user['password']
        }, format='json')
        """
        response = self.client.post( 
             reverse('login'),
             {'email': 'winny@example.com', 'password': 'strongpassword123'},
             format='json')
        print("Response Status Code:", response.status_code)  # Debugging
        print("Response Data:", response.json())  # Debugging
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if login is successful and a token is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    #test_user_logout
    def test_user_logout(self):
        # Get a token
        token = self.get_token()
        
        # Add the token to the header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Perform logout
        response = self.client.post(self.logout_url)
        
        # Check if logout is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], "Successfully logged out.")



        

