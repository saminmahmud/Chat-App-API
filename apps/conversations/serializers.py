from rest_framework import serializers
from .models import Conversation, Participant
from apps.accounts.serializers import UserMiniSerializer


class ConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ("id", "type", "name", "image", "updated_at")
        

class ParticipantSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    
    class Meta:
        model = Participant
        fields = ("id", "user", "role", "nickname", "joined_at")
        

class ConversationDetailSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    created_by = UserMiniSerializer(read_only=True)
    
    class Meta:
        model = Conversation
        fields = ("id", "type", "name", "image", "created_by", "created_at", "updated_at", "participants")
        
        
class ConversationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ("id", "type", "name", "image")
        

class ConversationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ("id", "name", "image")
        

class ParticipantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ("id", "user", "conversation")
        
    def validate(self, attrs):
        request = self.context.get("request")
        requesting_user = request.user if request else None
        
        is_requesting_user_is_admin = Participant.objects.filter(
            user=requesting_user,
            conversation=attrs.get("conversation"),
            role=Participant.Role.ADMIN
        ).exists()
        
        if not is_requesting_user_is_admin:
            raise serializers.ValidationError("Only admins can add participants to the conversation.")
        
        return attrs

        
class ParticipantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ("id", "role", "nickname", "last_read_message", "left_at")
        
        
        


        
    
        
