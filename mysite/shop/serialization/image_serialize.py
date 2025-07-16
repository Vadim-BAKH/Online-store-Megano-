"""Сериализатор для изображений товара."""

from rest_framework import serializers

from .._models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):

    """Сериализует изображение товара (src и alt)."""

    class Meta:

        """Метаданные модели с полями."""

        model = ProductImage
        fields = (
            "src",
            "alt",
        )
