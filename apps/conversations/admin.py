from django.contrib import admin
from .models import Conversation, Participant


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "created_by")
    
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "conversation", "role")