"""API-представление для получения товаров ограниченного тиража."""

from rest_framework.generics import ListAPIView

from .._models import Product
from ..serialization import LimitedProductSerializer


class LimitedProductListAPIView(ListAPIView):

    """Возвращает список до 16 товаров с ограниченным тиражом."""

    serializer_class = LimitedProductSerializer

    def get_queryset(self):
        return Product.objects.filter(limited_edition=True)[:16]
