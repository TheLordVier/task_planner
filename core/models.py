from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = []
    # pass

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ["username"]
