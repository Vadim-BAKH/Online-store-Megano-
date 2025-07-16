"""Сериализация количества и товаров для корзины.."""

from rest_framework import serializers

from .._models import CartItem
from .product_in_cart_serializer import ProductInCartSerializer


class CartItemSerializer(serializers.ModelSerializer):

    """Сериализует сведения о товарах для корзины."""

    product = ProductInCartSerializer()

    class Meta:

        """Метаданные модели с полями."""

        model = CartItem
        fields = (
            "product",
            "quantity",
        )
