from django.contrib.auth import authenticate, get_user_model
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
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
    
    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "is_active_user")