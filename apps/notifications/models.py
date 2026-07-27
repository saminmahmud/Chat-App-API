from django.db import models
from django.conf import settings
from apps.messaging.models import Message


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        FRIEND_REQUEST = "friend_request", "Friend Request"
        MESSAGE = "message", "Message"
       
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_notifications', on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    action_url = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.id} for {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]
        
    @property
    def body(self):
        if self.notification_type == self.NotificationType.FRIEND_REQUEST:
            return f"{self.sender.username} sent you a friend request."
        
        if self.notification_type == self.NotificationType.MESSAGE:
            conversation = self.message.conversation
            if conversation.type == conversation.Type.PRIVATE:
                return f"{self.sender.username} sent you a message."
            
            return f"{self.sender.username} sent a message in {conversation.name}."
            