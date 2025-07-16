"""Миксин для отображения превью изображения в админке."""

from django.db.models import Model
from django.utils.html import format_html


class ImagePreviewMixin:

    """
    Добавляет поле `image_preview`.

    Отображение миниатюры изображения.
    """

    readonly_fields = ("image_preview",)

    def image_preview(self, obj: Model) -> str:
        """
        Возвращает HTML для отображения изображения, если оно есть.

        Args:
            obj (Model): Объект модели, у которого должно быть поле `src`.

        Returns:
            str: HTML <img> или дефис, если изображение отсутствует.

        """
        if obj and getattr(obj, "src", None):
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.src.url,
            )
        return "-"

    image_preview.short_description = "Превью"
