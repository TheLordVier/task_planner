import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListGoalCommentView:
    url = reverse('goals:comment_list')

    def test_list_comments(self, auth_client: APIClient) -> None:
        """
        Тест, что авторизованный пользователь получает список комментариев
        """
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_list_test_list_comments_not_owner(self, client: APIClient) -> None:
        """
        Тест, что не авторизованный пользователь не получает список комментариев
        """
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
