import random
from django.test import TestCase
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()


class BaseTestCase(TestCase):
    
    def create_user(self, email=f"test{random.randint(1, 10000)}@example.com", password="Password123@", verified=True, bio="My Bio", **kwargs):
        user =  User.objects.create_user(email=email, password=password, bio=bio, **kwargs)
        
        EmailAddress.objects.create(user=user, email=email, verified=verified, primary=True)
        
        return user
    
    