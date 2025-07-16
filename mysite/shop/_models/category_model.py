"""
Модель категории товаров.

Поддерживает древовидную структуру и загрузку изображений.
"""

from django.db import models

from .soft_delete_model import SoftDeleteModel


def category_image_directory_path(
    instance: "Category",
    filename: str,
) -> str:
    """
    Возвращает путь для сохранения изображения категории.

    Args:
        instance (Category): Экземпляр категории;
        filename (str): Имя файла изображения.

    Returns:
        str: Путь к изображению в директории категории.

    """
    return f"images_{instance.pk}/category/{filename}"


class Category(SoftDeleteModel):

    """
    Модель категории товаров.

    Поддерживает иерархию через связь с родительской категорией.
    """

    title = models.CharField(
        max_length=50,
        null=False,
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.CASCADE,
    )
    src = models.ImageField(
        upload_to=category_image_directory_path,
        null=True,
        blank=True,
    )
    alt = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        """Возвращает строковое представление категории."""
        return str(self.title)
