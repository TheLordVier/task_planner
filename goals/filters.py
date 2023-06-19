from django_filters.rest_framework import FilterSet

from goals.models import Goal


class GoalListFilter(FilterSet):
    """
    Класс для фильтрации по дате дедлайна, категории, статусу и приоритету
    """
    class Meta:
        model = Goal
        fields = {
            'due_date': ['lte', 'gte'],
            'category': ['in'],
            'status': ['in'],
            'priority': ['in'],
        }
