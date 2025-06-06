from django.db import models

from .soft_delete_model import SoftDeleteModel


def category_image_directory_path(instance: "Category", filename: str) -> str:
    """
    Путь для изображений товара.
    """
    return f"images_{instance.pk}/category/{filename}"


class Category(SoftDeleteModel):

    title = models.CharField(max_length=50, null=False)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.CASCADE
    )
    src = models.ImageField(
        upload_to=category_image_directory_path,
        null=True,
        blank=True
    )
    alt = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title
