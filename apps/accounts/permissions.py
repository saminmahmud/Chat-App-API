from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from allauth.account.models import EmailAddress


class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        is_verified = EmailAddress.objects.filter(user=request.user, verified=True).exists()
        
        if not is_verified:
            raise PermissionDenied("Email address is not verified.")
        
        return True