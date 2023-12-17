import http
import os
import uuid

import jwt
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from jwt import DecodeError, ExpiredSignatureError

User = get_user_model()
admin_roles_names = set(
    name.strip() for name in os.environ.get('SUPER_ROLES_NAME').split(',')
)


def decode_token(token: str) -> dict:
    """Расшифровка полезной нагрузки JWT токена.

    Args:
        token: jwt токен.

    Returns:
        словарь полезной нагрузки токена.
    """
    return jwt.decode(token, options={"verify_signature": False})


class CustomBackend(BaseBackend):
    """Бэкенд для аутенификации через сторонний сервис."""

    def authenticate(
            self,
            request:  HttpRequest | None,
            username: str = None,
            password: str = None,
    ) -> User | None:
        """Аутентификация через сторонний сервис.

        Args:
            request: объект запроса или None;
            username: адрес электронной почты;
            password: пароль пользователя.

        Returns:
            объект пользователя или None.
        """
        url = settings.AUTH_API_LOGIN_URL
        payload = {
            'username': username,
            'password': password,
        }
        response = requests.post(
            url=url,
            data=payload,
            headers={'X-Request-Id': str(uuid.uuid4())},
        )
        if response.status_code != http.HTTPStatus.OK:
            return

        data = response.json()
        access_token = data['access_token']
        try:
            token_data = decode_token(access_token)
        except (DecodeError, ExpiredSignatureError):
            return

        role = token_data.get('role_name')
        if role not in admin_roles_names:
            return

        user, _ = User.objects.get_or_create(
            email=username,
            defaults={'is_staff': True, 'is_superuser': True},
        )
        return user

    def get_user(self, user_id: int) -> User | None:
        """Получение объекта пользователя.

        Args:
            user_id: id пользователя.

        Returns:
            объект пользователя или None.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
