from django.db import transaction
from django.db.models import QuerySet
from rest_framework import generics, filters, permissions

from goals.models import Board, BoardParticipant, Goal
from goals.permissions import BoardPermission
from goals.serializers import BoardCreateSerializer, BoardSerializer


class BoardCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer: BoardCreateSerializer) -> None:
        with transaction.atomic():
            board = serializer.save()
            BoardParticipant.objects.create(
                user=self.request.user,
                board=board,
                role=BoardParticipant.Role.owner
            )


class BoardListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self) -> QuerySet(Board):
        return Board.objects.filter(participants__user=self.request.user).exclude(is_deleted=True)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardSerializer
    queryset = Board.objects.prefetch_related('participants__user').exclude(is_deleted=True)

    def perform_destroy(self, instance: Board) -> None:
        with transaction.atomic():
            Board.objects.filter(id=instance.id).update(is_deleted=True)
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
