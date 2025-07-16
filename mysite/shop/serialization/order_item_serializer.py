"""Сериализатор для детального представления заказа с продуктами."""

from rest_framework import serializers

from .._models import Order
from .product_in_cart_serializer import ProductInCartSerializer


class OrderDetailSerializer(serializers.ModelSerializer):

    """
    Детализированная сериализация заказа.

    Включает сведения о покупателе, типах доставки и оплаты,
    списке продуктов и стоимости.
    """

    createdAt = serializers.SerializerMethodField()
    deliveryType = serializers.CharField(source="delivery_type")
    paymentType = serializers.CharField(source="payment_type")
    fullName = serializers.CharField(source="full_name")
    totalCost = serializers.DecimalField(
        source="total_cost",
        max_digits=10,
        decimal_places=2,
    )
    products = serializers.SerializerMethodField()
    delivery_cost = serializers.SerializerMethodField()
    paymentError = serializers.CharField(
        source="payment_error",
        allow_null=True,
        required=False,
    )

    class Meta:

        """Метаданные модели с полями."""

        model = Order
        fields = (
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "city",
            "address",
            "paymentType",
            "status",
            "totalCost",
            "order_items",
            "products",
            "delivery_cost",
            "paymentError",
        )

    def get_products(self, obj: Order) -> list[dict]:
        """Возвращает сериализованный список продуктов в заказе."""
        order_items = obj.order_items.select_related("product").all()
        products = [item.product for item in order_items]

        for product, item in zip(products, order_items):
            product.count = item.quantity

        serializer = ProductInCartSerializer(products, many=True, context=self.context)
        return serializer.data

    def get_delivery_cost(self, obj: Order) -> float:
        """Возвращает стоимость доставки."""
        return obj.get_delivery_cost()

    def get_createdAt(self, obj: Order) -> str:
        """Форматирует дату создания заказа."""
        return obj.created_at.strftime("%Y-%m-%d %H:%M")
