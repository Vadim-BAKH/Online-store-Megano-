"""Сериализаторы для модели профиля пользователя."""

from rest_framework import serializers

from ..models import Profile
from .avatar_serializer import AvatarField


class ProfileSerializer(serializers.ModelSerializer):

    """
    Сериализатор профиля пользователя.

    Включает следующие поля:
        - fullName: Полное имя пользователя.
        - email: Электронная почта.
        - phone: Телефонный номер.
        - avatar: Кастомное поле аватара (обрабатывается через AvatarField).
    """

    avatar = AvatarField(source="*")

    class Meta:

        """Метаданные модели с полями."""

        model = Profile
        fields = (
            "fullName",
            "email",
            "phone",
            "avatar",
        )
