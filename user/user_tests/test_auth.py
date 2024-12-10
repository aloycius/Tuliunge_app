import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta

@pytest.mark.django_db
class TestAuth:
    
    def test_user_registration(self, api_client, auth_urls):
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "phone_number": "1234567890",
            "password": "password123"
        }
        response = api_client.post(auth_urls["register"], data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("msg") == "User registered successfully"
    
    def test_user_login(self, api_client, create_user, auth_urls):
    
        user = create_user(
            name="Test User",
            email="testuser@example.com",
            phone_number="1234567890",
            password="password123"
        )

        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = api_client.post(auth_urls["login"], data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
    
    def test_invalid_login_credentials(self, api_client, auth_urls):
        data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = api_client.post(auth_urls["login"], data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data
    
    def test_expired_token_access(self, api_client, create_user, auth_urls):
        user = create_user(
            name="Expired User",
            email="expired@example.com",
            phone_number="0987654321",
            password="password123"
        )
        expired_token = AccessToken.for_user(user)
        expired_token.set_exp(lifetime=timedelta(seconds=-1))
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {expired_token}")
        
        response = api_client.get(auth_urls["login"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token_flow(self, api_client, create_user, auth_urls):
        user = create_user(
            name="Refresh User",
            email="refresh@example.com",
            phone_number="1231231234",
            password="password123"
        )
        login_response = api_client.post(auth_urls["login"], {
            "email": "refresh@example.com",
            "password": "password123"
        })
        refresh_token = login_response.data.get("refresh")
        response = api_client.post(auth_urls["refresh"], {"refresh": refresh_token})
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        
    def test_user_logout(self, api_client, create_user, auth_urls):
        """Test if a user can log out successfully."""
        # Create a user and log in to get a valid token
        user = create_user(
            name="Logout User",
            email="logoutuser@example.com",
            phone_number="1234567890",
            password="password123"
        )
        login_data = {
            "email": "logoutuser@example.com",
            "password": "password123"
        }
        login_response = api_client.post(auth_urls["login"], login_data)

        access_token = login_response.data.get("access")
        refresh_token = login_response.data.get("refresh")
        assert access_token and refresh_token  # Ensure tokens are present

        # Authenticate the user with the token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Perform logout
        logout_data = {"refresh": refresh_token}
        response = api_client.post(auth_urls["logout"], data = logout_data)
        
        # Debugging the logout response
        print("Login response data:", login_response.data)
        print("Logout response data:", response.data)
        print("Logout response status code:", response.status_code)


        assert response.status_code == status.HTTP_205_RESET_CONTENT
        assert response.data.get("msg") == "Successfully logged out."
    
    def test_logout_with_invalid_token(self, api_client, auth_urls):
        """Test logout with an invalid or missing token."""
        # No valid token is set in the API client
        response = api_client.post(auth_urls["logout"])
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get("detail") == "Authentication credentials were not provided."