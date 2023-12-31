from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from tauth.enum import TokenType


def get_user_from_token(payload):
    user_id = payload.get('id')
    if user_id is None:
        raise AuthenticationFailed('User not found.')

    user_model = get_user_model()

    try:
        user = user_model.objects.get(id=user_id)
    except user_model.DoesNotExist:
        raise AuthenticationFailed('User not found.')

    return user


class TAuthJWTAuthentication(BaseAuthentication):


    def authenticate(self, request):
        # import pdb;pdb.set_trace()
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if not authorization_header:
            return None

        # Check that the header starts with "Bearer"
        if not authorization_header.startswith('Bearer'):
            return None
        token = authorization_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != TokenType.access.name:
                raise AuthenticationFailed('This token is not valid for Authentication.')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token is invalid.')
        return get_user_from_token(payload), None


def t_auth_active_token_verify(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if payload.get('type') != TokenType.active.name:
            raise AuthenticationFailed('This token is not valid for Activation.')
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired.')
    except jwt.DecodeError:
        raise AuthenticationFailed('Token is invalid.')
    return get_user_from_token(payload)


def t_auth_reset_token_verify(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        if payload.get('type') != TokenType.reset.name:
            raise AuthenticationFailed(f'This token is not valid for reset password.')
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired.')
    except jwt.DecodeError:
        raise AuthenticationFailed('Token is invalid.')
    return get_user_from_token(payload)
