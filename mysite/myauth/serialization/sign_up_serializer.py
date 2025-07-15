"""Сериализаторы для работы с пользователями."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.Serializer):

    """
    Сериализатор для регистрации нового пользователя.

    Поля:
        - name: Необязательное имя пользователя (может быть пустым).
        - username: Уникальное имя пользователя (обязательно).
        - password: Пароль, минимум 8 символов, только для записи..
    """

    name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
    )
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    def validate_username(self, value):
        """Валидирует уникальный username."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists",
            )
        return value

    def create(self, validated_data):
        """
        Создаёт пользователя.

        Сохраняет пароль.
        """
        user = User(
            username=validated_data["username"],
            first_name=validated_data.get("name", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
