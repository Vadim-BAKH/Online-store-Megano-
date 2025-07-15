"""Модель пользователя."""

from django.conf import settings
from django.db import models
from shop.models import SoftDeleteModel


def profile_avatars_directory_path(
    instance: "Profile",
    filename: str,
) -> str:
    """
    Формирует путь для сохранения аватара пользователя.

    :param instance: Экземпляр модели Profile.
    :param filename: Имя загружаемого файла.
    :return: Путь для сохранения файла.
    """
    return f"images_{instance.pk}/avatar/{filename}"


class Profile(SoftDeleteModel):

    """
    Модель профиля пользователя.

    Attributes:
        fullName (AUTH_USER_MODEL): Связанный пользователь.
        email (str): Email пользователя.
        phone (str): Телефон пользователя.
        avatar (ImageField): Аватар пользователя.

    """

    class Meta:

        """
        Метаданные модели Profile.

        Задает порядок сортировки по полю fullName.
        """

        ordering = ("fullName",)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    fullName = models.CharField(max_length=25, null=False)
    email = models.EmailField(unique=True, null=False, db_index=True)
    phone = models.CharField(
        max_length=12, unique=True, null=True, blank=True, default=""
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=profile_avatars_directory_path,
    )

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return f"User: {self.user}"
