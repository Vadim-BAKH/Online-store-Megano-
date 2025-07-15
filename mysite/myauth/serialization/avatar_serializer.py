"""Кастомный сериализатор поля аватара."""

from typing import TYPE_CHECKING

from rest_framework import serializers

if TYPE_CHECKING:
    from ..models import Profile


class AvatarField(serializers.Serializer):

    """
    Сериализатор поля аватара.

    Возвращает объект с URL и альтернативным текстом:
    """

    src = serializers.SerializerMethodField()
    alt = serializers.SerializerMethodField()

    def get_src(self, obj: "Profile") -> str | None:
        """
        Возвращает URL изображения аватара, если он существует.

        Args:
            obj: Объект модели (например, Profile).

        Returns:
            str | None: URL изображения или None, если аватар не задан.

        """
        if obj.avatar:
            return obj.avatar.url
        return None

    def get_alt(self, obj: "Profile") -> str:
        """
        Возвращает текст альтернативы для изображения аватара.

        Args:
            obj: Объект модели (например, Profile).

        Returns:
            str: Альтернативный текст.

        """
        return f"Avatar for {obj.fullName}"
