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
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth import get_user_model
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.timezone import now



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
        register_response = self.client.post(self.register_url, self.test_user, format='json')
        print("Registration Status Code:", register_response.status_code)  # Debugging
        print("Registration Response Data:", register_response.json())  # Debugging

        # Get the user instance for later use in testing expired token
        self.user = User.objects.get(name=self.test_user_data['name'],
                                     email=self.test_user_data['email'],
                                     phone_number=self.test_user_data['phone_number'],
                                     password=self.test_user_data['password'])  # Adjust for your User model
        
    def get_token(self):
        # Helper function to get a JWT token for the user
        response = self.client.post(self.login_url, {
        'email': self.test_user['email'],
        'password': self.test_user['password']
    }, format='json')
    
    # Debugging information
        print("Login for Token Status Code:", response.status_code)
        print("Login for Token Response Data:", response.json())
    
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
        #self.assertIn('token', response.data)
        self.assertIn('msg', response.data)  # Check for a success message
        self.assertEqual(response.data['msg'], 'User registered successfully')

    
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
             {'email': self.test_user['email'], 'password': self.test_user['password']},
             format='json')
        print("Response Status Code:", response.status_code)  # Debugging
        print("Response Data:", response.json())  # Debugging
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if login is successful and a token is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        if 'access' not in response.data:
            print("Login failed: 'access' token not found in response.")
    
    def test_invalid_login_credentials(self):
     response = self.client.post(self.login_url, {
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }, format='json')
     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
     self.assertIn('non_field_errors', response.data)
    

    def test_missing_login_credentials(self):
     response = self.client.post(self.login_url, {}, format='json')
     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
     self.assertIn('email', response.data)
     self.assertIn('password', response.data)
    
    def test_expired_token_access(self):
    # Create an expired token manually
     expired_token = AccessToken.for_user(self.user)
     expired_token.set_exp(lifetime=timedelta(seconds=-1))  # Set expiry in the past

     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
    
     response = self.client.get(self.protected_url)  # Replace with an actual protected endpoint URL
     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_access_with_invalid_token(self):
    # Use a deliberately malformed token
     self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken12345')
    
     response = self.client.get(self.login_url)  # Replace with an actual protected endpoint URL
     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

    def test_refresh_token_flow(self):
    # Use the refresh token to get a new access token
     response = self.client.post('/api/token/refresh/', {  # Replace with your refresh token endpoint
        'refresh': self.refresh_token
    }, format='json')
    
     self.assertEqual(response.status_code, status.HTTP_200_OK)
     self.assertIn('access', response.data)
    
    
    


    #test_user_logout
    """
    def test_user_logout(self):
        
        # Get a token
        token = self.get_token()
        
        # Ensure the token is not None or empty
        if not token:
         self.fail("Token was not returned during login.")

        # Debugging information for the token
        print("Token retrieved for logout:", token)
    
        # Ensure a valid token is received
        self.assertIsNotNone(token, "Failed to retrieve a valid token for logout")
    
    
        
        # Add the token to the header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Perform logout
        response = self.client.post(self.logout_url,{'refresh': token}, format='json')
        #response = self.client.post(self.logout_url, format='json')

        # Debugging the response
        print("Logout Response Status Code:", response.status_code)
        try:
          print("Logout Response Data:", response.json())
        except Exception as e:
          print(f"Failed to parse JSON response: {e}")
        
        # Check if logout is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], "Successfully logged out.")
    """

    """
    # Manually authenticate the user
        user = get_user_model().objects.get(email=self.test_user['email'])  # Assuming a User model
        self.client.force_authenticate(user=user)

    # Perform logout
        response = self.client.post(self.logout_url)

    # Debugging the response
        print("Logout Response Status Code:", response.status_code)
        print("Logout Response Data:", response.json())

    # Check if logout is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('msg'), "Successfully logged out.")
  """
def test_logout_without_token(self):
     response = self.client.post(self.logout_url)
     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

def test_logout_with_expired_token(self):
      # Generate a token using the `AccessToken` class for the user
     access_token = AccessToken.for_user(self.user)
     
    # Use an expired token for the logout process
     expired_token = AccessToken.for_user(self.user)
     expired_token.set_exp(lifetime=timedelta(seconds=-1))  # Set expiry in the past

     # Convert the expired token to a string for use in authorization
     expired_token = str(access_token)
    
     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')

     # Try to access the protected endpoint with the expired token
     response = self.client.post(self.logout_url)
     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

def test_access_protected_route_without_authentication(self):
    response = self.client.get(self.protected_url)  # Replace with an actual protected endpoint URL
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    
def test_user_logout(self):
    # Get a token (and refresh token)
    response = self.client.post(self.login_url, {
        'email': self.test_user['email'],
        'password': self.test_user['password']
    }, format='json')
    
    # Debugging information for the login response
    print("Login Response Status Code:", response.status_code)
    print("Login Response Data:", response.json())
    
    # Ensure the login is successful
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Get tokens from the response
    access_token = response.data.get('access')
    refresh_token = response.data.get('refresh')
    
    # Debugging information for tokens
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)

    # Ensure valid tokens are received
    self.assertIsNotNone(access_token, "Failed to retrieve a valid access token for logout")
    self.assertIsNotNone(refresh_token, "Failed to retrieve a valid refresh token for logout")
    
    # Add the access token to the header for the logout request
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # Debugging information for headers before logout
    print("Headers before logout attempt:", self.client._credentials)
    
    # Perform logout
    response = self.client.post(self.logout_url, {
        'refresh': refresh_token  # Include refresh token for logout if required
    }, format='json')
    
    # Debugging the logout response
    print("Logout Response Status Code:", response.status_code)
    try:
        print("Logout Response Data:", response.json())
    except Exception as e:
        print(f"Failed to parse JSON response: {e}")
        print("Raw Response Content:", response.content)
    
    # Check if logout is successful
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data.get('msg'), "Successfully logged out.")

def test_double_logout_attempt(self):
    # Perform the first logout
    token = self.get_token()
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = self.client.post(self.logout_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Attempt to logout again with the same token
    response = self.client.post(self.logout_url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



        

