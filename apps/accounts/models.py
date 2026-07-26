from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.username:
            base_username = self.email.split("@")[0].lower()
            username = base_username
            counter = 1
            
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
                
            self.username = username
            
        super().save(*args, **kwargs)
            
    def __str__(self):
        return self.username
    
    class Meta:
        indexes = [
            models.Index(fields=['username']),
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    @property
    def is_active_user(self):
        email_verified = self.emailaddress_set.filter(verified=True).exists()
        return super().is_active and email_verified
        
            
    
