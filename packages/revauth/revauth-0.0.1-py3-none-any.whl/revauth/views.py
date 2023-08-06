from rest_framework import views, response, permissions, generics
from revauth import exceptions
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from revauth.settings import api_settings
from .serializers import RegisterSerializer, SocialSerializer, ValidationSerializer
from revauth import exceptions
from revauth.jwt import JWTCryptor
from revauth.socials import SocialSDK
from rest_framework import views
from django.conf import settings
from urllib.parse import urlparse


class ValidationView(views.APIView):
    permission_classes = ()
    serializer_class = ValidationSerializer
    handler_class = api_settings.DEFAULT_HANDLER_CLASS

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']
        handler = self.handler_class()
        result = handler.validate(identity)
        return response.Response(result, 200)


class UserRegister(views.APIView):
    profile_class = api_settings.DEFAULT_PROFILE_CLASS
    permission_classes = ()
    serializer_class = api_settings.DEFAULT_REGISTER_SERIALIZER
    handler_class = api_settings.DEFAULT_HANDLER_CLASS

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response.Response({'error': 'not valid'})

        try:
            decoded = JWTCryptor().decode(token)
        except:
            raise exceptions.JWTDecodeError

        handler = self.handler_class()
        return handler.perform_register(decoded=decoded, **serializer.validated_data)


class BaseSocialView(views.APIView):
    permission_classes = ()
    provider = None
    serializer_class = SocialSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = SocialSDK(social_type=self.provider)
        return client.login(serializer.validated_data['token'])


class FacebookLogin(BaseSocialView):
    provider = 'facebook'


class GoogleLogin(BaseSocialView):
    provider = 'google'
