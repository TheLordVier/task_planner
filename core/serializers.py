from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, ValidationError

User_Model = get_user_model()


class PasswordField(serializers.CharField):
    """
    Сериализатор проверки создания/изменения пароля
    """
    def __init__(self, **kwargs):
        kwargs["style"] = {"input_type": "password"}
        kwargs.setdefault("write_only", True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации
    """
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User_Model
        read_only_fields = ("id",)
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_repeat",
        )

    def validate(self, attrs: dict):
        if attrs["password"] != attrs["password_repeat"]:
            raise ValidationError("password and password_repeat is not equal")
        return attrs

    def create(self, validated_data: dict) -> User_Model:
        del validated_data["password_repeat"]
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """
    Сериализатор авторизации
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        if not (user := authenticate(
                username=validated_data["username"],
                password=validated_data["password"],

        )):
            raise AuthenticationFailed
        return user

    class Meta:
        model = User_Model
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор отображения информации о пользователе
    """
    class Meta:
        model = User_Model
        fields = ("id", "username", "first_name", "last_name", "email")


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Сериализатор обновления пароля
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if not (user := attrs["user"]):
            raise NotAuthenticated
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": "incorrect password"})
        return attrs

    def create(self, validated_data: dict):
        raise NotImplementedError

    def update(self, instance: user, validated_data):
        instance.password = make_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance
