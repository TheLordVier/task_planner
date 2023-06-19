from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from goals.filters import GoalListFilter
from goals.models import Goal
from goals.permissions import GoalPermission
from goals.serializers import GoalSerializer, GoalUserSerializer


class GoalCreateView(generics.CreateAPIView):
    """
    Представление для создания новой цели
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer


class GoalListView(generics.ListAPIView):
    """
    Представление для отображения списка всех доступных целей
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalUserSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = GoalListFilter
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
        ).exclude(status=Goal.Status.archived)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для отображения, обновления и удаления конкретной цели
    """
    permission_classes = [GoalPermission]
    serializer_class = GoalUserSerializer
    queryset = Goal.objects.exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal) -> None:
        instance.status = Goal.Status.archived
        instance.save(update_fields=['status'])
