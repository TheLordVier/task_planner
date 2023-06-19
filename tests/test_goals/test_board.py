import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.fields import DateTimeField
from rest_framework.response import Response

from rest_framework.test import APIClient
from goals.models import Board
from tests.factories import CreateBoardCategoryRequest


@pytest.mark.django_db
class TestListBoardView:
    url = reverse('goals:board_list')

    def test_list_board(self, auth_client: APIClient) -> None:
        """
        Тест, что авторизованный пользователь получает список своих категорий
        """
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_list_board_not_owner(self, client: APIClient) -> None:
        """
        Тест, что не авторизованный пользователь не получает список категорий
        """
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestBoardCreateView:
    url = reverse('goals:create_board')

    def test_authorization_required(self, client) -> None:
        """
        Тест, что неавторизованный пользователь, не получает доступ к созданию доски
        """
        response: Response = client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_board(self, auth_client):
        """
        Тест, что новая доска создается для авторизованного пользователя
        """
        data = CreateBoardCategoryRequest.build()

        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED


def _serialize_response_board(board: Board, **kwargs) -> dict:
    data = {
        "id": board.id,
        "created": DateTimeField().to_representation(board.created),
        "updated": DateTimeField().to_representation(board.updated),
        "title": board.title,
        "is_deleted": board.is_deleted
    }
    return data | kwargs
