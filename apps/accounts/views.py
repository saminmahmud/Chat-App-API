from rest_framework.decorators import action
from django.shortcuts import render
from dj_rest_auth.views import LoginView
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from apps.accounts.models import FriendRequest
from apps.accounts.prmissions import IsEmailVerified
from apps.accounts.serializers import LoginResponseSerializer, LoginUserSerializer
from .serializers import FriendRequestSerializer, FriendRequestCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CustomLoginView(LoginView):
    @extend_schema(
        responses={
            200: LoginResponseSerializer
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_response(self):
        response = super().get_response()
        response.data['user'] = LoginUserSerializer(self.user).data
        return response


class FriendRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsEmailVerified]
    
    def get_queryset(self):
        user = self.request.user

        if self.action == "cancel":
            return FriendRequest.objects.select_related("sender", "receiver").filter(sender=user)
        
        return FriendRequest.objects.select_related("sender", "receiver").filter(receiver=user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FriendRequestCreateSerializer
        
        return FriendRequestSerializer
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user) 
        
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        
        if friend_request.status != FriendRequest.Status.PENDING:
            return Response(
                {"detail": "Only pending requests can be accepted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        friend_request.status = FriendRequest.Status.ACCEPTED
        friend_request.save(update_fields=["status"])
        return Response(
            {"detail": "Friend request accepted."},
            status=status.HTTP_200_OK,
        )
        
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.status != FriendRequest.Status.PENDING:
            return Response(
                {"detail": "Only pending requests can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request.status = FriendRequest.Status.CANCELLED
        friend_request.save(update_fields=["status"])

        return Response(
            FriendRequestSerializer(friend_request).data,
            status=status.HTTP_200_OK
        )
        
        