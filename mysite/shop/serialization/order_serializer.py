"""Сериализатор для обновления заказа и его позиций."""

from loguru import logger
from rest_framework import serializers

from .._models import Order, OrderItem
from .order_item import OrderItemCreateSerializer


class OrderUpdateSerializer(serializers.ModelSerializer):

    """
    Сериализатор для обновления заказа, включая позиции (order_items).

    При передаче новых позиций они заменяют текущие.
    """

    def __init__(self, *args, **kwargs):
        """
        Делает поля необязательными при частичном обновлении (PATCH).

        Это позволяет передавать только те поля, которые нужно изменить.
        """
        super().__init__(*args, **kwargs)
        if self.partial:
            for field_name in [
                "full_name",
                "delivery_type",
                "payment_type",
                "status",
            ]:
                self.fields[field_name].required = False

    order_items = OrderItemCreateSerializer(
        many=True
    )  # source не нужен, имя совпадает с моделью
    full_name = serializers.CharField()
    delivery_type = serializers.CharField()
    payment_type = serializers.CharField()
    status = serializers.CharField()

    class Meta:

        """Метаданные модели с полями."""

        model = Order
        fields = (
            "full_name",
            "email",
            "phone",
            "delivery_type",
            "city",
            "address",
            "payment_type",
            "status",
            "order_items",
        )

    def update(self, instance: Order, validated_data: dict) -> Order:
        """
        Обновляет заказ и связанные позиции заказа.

        Если передан список order_items — старые удаляются и создаются новые.
        Пересчитывает total_cost с учётом доставки.
        """
        logger.debug("✅ ВАЛИДИРОВАННЫЕ ДАННЫЕ:")
        for attr, value in validated_data.items():
            logger.debug("  - '{}' = '{}'", attr, value)

        order_items_data = validated_data.pop("order_items", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if order_items_data is not None:
            instance.order_items.all().delete()
            total = 0
            for item in order_items_data:
                product = item["product"]
                quantity = item["quantity"]
                OrderItem.objects.create(
                    order=instance, product=product, quantity=quantity
                )
                total += product.price * quantity

            delivery_cost = instance.get_delivery_cost()
            instance.total_cost = total + delivery_cost

        logger.debug(
            "💾 Сохраняю заказ с delivery_type = '{}', payment_type = '{}'",
            instance.delivery_type,
            instance.payment_type,
        )
        instance.save()
        return instance
        # logger.debug("Validated data: {}", validated_data)
        #
        # order_items_data = validated_data.pop("order_items", None)
        #
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        # instance.save()
        #
        # if order_items_data is not None:
        #     instance.order_items.all().delete()
        #     total = 0
        #     for item in order_items_data:
        #         product = item["product"]
        #         quantity = item["quantity"]
        #         OrderItem.objects.create(
        #             order=instance, product=product, quantity=quantity
        #         )
        #         total += product.price * quantity
        #
        #     delivery_cost = instance.get_delivery_cost()
        #     instance.total_cost = total + delivery_cost
        #     instance.save()
        #
        # return instance
