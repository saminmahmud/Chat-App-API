from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class ChangePasswordAPITestCase(APITestCase):
    def setUp(self):
        self.url = "/api/auth/password/change/"
        
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123"
        )
        
    def test_change_password_success(self):
        self.client.force_authenticate(user=self.user) # authenticates the user for the test
        
        response = self.client.post(
            self.url,
            data={
                'new_password1': 'newpassword456',
                'new_password2': 'newpassword456'
            },
            format='json'
        )
        
        self.assertEqual(
            response.status_code, 
            status.HTTP_200_OK
        )
        
        self.user.refresh_from_db() # ensure the latest user data is fetched from the database
        
        self.assertTrue(
            self.user.check_password('newpassword456')
        )