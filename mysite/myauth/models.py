"""Модель пользователя."""

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs) -> None:
#     """
#     Обработчик post_save для User.
#
#     :param sender: Класс модели, отправивший сигнал.
#     :param instance: Экземпляр сохранённого пользователя.
#     :param created: True, если объект создан впервые.
#     :param kwargs: Дополнительные аргументы.
#     :return: None
#     """
#     if created:
#         Profile.objects.create(user=instance)


def profile_avatars_directory_path(instance: "Profile", filename: str) -> str:
    """
    Формирует путь для сохранения аватара пользователя.

    :param instance: Экземпляр модели Profile.
    :param filename: Имя загружаемого файла.
    :return: Путь для сохранения файла.
    """
    return f"images_{instance.pk}/avatar/{filename}"


class Profile(models.Model):
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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    fullName = models.CharField(max_length=25, null=False)
    email = models.EmailField(unique=True, null=False, db_index=True)
    phone = models.CharField(
        max_length=12, unique=True, null=True, blank=True, default=""
    )
    avatar = models.ImageField(
        null=True, blank=True, upload_to=profile_avatars_directory_path
    )

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return f"User: {self.user}"
