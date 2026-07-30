from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationCreateSerializer, ParticipantSerializer, ParticipantCreateSerializer, ParticipantUpdateSerializer, ConversationUpdateSerializer
from .models import Conversation, Participant
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsEmailVerified


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated, IsEmailVerified]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        elif self.action == 'retrieve':
            return ConversationDetailSerializer
        elif self.action == 'create':
            return ConversationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ConversationUpdateSerializer
        
        return ConversationDetailSerializer
    
    
class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    permission_classes = [IsAuthenticated, IsEmailVerified]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ParticipantCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ParticipantUpdateSerializer
        
        return ParticipantSerializer
    
    # leave the conversation
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        participant = self.get_object()
        
        if participant.user != request.user:
            return Response({"detail": "You can only leave your own conversation."}, status=status.HTTP_403_FORBIDDEN)
        
        if participant.role == Participant.Role.ADMIN:
            other_admins = Participant.objects.filter(conversation=participant.conversation, role=Participant.Role.ADMIN).exclude(user=request.user)
            if not other_admins.exists():
                # oldest participant becomes admin
                oldest_participant = Participant.objects.filter(conversation=participant.conversation).exclude(user=request.user).order_by('joined_at').first()
                if oldest_participant:
                    oldest_participant.role = Participant.Role.ADMIN
                    oldest_participant.save()
                    
        participant.delete()
        return Response({"detail": "You have left the conversation."}, status=status.HTTP_204_NO_CONTENT)
    
    # Remove a participant from the conversation
    @action(detail=True, methods=['post'])
    def remove(self, request, pk=None):
        participant = self.get_object()
        
        if not participant:
            return Response({"detail": "Participant not found."}, status=status.HTTP_404_NOT_FOUND)
        
        admin = Participant.objects.filter(conversation=participant.conversation, user=request.user, role=Participant.Role.ADMIN).first()
        if not admin:
            return Response({"detail": "Only admins can remove participants from the conversation."}, status=status.HTTP_403_FORBIDDEN)
        
        participant.delete()
        return Response({"detail": "Participant removed from the conversation."}, status=status.HTTP_204_NO_CONTENT)


    