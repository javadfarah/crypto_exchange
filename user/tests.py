from rest_framework.test import APITestCase
from user.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.urls import reverse
from rest_framework import status


class LoginViewTests(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_login_with_valid_credentials(self):
        response = self.client.post('/auth/login/', {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_login_with_invalid_credentials(self):
        response = self.client.post('/auth/login/', {
            'username': self.username,
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid Credentials')


# class AuthMeViewTests(APITestCase):
#     def setUp(self):
#         self.username = 'testuser'
#         self.email = 'testuser@example.com'
#         self.password = 'testpassword'
#         self.user = User.objects.create_user(
#             username=self.username,
#             email=self.email,
#             password=self.password
#         )
#         self.access_token = AccessToken.for_user(self.user)
#
#     def test_auth_me_with_valid_access_token(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
#         response = self.client.post('/auth/me/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['username'], self.username)
#         self.assertEqual(response.data['message'], 'Access token is valid')
#
#     def test_auth_me_with_invalid_access_token(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
#         response = self.client.post('/auth/me/')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(response.data['detail'], 'Given token not valid for any token type')


class TokenRefreshTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = RefreshToken.for_user(self.user)

    def test_token_refresh(self):
        refresh_token = str(self.token)
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh_token}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_invalid_token_refresh(self):
        response = self.client.post(reverse('token_refresh'), {'refresh': 'invalidtoken'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Token is invalid or expired')


class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.access_token = AccessToken.for_user(self.user)

    def test_logout(self):
        self.client.force_login(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        response = self.client.post('/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class SignupTestCase(APITestCase):
    def test_signup(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post('/auth/signup/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
