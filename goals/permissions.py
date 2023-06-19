from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.request import Request

from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


class BoardPermission(IsAuthenticated):
    """
    Класс BoardPermission служит для ограничения доступа к доске для пользователей,
    кто отсутствует в списке участников
    """
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Board) -> bool:
        _filters: dict[str, Any] = {"user": request.user, "board": obj}
        if request.method not in SAFE_METHODS:
            _filters["role"] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermission(IsAuthenticated):
    """
    Класс GoalCategoryPermission служит для ограничения доступа к категории для
    пользователей, которые не имеют роль редактор или владелец
    """
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalCategory) -> bool:
        _filters: dict[str, Any] = {"user": request.user, "board": obj.board}
        if request.method not in SAFE_METHODS:
            _filters["role__in"] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalPermission(IsAuthenticated):
    """
    Класс GoalPermission служит для ограничения доступа к цели для
    пользователей, которые не имеют роль редактор или владелец
    """
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Goal) -> bool:
        _filters: dict[str, Any] = {"user": request.user, "board": obj.category.board}
        if request.method not in SAFE_METHODS:
            _filters["role__in"] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCommentPermission(IsAuthenticated):
    """
    Класс GoalCommentPermission служит для ограничения доступа к комментариям,
    для не авторизованных пользователей
    """
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalComment) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
