from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from utils.jwt.jwt_token import AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
import time
import math


class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class AuthMeView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        update_token = False
        try:
            access_token = request.data['access_token']
            refresh_token = request.data['refresh_token']
            if access_token is None or refresh_token is None:
                return Response({'message': 'Both access token and refresh token are required.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'Both access token and refresh token are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token_obj = AccessToken(access_token)
            refresh_token_obj = RefreshToken(refresh_token)
        except Exception:
            return Response({'message': 'Invalid access token or refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)

        access_token_exp = access_token_obj['exp']
        now = time.time()
        time_left_in_minutes = math.floor((access_token_exp - now) / 60)

        if time_left_in_minutes < 15:  # Checks if less than 15 minutes remain until token expiration
            access_token_obj = refresh_token_obj.access_token
            access_token = str(access_token_obj)
            update_token = True

        try:
            access_token_obj.verify()
        except Exception:
            try:
                access_token_obj = refresh_token_obj.access_token
                access_token = str(access_token_obj)
                update_token = True
            except Exception:
                return Response({'message': 'Invalid access token or refresh token.'},
                                status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(id=access_token_obj.payload.get("user_id"))
        role = user.groups.first().name if user.groups.exists() else ""

        return Response({
            'update_token': update_token,
            'access_token': access_token,
            'refresh_token': str(refresh_token_obj),
            'username': user.username,
            'role': role,
            'message': 'Access token is valid.',
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            logout(request)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username or not password:
            return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Check if the username already exists in the database
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return Response({'success': 'Successfully registered'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
