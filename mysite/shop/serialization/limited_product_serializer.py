"""Сериализатор для товаров ограниченного тиража."""

from rest_framework.serializers import ModelSerializer

from .._models import Product
from .image_serialize import ProductImageSerializer


class LimitedProductSerializer(ModelSerializer):

    """
    Сериализует данные товара.

    Для отображения в блоке лимитированных предложений.
    """

    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:

        """Метаданные модели с полями."""

        model = Product
        fields = ["id", "images", "title", "price"]
