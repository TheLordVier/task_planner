import pytest
from typing import Any
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User
from tests.factories import SignUpRequest


@pytest.mark.django_db
class TestSignUpView:
    url = reverse('core:signup')

    def test_user_created(self, client):
        """
        Тест на создание пользователя
        """
        data = SignUpRequest.build()
        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get()
        assert response.json() == self._serialize_response(user)
        assert user.check_password(data['password'])

    @pytest.mark.parametrize(
        'password', ['654321', 'test', 'qwerty123456'], ids=['only numbers', 'too short', 'too common']
    )
    def test_password_too_weak(self, client, password):
        """
        Тест на сложность пароля
        """
        data = {
            'password': password,
            'password_repeat': password,
        }
        response = client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_passwords_missmatch(self, client, faker):
        """
        Тест на соответствие паролей password и password_repeat
        """
        data = SignUpRequest.build(password_repeat=faker.password())
        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'non_field_errors': ['password and password_repeat is not equal']}

    @staticmethod
    def _serialize_response(user: User, **kwargs) -> dict:
        data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        return data | kwargs

    def test_user_already_exists(self, client, user):
        """
        Тест на уникальность username для пользователя
        """
        data = SignUpRequest.build(username=user.username)
        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'username': ['A user with that username already exists.']}


@pytest.mark.django_db
class TestProfileView:
    url = reverse('core:profile')

    def test_profile_exists(self, auth_client: APIClient) -> None:
        """
        Тест, что данный профиль существует
        """
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        profile = User.objects.get()
        assert response.json() == self._serialize_response_profile(profile)

    @staticmethod
    def _serialize_response_profile(self, **kwargs: Any) -> dict:
        data = {
            'id': ANY,
            'username': ANY,
            'first_name': ANY,
            'last_name': ANY,
            'email': ANY,
        }
        return data | kwargs

    def test_profile_update(self, auth_client: APIClient) -> None:
        """
        Тест, что пользователь может вносить изменения в свой профиль
        """
        response = auth_client.put(self.url, data={'username': 'username', 'email': 'mail@mail.com'})

        assert response.status_code == status.HTTP_200_OK
        profile = User.objects.get()
        assert response.json() == self._serialize_response_profile_update(profile)

    @staticmethod
    def _serialize_response_profile_update(self, **kwargs: Any) -> dict:
        data = {
            'id': ANY,
            'username': 'username',
            'first_name': ANY,
            'last_name': ANY,
            'email': 'mail@mail.com',
        }
        return data | kwargs

    def test_profile_delete(self, auth_client: APIClient) -> None:
        """
        Тест, что авторизованный пользователь может удалить профиль
        """
        response = auth_client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_profile_delete_not_user(self, client: APIClient) -> None:
        """
        Тест, что не авторизованный пользователь не может удалить профиль
        """
        response = client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestLoginView:
    url = reverse('core:login')

    def test_login_wrong(self, client: APIClient) -> None:
        """
        Тест, что не авторизованный пользователь не залогиниться
        """
        response = client.post(self.url, data={"username": "username", "password": "password"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
