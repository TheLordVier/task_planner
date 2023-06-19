import factory
from django.utils import timezone
from pytest_factoryboy import register

from bot.models import TgUser
from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> User:
        return User.objects.create_user(*args, **kwargs)


class DatesFactoryMixin(factory.django.DjangoModelFactory):
    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)

    class Meta:
        abstract = True


@register
class BoardFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')

    class Meta:
        model = Board

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


@register
class BoardParticipantFactory(DatesFactoryMixin):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant


@register
class GoalCategoryFactory(DatesFactoryMixin):
    title = factory.Faker('catch_phrase')
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)

    class Meta:
        model = GoalCategory


@register
class GoalFactory(DatesFactoryMixin):
    title = factory.Faker('catch_phrase')
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)

    class Meta:
        model = Goal


@register
class GoalCommentFactory(factory.django.DjangoModelFactory):
    text = factory.Faker('catch_phrase')
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)

    class Meta:
        model = GoalComment


@register
class TgUserFactory(factory.django.DjangoModelFactory):
    chat_id = factory.Faker('random_int', min=1)

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> User:
        obj = TgUser.objects.create(*args, **kwargs)
        obj.update_verification_code()
        return obj

    class Meta:
        model = TgUser


class SignUpRequest(factory.DictFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    password_repeat = factory.LazyAttribute(lambda repeat: repeat.password)


class LoginRequest(factory.DictFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')


class CreateBoardCategoryRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')


class CreateGoalCategoryRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')


class CreateGoalRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')


class CreateGoalCommentRequest(factory.DictFactory):
    title = factory.Faker('sentence')
