from django.urls import path

from goals.views.goal_category import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView
from goals.views.goals import GoalCreateView, GoalListView, GoalDetailView
from goals.views.goal_comment import GoalCommentCreateView, GoalCommentDetailView, GoalCommentListView

urlpatterns = [
    # Category
    path("goal_category/create", GoalCategoryCreateView.as_view(), name='create_category'),
    path("goal_category/list", GoalCategoryListView.as_view(), name='category_list'),
    path("goal_category/<int:pk>", GoalCategoryView.as_view(), name='category_detail'),
    # Goals
    path("goal/create", GoalCreateView.as_view(), name='create_goal'),
    path("goal/list", GoalListView.as_view(), name='goal_list'),
    path("goal/<int:pk>", GoalDetailView.as_view(), name='goal_detail'),
    # Comments
    path("goal_comment/create", GoalCommentCreateView.as_view(), name='comment_create'),
    path("goal_comment/list", GoalCommentListView.as_view(), name='comment_list'),
    path("goal_comment/<int:pk>", GoalCommentDetailView.as_view(), name='comment_detail'),
]
