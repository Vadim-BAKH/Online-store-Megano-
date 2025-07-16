"""Сериализация корзины."""

from rest_framework import serializers

from .._models import Cart
from .cart_item_serializer import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):

    """Сериализует модель корзины."""

    items = CartItemSerializer(many=True)

    class Meta:

        """Метаданные модели с полями."""

        model = Cart
        fields = (
            "id",
            "items",
        )
