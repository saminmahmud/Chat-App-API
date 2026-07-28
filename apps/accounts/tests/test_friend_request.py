from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import FriendRequest
from rest_framework import status
from tests.base import BaseTestCase
from django.urls import reverse

User = get_user_model()


class FriendRequestTestCase(BaseTestCase, APITestCase):
    def setUp(self):

        self.sender = self.create_user(
            email="sender@example.com"
        )
        
        self.receiver = self.create_user(
            email="receiver@example.com"
        )

    def test_create_friend_request(self):
        self.client.force_authenticate(user=self.sender)
        
        url = reverse("friend-request-list")
        
        response = self.client.post(
            url,
            {"receiver": self.receiver.id},
            format="json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        
    def test_accept_friend_request(self):
        friend_request = FriendRequest.objects.create(
            sender=self.sender,
            receiver=self.receiver
        )
        
        self.client.force_authenticate(user=self.receiver)
        
        url = reverse("friend-request-accept", kwargs={"pk": friend_request.id})
        
        response = self.client.post(url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        
        friend_request.refresh_from_db()
        
        self.assertEqual(friend_request.status, FriendRequest.Status.ACCEPTED)
        
    def test_cancel_friend_request(self):
        friend_request = FriendRequest.objects.create(
            sender=self.sender,
            receiver=self.receiver
        )
        
        self.client.force_authenticate(user=self.sender)
        
        url = reverse("friend-request-cancel", kwargs={"pk": friend_request.id})
        
        response = self.client.post(url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        
        friend_request.refresh_from_db()
        
        self.assertEqual(friend_request.status, FriendRequest.Status.CANCELLED)

    def test_sent_again_friend_request_after_cancellation(self):
        friend_request = FriendRequest.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            status=FriendRequest.Status.CANCELLED
        )
        
        self.client.force_authenticate(user=self.sender)
        
        url = reverse("friend-request-list")
        
        response = self.client.post(
            url,
            {"receiver": self.receiver.id},
            format="json"
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        
        self.assertEqual(
            FriendRequest.objects.count(),
            1
        )
        
    def test_cannot_accept_friend_request_not_receiver(self):
        friend_request = FriendRequest.objects.create(
            sender=self.sender,
            receiver=self.receiver
        )
        
        self.client.force_authenticate(user=self.sender)
        
        url = reverse("friend-request-accept", kwargs={"pk": friend_request.id})
        
        response = self.client.post(url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        
        