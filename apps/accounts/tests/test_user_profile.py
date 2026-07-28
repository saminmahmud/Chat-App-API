from rest_framework import status
from rest_framework.test import APITestCase
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from tests.base import BaseTestCase


class UserProfileAPITestCase(BaseTestCase, APITestCase):
    def setUp(self):
        self.url = "/api/auth/user/"

        self.user = self.create_user(
            email="test@example.com",
            password="Password123@",
            bio="Old Bio"
        )

    def test_create_user(self):

        self.assertEqual(
            self.user.email,
            "test@example.com"
        )

        self.assertTrue(
            self.user.check_password("Password123@")
        )
        
    def test_username_auto_generated(self):

        self.assertEqual(
            self.user.username,
            "test"
        )
    
    def test_update_username(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.patch(
            self.url,
            {"username": "new_username"},
            format="json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        
        self.user.refresh_from_db()
        
        self.assertEqual(self.user.username, "test")
        
    def test_update_profile_picture(self):
        self.client.force_authenticate(user=self.user)
        
        # Create a simple image for testing
        image = Image.new('RGB', (100, 100))
        byte_io = BytesIO()
        image.save(byte_io, 'JPEG')
        byte_io.seek(0)
        
        image_file = SimpleUploadedFile("test_image.jpg", byte_io.read(), content_type="image/jpeg")
        
        response = self.client.patch(
            self.url,
            {"profile_picture": image_file},
            format="multipart"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        
        self.user.refresh_from_db()
        
        self.assertIsNotNone(self.user.profile_picture)
        
        self.user.profile_picture.delete(save=True)
        