from django.db import models

from core.models import User
from todolist.models import BaseModel


class GoalCategory(BaseModel):
    title = models.CharField(verbose_name="Название", max_length=260)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Goal(BaseModel):
    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(verbose_name="Название", max_length=260)
    description = models.TextField(blank=True)
    category = models.ForeignKey(to=GoalCategory, on_delete=models.PROTECT)
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"


class GoalComment(BaseModel):
    text = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    goal = models.ForeignKey(to=Goal, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
