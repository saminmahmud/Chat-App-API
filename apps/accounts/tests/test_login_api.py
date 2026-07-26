from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.url = "/api/auth/login/"
        
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123"
        )
        
    def test_login_with_email(self):
        response = self.client.post(
            self.url,
            data={
                'login': 'test@example.com',
                'password': 'password123'
            },
            format='json'
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        
    def test_login_with_username(self):
        response = self.client.post(
            self.url,
            data={
                'login': self.user.username,
                'password': 'password123'
            },
            format='json'
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        
    def test_login_jwt_response_structure(self):
        response = self.client.post(
            self.url,
            data={
                'login': 'test@example.com',
                'password': 'password123'
            },
            format='json'
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)