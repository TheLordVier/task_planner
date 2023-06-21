from typing import Callable, Any
from unittest.mock import ANY

import pytest
from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response


from rest_framework.test import APIClient
from goals.models import Board, BoardParticipant


@pytest.fixture
def board_create_data(faker: Faker) -> Callable:
    def _wrapper(**kwargs: Any) -> dict:
        data = {"title": faker.sentence(2)}
        data |= kwargs
        return data
    return _wrapper


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

    def test_failed_to_create_deleted_board(self, auth_client: APIClient, board_create_data: Any) -> None:
        """
        Тест, что нельзя создать удаленную доску
        """
        response = auth_client.post(self.url, data=board_create_data(is_deleted=False))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._serializer_board_response(is_deleted=False)
        assert Board.objects.last().is_deleted is False

    def test_request_user_became_board_owner(self, auth_client: APIClient, user: Any, board_create_data: Any) -> None:
        """
        Тест, что пользователь с правами владельца может создать доску
        """
        response = auth_client.post(self.url, data=board_create_data())

        assert response.status_code == status.HTTP_201_CREATED
        board_participant = BoardParticipant.objects.get(user_id=user.id)
        assert board_participant.board_id == response.data["id"]
        assert board_participant.role == BoardParticipant.Role.owner

    def _serializer_board_response(self, **kwargs: Any) -> dict:
        data = {
            "id": ANY,
            "created": ANY,
            "updated": ANY,
            "title": ANY,
            "is_deleted": True
        }
        data |= kwargs
        return data


@pytest.mark.django_db
class TestRetrieveBoardView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant: Any) -> None:
         self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int) -> str:
        return f"/goals/board/{board_pk}"

    def test_authorization_required(self, client: APIClient) -> None:
        """
        Тест, который проверяет, что пользователь авторизован, если нет то получаем ошибку
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_deleted_board(self, auth_client: APIClient, board: Any) -> None:
        """
        Тест, который проверяет можно ли посмотреть удаленную доску
        """
        board.is_deleted = True
        board.save()
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_foreign_board(self, client: APIClient, user_factory: Any) -> None:
        """
        Тест, который проверяет можно ли получить доступ не к своей доске
        """
        another_user = user_factory.create()
        client.force_login(another_user)

        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDestroyBoardView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant: Any) -> None:
         self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int) -> str:
        return f"/goals/board/{board_pk}"

    def test_authorization_required(self, client: APIClient) -> None:
        """
        Тест, который проверяет, что пользователь авторизован, если нет то получаем ошибку
        """
        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("role", [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.reader,
    ], ids=["writer", "reader"])
    def test_not_owner_deleted_board(self, client: APIClient, user_factory: Any,
                                     board: Any, board_participant_factory: Any, role: str) -> None:
        """
        Тест, который проверяет, может ли не владелец доски удалить её
        """
        another_user = user_factory.create()
        board_participant_factory.create(user=another_user, board=board, role=role)
        client.force_login(another_user)

        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_deleted_board(self, auth_client: APIClient,  board: Any) -> None:
        """
        Тест, который проверяет, может ли владелец удалить доску
        """
        response = auth_client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        board.refresh_from_db()
        assert board.is_deleted is True
