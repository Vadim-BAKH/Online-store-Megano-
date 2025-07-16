"""APIView для обработки платежей по заказу."""

from random import choice

from django.db import transaction
from django.shortcuts import get_object_or_404
from loguru import logger
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .._models import Order, Payment
from ..serialization import PaymentSerializer


class PaymentOrderApi(APIView):

    """
    API для создания платежа по заказу.

    Если номер карты некорректен (по условиям проверки),
    возвращает ошибку
    и сохраняет её в поле `payment_error` заказа.
    """

    @transaction.atomic
    def post(self, request: Request, id: int) -> Response:
        """
        POST-запрос для проведения оплаты по заказу.

        Аргументы:
        - `request`: объект запроса с данными платежа.
        - `id`: ID заказа, к которому относится платёж.

        Возвращает:
        - 201 при успешной оплате.
        - 400 при ошибке валидации или симуляции сбоя.
        """
        order = get_object_or_404(
            Order,
            id=id,
            user=request.user,
        )

        # Ниже условие - формальность, тк кнопка не видна.
        if hasattr(order, "payment"):
            return Response(
                {"detail": "Платёж для этого заказа уже создан."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            number = data["number"]

            if number.endswith("0") or int(number) % 2 != 0:
                errors = (
                    "Случайный сбой",
                    "Проверь остаток на счёте",
                    "Попытка подозрительной транзакции",
                )
                error_message = choice(errors)
                order.payment_error = error_message
                order.save(update_fields=("payment_error",))
                return Response(
                    {"detail": error_message},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Создаём платеж
            Payment.objects.create(
                order=order,
                number=data["number"],
                name=data["name"],
                month=data["month"],
                year=data["year"],
                code=data["code"],
            )
            order.status = "paid"
            order.payment_error = None
            order.save(
                update_fields=(
                    "status",
                    "payment_error",
                )
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        error_message = next(iter(serializer.errors.values()))[0]
        logger.debug("Ошибка: '{}'", error_message)
        order.payment_error = error_message
        order.save(update_fields=("payment_error",))
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
