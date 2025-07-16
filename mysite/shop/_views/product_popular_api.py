"""Получение популярных товаров по количеству покупок."""

from django.db.models import Count
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .._models import Product
from ..serialization import ProductSerializer


class PopularProductsAPIView(APIView):

    """
    API-представление для получения списка популярных товаров.

    Популярность по количеству связанных объектов OrderItem.
    Сортировка сначала по `sort_index` (если задан),
    затем по количеству покупок.
    """

    def get(self, request: Request) -> Response:
        """
        Возвращает JSON-список до 8 самых популярных товаров.

        Args:
            request (Request): Объект запроса от клиента.

        Returns:
            Response: JSON-ответ со списком сериализованных товаров.

        """
        popular_products = Product.objects.annotate(
            purchase_count=Count("orderitem")
        ).order_by("-sort_index", "-purchase_count")[:8]

        serializer = ProductSerializer(
            popular_products,
            many=True,
            context={"request": request},
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
