from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.request import Request

from core.models import User
from core.serializers import UserSerializer
from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.editable_roles)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    def validate_user(self, user: User) -> User:
        if self.context["request"].user == user:
            raise ValidationError("Failed to change your role")
        return user

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(BoardCreateSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance: Board, validated_data: dict) -> Board:
        request: Request = self.context["request"]

        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(user=request.user).delete()
            BoardParticipant.objects.bulk_create(
                [
                    BoardParticipant(
                        user=participant["user"],
                        role=participant["role"],
                        board=instance
                    )
                    for participant in validated_data.get("participants", [])
                ],
                ignore_conflicts=True,
            )

            if title := validated_data.get("title"):
                instance.title = title

            instance.save()

        return instance


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # board = None

    def validate_board(self, board: Board) -> Board:
        if board.is_deleted:
            raise ValidationError("Board is deleted")

        if not BoardParticipant.objects.filter(
                board_id=board.id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context["request"].user
        ).exists():
            raise PermissionDenied

        return board

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"


class GoalCategorySerializer(GoalCreateSerializer):
    user = UserSerializer(read_only=True)


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError("Category not found")

        if not BoardParticipant.objects.filter(
                board_id=value.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context["request"].user
        ).exists():
            raise PermissionDenied

        return value


class GoalUserSerializer(GoalSerializer):
    user = UserSerializer(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError("Goal not found")
        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context["request"].user
        ).exists():
            raise PermissionDenied("Not owner of category")
        return value


class GoalCommentSerializer(CommentSerializer):
    user = UserSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)
