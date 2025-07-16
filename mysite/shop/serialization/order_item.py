"""Сериализатор для создания позиции заказа (OrderItem)."""

from rest_framework import serializers

from .._models import OrderItem, Product


class OrderItemCreateSerializer(serializers.ModelSerializer):

    """Сериализатор для создания объекта OrderItem."""

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product"
    )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:

        """Метаданные модели с полями."""

        model = OrderItem
        fields = ("product_id", "quantity")
