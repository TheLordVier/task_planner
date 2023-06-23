from typing import Any

import pytest
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.fields import DateTimeField

from goals.models import BoardParticipant, GoalCategory
from tests.factories import CreateGoalCategoryRequest


@pytest.mark.django_db
class TestListGoalCategoryView:
    url = reverse('goals:category_list')

    def test_list_category(self, auth_client: APIClient) -> None:
        """
        Тест, что авторизованный пользователь получает список своих категорий
        """
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_list_category_not_owner(self, client: APIClient) -> None:
        """
        Тест, что не авторизованный пользователь не получает список категорий
        """
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCreateGoalCategoryView:
    url = reverse('goals:create_category')

    def test_authorization_required(self, client) -> None:
        """
        Тест, что неавторизованный пользователь, не получает доступ к созданию категории
        """
        response: Response = client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category_with_role_writer(self, client, board, another_user):
        """
        Тест, что новая категория создается, когда пользователь имеет права редактора
        """
        BoardParticipant.objects.create(board=board, user=another_user, role=BoardParticipant.Role.writer)
        client.force_login(another_user)
        data = CreateGoalCategoryRequest(board=board.id)

        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        new_category = GoalCategory.objects.get()
        assert response.json() == _serialize_response_category(new_category)

    def test_create_category_with_role_reader(self, client, board, another_user):
        BoardParticipant.objects.create(board=board, user=another_user, role=BoardParticipant.Role.reader)
        client.force_login(another_user)
        data = CreateGoalCategoryRequest(board=board.id)

        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category_with_role_owner(self, client, board, another_user):
        """
        Тест, что новая категория создается, когда пользователь является владельцем
        """
        BoardParticipant.objects.create(board=board, user=another_user, role=BoardParticipant.Role.owner)
        client.force_login(another_user)
        data = CreateGoalCategoryRequest(board=board.id)

        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        new_category = GoalCategory.objects.get()
        assert response.json() == _serialize_response_category(new_category)


def _serialize_response_category(goal_category: GoalCategory, **kwargs) -> dict:
    data = {
        'id': goal_category.id,
        'created': DateTimeField().to_representation(goal_category.created),
        'updated': DateTimeField().to_representation(goal_category.updated),
        'title': goal_category.title,
        'is_deleted': goal_category.is_deleted,
        'board': goal_category.board_id,
    }
    return data | kwargs


@pytest.mark.django_db
class TestRetrieveGoalCategoryView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant_factory: Any, goal_category_factory: Any, user: Any) -> None:
        self.url = f"/goals/goal_category/{self._set_data(board_participant_factory, goal_category_factory, user)}"

    @staticmethod
    def _set_data(board_participant_factory: Any, goal_category_factory: Any, user: Any) -> int:
        board_participant = board_participant_factory.create(role=BoardParticipant.Role.owner, user=user)
        goal_category = goal_category_factory.create(board=board_participant.board, user=user)
        return goal_category.id

    def test_authorization_required(self, client: APIClient) -> None:
        """
        Тест, что неавторизованный пользователь, не получает доступ к категории
        """
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_auth(self, auth_client: APIClient) -> None:
        """
        Тест, что авторизованный пользователь может просмотреть свою категорию
        """
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_deleted_owner_category(self, auth_client: APIClient) -> None:
        """
        Тест, что авторизованный пользователь может удалить категорию
        """
        response = auth_client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_deleted_not_owner_category(self, client: APIClient) -> None:
        """
        Тест, что не авторизованный пользователь не может удалить категорию
        """
        response = client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
