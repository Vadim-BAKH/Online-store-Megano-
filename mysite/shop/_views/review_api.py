"""Представление для создания отзыва на продукт."""

from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import (
    NotFound,
)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .._models import Product
from ..serialization import ReviewCreateSerializer


class ProductReviewCreateView(CreateAPIView):

    """
    Создание отзыва на продукт.

    Доступ разрешён только авторизованным пользователям.
    """

    serializer_class = ReviewCreateSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        SessionAuthentication,
    ]

    def get_product(self) -> Product:
        """
        Получает продукт по ID из URL.

        Raises:
            NotFound: если продукт не существует.

        Returns:
            Экземпляр `Product`.

        """
        product_id = self.kwargs.get("product_id")
        try:
            return Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound("Товар не найден")

    def get_serializer_context(self) -> dict:
        """
        Добавляет продукт в контекст сериализатора.

        Returns:
            Словарь с дополнительным контекстом.

        """
        context = super().get_serializer_context()
        context["product"] = self.get_product()
        return context
