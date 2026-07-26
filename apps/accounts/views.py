from django.shortcuts import render
from dj_rest_auth.views import LoginView
from drf_spectacular.utils import extend_schema
from apps.accounts.serializers import LoginResponseSerializer, LoginUserSerializer


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
