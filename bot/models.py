from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string

USER = get_user_model()


class TgUser(models.Model):
    chat_id = models.BigIntegerField(verbose_name="Telegram чат", primary_key=True, editable=True, unique=True)
    user = models.OneToOneField(USER, verbose_name="Пользователь", on_delete=models.CASCADE,
                                null=True, blank=True
                                )
    verification_code = models.CharField(verbose_name="Верификационный код", max_length=25,
                                         null=True, blank=True
                                         )

    def __str__(self):
        return f"{self.__class__.__name__} {self.chat_id}"

    def update_verification_code(self) -> None:
        self.verification_code = self._generate_verification_code()
        self.save(update_fields=["verification_code"])

    @property
    def is_verified(self) -> bool:
        return bool(self.user)

    @staticmethod
    def _generate_verification_code() -> str:
        return get_random_string(25)

    class Meta:
        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"
