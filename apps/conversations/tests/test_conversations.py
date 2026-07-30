from tests.base import BaseTestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.conversations.models import Conversation, Participant


class ConversationTestCase(BaseTestCase, APITestCase):
    def setUp(self):
        self.user1 = self.create_user(email="user1@example.com")
        self.user2 = self.create_user(email="user2@example.com")
        self.user3 = self.create_user(email="user3@example.com")
        self.user4 = self.create_user(email="user4@example.com")
        
        # Private Conversation
        self.private_conversation = Conversation.objects.create(
            type=Conversation.Type.PRIVATE
        )
        Participant.objects.create(user=self.user1, conversation=self.private_conversation)
        Participant.objects.create(user=self.user2, conversation=self.private_conversation)
        
        # Group Conversation
        self.group_conversation = Conversation.objects.create(
            type=Conversation.Type.GROUP,
            name="Group Chat",
            created_by=self.user1,
        )
        Participant.objects.create(user=self.user1, conversation=self.group_conversation, role=Participant.Role.ADMIN)
        Participant.objects.create(user=self.user2, conversation=self.group_conversation)
        Participant.objects.create(user=self.user3, conversation=self.group_conversation)
        
        
    def test_private_conversation_creation(self):
        self.assertEqual(self.private_conversation.name, None)
        self.assertEqual(self.private_conversation.created_by, None)
        self.assertEqual(self.private_conversation.participants.count(), 2)
        
    def test_group_conversation_creation(self):
        self.assertEqual(self.group_conversation.name, "Group Chat")
        self.assertEqual(self.group_conversation.created_by, self.user1)
        self.assertEqual(self.group_conversation.participants.count(), 3)
        
    def test_add_participant_to_group_conversation(self):
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('participant-list')
        data = {
            "user": self.user4.id,
            "conversation": self.group_conversation.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.group_conversation.participants.count(), 4)
        self.assertTrue(self.group_conversation.participants.filter(user=self.user4).exists())
        
    def test_non_admin_cannot_add_participant(self):
        self.client.force_authenticate(user=self.user2)
        
        url = reverse('participant-list')
        data = {
            "user": self.user4.id,
            "conversation": self.group_conversation.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.group_conversation.participants.count(), 3)
        self.assertFalse(self.group_conversation.participants.filter(user=self.user4).exists())
    
    def test_participant_is_unique(self):
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('participant-list')
        data = {
            "user": self.user2.id,
            "conversation": self.group_conversation.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.group_conversation.participants.count(), 3)

    def test_make_admin(self):
        self.client.force_authenticate(user=self.user1)
        
        participant = Participant.objects.get(user=self.user2, conversation=self.group_conversation)
        
        url = reverse('participant-detail', kwargs={'pk': participant.id})
        data = {
            "role": Participant.Role.ADMIN
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        participant.refresh_from_db()
        self.assertEqual(participant.role, Participant.Role.ADMIN)
        self.assertEqual(self.group_conversation.participants.filter(role=Participant.Role.ADMIN).count(), 2)
        
    def test_leave_conversation(self):
        self.client.force_authenticate(user=self.user1)
        
        participant = Participant.objects.get(user=self.user1, conversation=self.group_conversation)
        
        url = reverse('participant-leave', kwargs={'pk': participant.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.group_conversation.participants.filter(user=self.user1).exists())
        self.assertEqual(self.group_conversation.participants.count(), 2)
        self.assertTrue(self.group_conversation.participants.filter(role=Participant.Role.ADMIN, user=self.user2).exists())
        
    def test_remove_participant(self):
        self.client.force_authenticate(user=self.user1)
        
        participant = Participant.objects.get(user=self.user2, conversation=self.group_conversation)
        
        url = reverse('participant-remove', kwargs={'pk': participant.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.group_conversation.participants.filter(user=self.user2).exists())
        self.assertEqual(self.group_conversation.participants.count(), 2)