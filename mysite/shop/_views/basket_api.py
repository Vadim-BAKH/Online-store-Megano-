"""APIView для управления корзиной товаров."""

from django.db import transaction
from django.shortcuts import get_object_or_404
from loguru import logger
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .._models import Cart, CartItem, Product
from ..serialization import ProductInCartSerializer


class BasketAPIView(APIView):

    """
    Обработка запросов корзины.

    Получение, добавление и удаление товаров.
    """

    def get_cart(self, request: Request) -> Cart:
        """
        Возвращает текущую корзину пользователя.

        Если пользователь авторизован —
        объединяет корзину сессии с корзиной пользователя.
        """
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            session_key = request.session.session_key
            logger.debug("session_key: '{}'", session_key)
            if session_key:
                try:
                    session_cart = Cart.objects.get(
                        session_key=session_key, user=None
                    )
                    logger.debug("session_cart: '{}'", session_cart)
                    with transaction.atomic():
                        for (
                            item
                        ) in session_cart.items.select_for_update().all():
                            (
                                cart_item,
                                created,
                            ) = CartItem.objects.select_for_update().get_or_create(
                                cart=cart, product=item.product
                            )
                            if not created:
                                new_quantity = (
                                    cart_item.quantity + item.quantity
                                )
                                cart_item.quantity = min(
                                    new_quantity, item.product.count
                                )
                            else:
                                cart_item.quantity = min(
                                    item.quantity, item.product.count
                                )
                            cart_item.save()
                            logger.debug("Создан: '{}'", cart_item)
                        session_cart.delete()
                except Cart.DoesNotExist:
                    pass
            return cart
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(
                session_key=session_key, user=None
            )
            logger.debug("session_key до авторизации: '{}'", session_key)

            return cart

    def serialize_cart_products(self, cart: Cart):
        """Сериализует список товаров из корзины с учётом их количества."""
        products_data = []
        for cart_item in cart.items.select_related("product").all():
            product_data = ProductInCartSerializer(cart_item.product).data
            product_data["count"] = (
                cart_item.quantity
            )  # заменяем count на количество в корзине
            products_data.append(product_data)
        return products_data

    def get(self, request: Request) -> Response:
        """Возвращает список товаров в корзине."""
        cart = self.get_cart(request=request)
        data = self.serialize_cart_products(cart)

        return Response(data)

    def post(self, request: Request) -> Response:
        """Добавляет товар в корзину или увеличивает его количество."""
        cart = self.get_cart(request=request)
        product_id = request.data.get("id")
        count = int(request.data.get("count", 1))
        product = get_object_or_404(Product, id=product_id)

        with transaction.atomic():
            try:
                cart_item = CartItem.objects.select_for_update().get(
                    cart=cart, product=product
                )
                existing_quantity = cart_item.quantity
                logger.debug(
                    "Создан '{}' с '{}'", cart_item, existing_quantity
                )
            except CartItem.DoesNotExist:
                cart_item = None
                existing_quantity = 0

            new_quantity = existing_quantity + count
            allowed_quantity = min(new_quantity, product.count)

            if allowed_quantity <= 0:
                return Response(
                    {"detail": "Товар отсутствует на складе"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if cart_item:
                cart_item.quantity = allowed_quantity
                cart_item.save()
                logger.debug(f"Обновление {cart_item}")
            else:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=allowed_quantity,
                )
                logger.debug("Создан '{}'", cart_item)

        data = self.serialize_cart_products(cart)

        return Response(data)

    def delete(self, request: Request) -> Response:
        """
        Уменьшает количество товара в корзине.

        Удаляет его полностью.
        """
        cart = self.get_cart(request)
        product_id = request.data.get("id")
        count = int(request.data.get("count", 0))

        with transaction.atomic():
            try:
                cart_item = CartItem.objects.select_for_update().get(
                    cart=cart, product_id=product_id
                )
                if count >= cart_item.quantity:
                    cart_item.delete()
                else:
                    cart_item.quantity -= count
                    cart_item.save()
            except CartItem.DoesNotExist:
                pass

        data = self.serialize_cart_products(cart)
        return Response(data)
