from django.db import models
from django.conf import settings


class Conversation(models.Model):
    class Type(models.TextChoices):
        PRIVATE = "private", "Private"
        GROUP = "group", "Group"
        
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.PRIVATE)
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='conversation_images/', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_conversations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name if self.name else f"Conversation {self.id}"
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['name']),
        ]
        

class Participant(models.Model):
    class Role(models.TextChoices):
        MEMBER = "member", "Member"
        ADMIN = "admin", "Admin"
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='participants', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='participants', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)
    last_read_message = models.ForeignKey('messaging.Message', related_name='last_read_by', blank=True, null=True, on_delete=models.SET_NULL)
        
    def __str__(self):
        return f"{self.user.username} in {self.conversation.name if self.conversation.name else f'Conversation {self.conversation.id}'}"
    
    class Meta:
        unique_together = ('user', 'conversation')
        indexes = [
            models.Index(fields=['role']),
        ]   
