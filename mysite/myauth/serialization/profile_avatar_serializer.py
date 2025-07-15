"""Кастомный сериализатор поля аватара."""

from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from ..models import Profile


class AvatarSerializer(serializers.ModelSerializer):

    """
    Сериализатор для поля аватара.

    Используется для загрузки и валидации изображения аватара
    пользователя. Включает проверку на максимальный размер файла.
    """

    class Meta:

        """Метаданные модели."""

        model = Profile
        fields = ("avatar",)

    def validate_avatar(self, value: UploadedFile) -> UploadedFile:
        """
        Проверяет, что размер изображения не превышает 2 МБ.

        Args:
            value (UploadedFile): Загруженное изображение.

        Returns:
            UploadedFile: Проверенный файл.

        Raises:
            ValidationError: Если размер превышает допустимый лимит.

        """
        max_size = 2 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                "Размер аватара не должен превышать 2 МБ."
            )
        return value
