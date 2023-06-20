from typing import Any

from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationCodeView(generics.GenericAPIView):
    """
    Представление для верификации пользователя Telegram
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = TgUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tg_user: TgUser = serializer.save(user=request.user)

        TgClient().send_message(tg_user.chat_id, "Bot token verified!")

        return Response(serializer.data)
