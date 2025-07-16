"""Представление для получения информации о товаре по его ID."""

from rest_framework.generics import RetrieveAPIView

from .._models import Product
from ..serialization import ProductSerializer


class ProductDetailAPIView(RetrieveAPIView):

    """
    API-представление для получения одного товара по ID.

    Использует `RetrieveAPIView` из DRF.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    lookup_url_kwarg = "product_id"
