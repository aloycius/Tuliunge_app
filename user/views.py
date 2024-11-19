from django.shortcuts import render



# ...
# Create your views here.
# user/views.py
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserManager
from django.contrib.auth import authenticate
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken  # for JWT tokens
from rest_framework.exceptions import ValidationError

# Register API
""""
class RegisterView(APIView):
    def post(self, request):
        
        if request.method == "POST":
            return Response({
                "message": "Register successful",
            }, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
"""

class RegisterView(APIView):
     permission_classes = [AllowAny]

     def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
   
# Login API
"""
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({"msg": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#LOGOUT API
    
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # The refresh token is expected to be provided in the request data
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"msg": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            ##token.blacklist()  # Blacklist the token if you're using the blacklist app
            return Response({"msg": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            raise ValidationError({"msg": "Token is invalid or expired."})

    


    


