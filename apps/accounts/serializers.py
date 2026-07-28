from django.contrib.auth import authenticate, get_user_model
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import FriendRequest

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    login = serializers.CharField()

    username = None
    email = None

    def validate(self, attrs):
        login = attrs["login"]
        password = attrs["password"]

        if "@" in login:
            try:
                user = User.objects.get(email__iexact=login)
                username = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email.")
        else:
            username = login

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        attrs["user"] = user
        return attrs
    
    
class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_active_user",
        )


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = LoginUserSerializer()
    

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return email
    
    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "is_active_user", "profile_picture", "bio", "last_seen", "created_at", "updated_at")
        read_only_fields = ("email", "username", "is_active_user", "last_seen", "created_at", "updated_at")
        
    def validate(self, attrs):
        if "username" in attrs:
            raise serializers.ValidationError({"username": "You cannot update the username."})
        if "email" in attrs:
            raise serializers.ValidationError({"email": "You cannot update the email."})
        return super().validate(attrs)


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "profile_picture")    


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserMiniSerializer(read_only=True)
    receiver = UserMiniSerializer(read_only=True)
    
    class Meta:
        model = FriendRequest
        fields = ("id", "sender", "receiver", "status", "created_at", "updated_at")
        read_only_fields = fields
      
        
class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("receiver",)
        
    def validate_receiver(self, receiver):
        request = self.context["request"]
        
        if receiver == request.user:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")
        
        existing_request = FriendRequest.objects.filter(sender=request.user, receiver=receiver).first()
        
        if (existing_request and existing_request.status != FriendRequest.Status.CANCELLED):
            raise serializers.ValidationError("Friend request already sent.")
        
        return receiver
    
    def create(self, validated_data):
        sender = validated_data["sender"]
        receiver = validated_data["receiver"]
        
        friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, status=FriendRequest.Status.CANCELLED).first()
        
        if friend_request:
            friend_request.status = FriendRequest.Status.PENDING
            friend_request.save(update_fields=["status"])
            return friend_request
            
        return super().create(validated_data)
    
    