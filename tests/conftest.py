import pytest
from rest_framework.test import APIClient

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> APIClient:
    """
    Экземпляр тестового клиента Rest Framework
    """
    return APIClient()


@pytest.fixture()
def auth_client(client, user):
    """
    Аутентифицированный клиент Rest Framework
    """
    client.force_login(user)
    return client


@pytest.fixture()
def another_user(user_factory):
    return user_factory.create()
