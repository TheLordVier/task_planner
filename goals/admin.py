from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from goals.models import Board, BoardParticipant, GoalCategory, GoalComment, Goal


class ParticipantsInLine(admin.TabularInline):
    model = BoardParticipant
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(role=BoardParticipant.Role.owner)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'participants_count', 'is_deleted')
    list_display_links = ['title']
    list_filter = ['is_deleted']
    search_fields = ['title']
    inlines = [ParticipantsInLine]

    def participants_count(self, obj: Board) -> int:
        return obj.participants.exclude(role=BoardParticipant.Role.owner).count()


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ['is_deleted']
    readonly_fields = ('created', 'updated')
    search_fields = ['title']


class CommentInLine(admin.StackedInline):
    model = GoalComment
    extra = 0


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author_goal')
    search_fields = ('title', 'description')
    readonly_fields = ('created', 'updated')
    list_filter = ('status', 'priority')
    inlines = [CommentInLine]

    def author_goal(self, obj: Goal) -> str:
        return format_html(
            "<a href='{url}'>{user_name}</a>",
            url=reverse('admin:core_user_change', kwargs={'object_id': obj.user_id}),
            user_name=obj.user.username
        )

    author_goal.short_description = 'Author'
