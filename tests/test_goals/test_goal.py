import pytest
from typing import Any
from django.urls import reverse
from rest_framework import status
from rest_framework.fields import DateTimeField
from rest_framework.response import Response
from rest_framework.test import APIClient

from goals.models import BoardParticipant, Goal
from tests.factories import CreateGoalRequest


@pytest.mark.django_db
class TestCreateGoalView:
    url = reverse('goals:create_goal')

    def test_authorization_required(self, client) -> None:
        """
        Тест, что неавторизованный пользователь, не получает доступ к созданию цели
        """
        response: Response = client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_goal_if_not_participant(self, auth_client, goal_category, faker):
        """
        Тест, что пользователь без прав редактора или владельца не может создать цель
        """
        data = CreateGoalRequest.build(category=goal_category.id)

        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Must be owner or writer in project'}

    def test_failed_to_create_goal_if_reader(self, auth_client, board_participant, goal_category, faker):
        """
        Тест, что пользователь с правами читатель не может создать цель
        """
        board_participant.role = BoardParticipant.Role.reader
        board_participant.save(update_fields=['role'])
        data = CreateGoalRequest.build(category=goal_category.id)

        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Must be owner or writer in project'}

    @pytest.mark.parametrize('role', [BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                             ids=['owner', 'writer'])
    def test_create_goal_with_roles_owner_or_writer(self, auth_client, board_participant, goal_category, faker, role):
        """
        Тест, что новая цель создается, когда пользователь имеет права редактора или владельца
        """
        board_participant.role = role
        board_participant.save(update_fields=['role'])
        data = CreateGoalRequest.build(category=goal_category.id)

        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        new_goal = Goal.objects.get()
        assert response.json() == _serialize_response_goal(new_goal)

    @pytest.mark.usefixtures('board_participant')
    def test_create_goal_on_deleted_category(self, auth_client, goal_category):
        """
        Тест, что цель не может быть создана на удалённой категории
        """
        goal_category.is_deleted = True
        goal_category.save(update_fields=['is_deleted'])
        data = CreateGoalRequest.build(category=goal_category.id)

        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'category': ['Category not found']}

    @pytest.mark.usefixtures('board_participant')
    def test_create_goal_on_not_exiting_category(self, auth_client):
        """
        Тест, что цель не может быть создана на несуществующей категории
        """
        data = CreateGoalRequest.build(category=1)

        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'category': ['Invalid pk "1" - object does not exist.']}


def _serialize_response_goal(goal: Goal, **kwargs) -> dict:
    data = {
        'id': goal.id,
        'category': goal.category_id,
        'created': DateTimeField().to_representation(goal.created),
        'updated': DateTimeField().to_representation(goal.updated),
        'title': goal.title,
        'description': goal.description,
        'due_date': DateTimeField().to_representation(goal.due_date),
        'status': goal.status,
        'priority': goal.priority
    }
    return data | kwargs


@pytest.mark.django_db
class TestListGoalView:
    url = reverse('goals:goal_list')

    def test_list_goals(self, auth_client: APIClient) -> None:
        """
        Тест, что авторизованный пользователь получает список своих целей
        """
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_list_goals_not_owner(self, client: APIClient) -> None:
        """
        Тест, что не авторизованный пользователь не получает список целей
        """
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestRetrieveGoalView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant_factory: Any, goal_category_factory: Any, user: Any, goal_factory: Any) -> None:
        self.url = f"/goals/goal/{self._set_data(board_participant_factory, goal_category_factory, user, goal_factory).id}"

    @staticmethod
    def _set_data(board_participant_factory: Any, goal_category_factory: Any, user: Any, goal_factory: Any) -> Goal:
        board_participant = board_participant_factory.create(role=BoardParticipant.Role.owner, user=user)
        goal_category = goal_category_factory.create(board=board_participant.board, user=user)
        goal = goal_factory.create(category=goal_category, user=user)
        return goal

    def test_authorization_required(self, client: APIClient) -> None:
        """
        Тест, что неавторизованный пользователь, не получает доступ к цели
        """
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_auth(self, auth_client: APIClient) -> None:
        """
        Тест, который проверяет авторизован ли пользователь
        """
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_deleted_owner_category(self, auth_client: APIClient) -> None:
        """
        Тест, который проверяет, что авторизованный пользователь (владелец) может удалить категорию
        """
        response = auth_client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_deleted_not_owner_category(self, client: APIClient) -> None:
        """
        Тест, который проверяет что не владелец категории не может удалить её
        """
        response = client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
