"""
Модель изображений товаров.

Хранит изображения, связанные с конкретным товаром.
"""

from django.db import models

from .product_model import Product
from .soft_delete_model import SoftDeleteModel


def product_image_directory_path(
    instance: "Product",
    filename: str,
) -> str:
    """
    Возвращает путь для сохранения изображения товара.

    Args:
        instance (Product): Экземпляр товара.
        filename (str): Имя загружаемого файла.

    Returns:
        str: Путь для сохранения файла.

    """
    return f"images_{instance.pk}/product/{filename}"


class ProductImage(SoftDeleteModel):

    """
    Изображение товара.

    Связано с товаром и содержит путь к изображению и alt-текст.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    src = models.ImageField(
        null=True,
        blank=True,
        upload_to=product_image_directory_path,
    )
    alt = models.CharField(
        null=True,
        blank=True,
        max_length=50,
    )

    def __str__(self) -> str:
        """
        Строковое представление изображения.

        Returns:
            str: Название изображения и ID товара.

        """
        return f"Image for {self.product.title} (ID {self.product.id})"
