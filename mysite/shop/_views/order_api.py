"""Создание заказа на основе содержимого корзины."""

from django.db import transaction
from loguru import logger
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .._models import Order, OrderItem
from .basket_api import BasketAPIView


class CreateOrderView(APIView):

    """Обрабатывает создание нового заказа из корзины."""

    @transaction.atomic
    def post(self, request: Request) -> Response:
        """
        Создаёт заказ на основе текущей корзины пользователя или гостя.

        Возвращает:
            Response: JSON-ответ с ошибкой, если корзина пуста,
            или пустой успешный ответ.
        """
        cart = BasketAPIView().get_cart(request)
        if not cart.items.exists():
            return Response({"detail": "Корзина пуста"}, status=400)

        user = request.user if request.user.is_authenticated else None

        logger.debug("Создаем заказ для user: '{}'", user or "гостя")

        order = Order.objects.create(
            user=user,
            full_name="",
            email="",
            phone="",
            delivery_type="delivery",
            city="",
            address="",
            payment_type="",
            total_cost=0,
            status="new",
        )
        logger.debug("Создаем заказ '{}'", order)
        total = 0
        for cart_item in cart.items.select_related("product").all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )
            total += cart_item.product.price * cart_item.quantity

        delivery_cost = order.get_delivery_cost()
        order.total_cost = total + delivery_cost
        order.cart = cart
        order.save()
        if not request.user.is_authenticated:
            request.session["guest_order_id"] = order.id
            logger.debug("🧷 Гостевой заказ сохранён в сессию: '{}'", order.id)

        logger.debug("Вид заказа '{}'", order)

        cart.items.all().delete()
        cart.delete()

        return Response({"orderId": order.id}, status=201)
