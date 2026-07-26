from django.contrib.auth import authenticate, get_user_model
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

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