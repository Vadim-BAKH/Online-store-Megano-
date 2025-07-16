"""Обработка получения и обновления заказа по его ID."""

from django.db import transaction
from django.db.models import Prefetch
from django.http import Http404
from loguru import logger
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .._models import Order, OrderItem
from ..serialization import OrderDetailSerializer, OrderUpdateSerializer


class OrderDetailView(APIView):

    """
    APIView для просмотра и оформления заказа по ID.

    Поддерживает:
      - GET: получить детали заказа
      - POST: частично обновить заказ (оформление)
    """

    def get_object(self, request: Request, id: int) -> Order:
        """
        Возвращает объект заказа, если у пользователя есть к нему доступ.

        Проверка доступа:
        - Авторизованный пользователь должен быть владельцем заказа.
        - Гость — владелец заказа с ID, сохранённым в сессии.
        """
        try:
            order = (
                Order.objects.prefetch_related(
                    Prefetch(
                        "order_items",
                        queryset=OrderItem.objects.select_related("product"),
                    )
                )
                .select_related("cart")
                .get(id=id)
            )
        except Order.DoesNotExist:
            raise Http404("Заказ не найден")

        # Авторизованный пользователь
        if request.user.is_authenticated:
            if order.user_id == request.user.id:
                logger.debug("Получен объект заказа для авторизованного user")
                return order
            if order.user_id is None:
                guest_order_id = request.session.get("guest_order_id")
                if guest_order_id == order.id:

                    return order
            raise PermissionDenied("Нет доступа к этому заказу")

        # Гость
        guest_order_id = request.session.get("guest_order_id")
        if guest_order_id == order.id:
            logger.debug("Получен объект заказа для неавторизованного user")
            return order
        raise PermissionDenied("Гость не имеет доступа к этому заказу")

    def get(self, request: Request, id: int) -> Response:
        """Возвращает подробную информацию о заказе."""
        order = self.get_object(request, id)
        serializer = OrderDetailSerializer(
            order,
            context={"request": request},
        )
        logger.debug("Детали: '{}'", serializer.data)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request: Request, id: int) -> Response:
        """Частичное обновление заказа."""
        order = self.get_object(request, id)
        serializer = OrderUpdateSerializer(
            order,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            order.refresh_from_db()
            logger.debug("Заказ № '{}' оформлен для оплаты", order.id)
            return Response({"orderId": order.id})
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
