from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserModelTest(TestCase):

    def test_create_user(self):

        user = User.objects.create_user(
            email="samin@gmail.com",
            password="12345678"
        )
        
        self.assertEqual(
            user.email,
            "samin@gmail.com"
        )

        self.assertTrue(
            user.check_password("12345678")
        )
        
    def test_username_auto_generated(self):

        user = User.objects.create_user(
            email="samin@gmail.com",
            password="12345678"
        )

        self.assertEqual(
            user.username,
            "samin"
        )