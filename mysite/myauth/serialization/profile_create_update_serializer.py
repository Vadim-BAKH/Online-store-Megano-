"""Сериализатор для обновления профиля пользователя."""

from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from ..models import Profile


class ProfileUpdateSerializer(
    serializers.ModelSerializer,
):

    """
    Сериализатор обновления профиля пользователя.

    Поля:
        - fullName: Полное имя.
        - email: Электронная почта.
        - phone: Телефонный номер.
        - avatar: Аватар, изображение до 2 МБ.
    """

    avatar = serializers.ImageField(required=False)

    class Meta:

        """Метаданные модели с полями."""

        model = Profile
        fields = (
            "fullName",
            "email",
            "phone",
            "avatar",
        )

    def validate_avatar(self, value: UploadedFile) -> UploadedFile:
        """
        Проверяет, что размер изображения не превышает 2 МБ.

        Args:
            value: Загружаемый файл (изображение).

        Returns:
            File: Проверенное изображение.

        Raises:
            ValidationError: Если файл больше 2 МБ.

        """
        max_size = 2 * 1024 * 1024  # 2 МБ
        if value.size > max_size:
            raise serializers.ValidationError(
                "Размер аватара не должен превышать 2 МБ."
            )
        return value
        max_size = 2 * 1024 * 1024  # 2 МБ
        if value.size > max_size:
            raise serializers.ValidationError(
                "Размер аватара не должен превышать 2 МБ."
            )
        return value
