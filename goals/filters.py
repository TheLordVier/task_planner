from django_filters.rest_framework import FilterSet

from goals.models import Goal


class GoalListFilter(FilterSet):
    class Meta:
        model = Goal
        fields = {
            'due_date': ['lte', 'gte'],
            'category': ['in'],
            'status': ['in'],
            'priority': ['in'],
        }
