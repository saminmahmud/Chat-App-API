from django.contrib import admin
from .models import Message, MessageAttachment, MessageReaction


class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment
    extra = 0
    list_display = ('id', 'file', 'thumbnail', 'created_at')
    
class MessageReactionInline(admin.TabularInline):
    model = MessageReaction
    extra = 0
    list_display = ('id', 'emoji', 'user', 'created_at')
    
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'conversation', 'content', 'type')
    inlines = [MessageAttachmentInline, MessageReactionInline]



