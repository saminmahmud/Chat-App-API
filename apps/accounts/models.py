from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

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
        
            
class FriendRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        CANCELLED = "cancelled", "Cancelled"
        
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver_friend_requests', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"FriendRequest from {self.sender.username} to {self.receiver.username} - Status: {self.status}"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('receiver', 'sender')
        indexes = [
            models.Index(fields=['receiver']),
            models.Index(fields=['sender']),
        ]

