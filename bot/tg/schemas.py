from pydantic import BaseModel


class Chat(BaseModel):
    """
    Чат пользователя
    """
    id: int


class Message(BaseModel):
    """
    Сообщения
    """
    chat: Chat
    text: str | None = None


class UpdateObj(BaseModel):
    """
    Обновление данных
    """
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    """
    Получения ответа об обновлениях
    """
    ok: bool
    result: list[UpdateObj]


class SendMessageResponse(BaseModel):
    """
    Отправка сообщений
    """
    ok: bool
    result: Message
