import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status

from bot.tg.client import TgClient
from core.models import User


@pytest.mark.django_db
class TestTgUser:
    url = reverse('bot:verify')

    def test_bot_telegram_user_verified(self, auth_client, user: User, tg_user_factory):
        """
        Тест верификации пользователя
        """
        tg_user = tg_user_factory.create(user=None)
        data = {'verification_code': tg_user.verification_code}

        with patch.object(TgClient, 'send_message'):
            response = auth_client.patch(self.url, data=data)

        assert response.status_code == status.HTTP_200_OK
        tg_user.refresh_from_db()
        assert tg_user.user == user

    def test_bot_telegram_invalid_verification_code(self, tg_user_factory, auth_client):
        """
        Тест проверка на неверный верификационный код
        """
        tg_user = tg_user_factory.create(verification_code='code')
        data = {'verification_code': 'Invalid verification code'}

        with patch.object(TgClient, 'send_message') as mock:
            response = auth_client.patch(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        tg_user.refresh_from_db()
        assert tg_user.user is None
        mock.assert_not_called()

    def test_bot_telegram_send_message(self, auth_client, tg_user):
        """
        Тест, что верифицированный пользователь может отправлять запросы Телеграм боту
        """
        data = {'verification_code': tg_user.verification_code}

        with patch.object(TgClient, 'send_message') as mock:
            response = auth_client.patch(self.url, data=data)

        assert response.status_code == status.HTTP_200_OK
        mock.assert_called_once_with(tg_user.chat_id, 'Bot token verified!')
