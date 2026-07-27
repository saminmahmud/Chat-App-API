from django.db import models
from django.conf import settings
from apps.conversations.models import Conversation
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class Message(models.Model):
    class MessageType(models.TextChoices):
        TEXT = "text", "Text"
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"
        FILE = "file", "File"
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=MessageType.choices, default=MessageType.TEXT)
    content = models.TextField()
    reply_to = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Message {self.id} in {self.conversation.name if self.conversation.name else f'Conversation {self.conversation.id}'}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['conversation']),
            models.Index(fields=['sender']),
            models.Index(fields=['is_edited']),
            models.Index(fields=['is_deleted']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['reply_to']),
        ]
        
        
class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='message_attachments/')
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='message_attachments/thumbnails/', blank=True, null=True)
    
    def __str__(self):
        return f"Attachment {self.id} for Message {self.message.id}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['message']),
            models.Index(fields=['thumbnail']),
            models.Index(fields=['created_at']),
        ]
        
    def save(self, *args, **kwargs):
        if self.file and self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            img = Image.open(self.file)
            img.thumbnail((300, 300), Image.ANTIALIAS)
            
            thumb_io = BytesIO()
            img_format = img.format if img.format else "JPEG"
            img.save(thumb_io, format=img_format)
            thumb_file = ContentFile(thumb_io.getvalue(), name=f'thumbnail_{self.file.name}')
            
            self.thumbnail.save(thumb_file.name, thumb_file, save=False)
        
        super().save(*args, **kwargs)
        
        
class MessageReaction(models.Model):
    class Emoji(models.TextChoices):
        LIKE = "👍", "👍"
        LOVE = "❤️", "❤️"
        LAUGH = "😂", "😂"
        SURPRISED = "😲", "😲"
        SAD = "😢", "😢"
        ANGRY = "😡", "😡"
        
    message = models.ForeignKey(Message, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_reactions', on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10, choices=Emoji.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} reacted with {self.emoji} to Message {self.message.id}"
    
    class Meta:
        unique_together = ('message', 'user', 'emoji')
        indexes = [
            models.Index(fields=['message']),
            models.Index(fields=['user']),
            models.Index(fields=['emoji']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]