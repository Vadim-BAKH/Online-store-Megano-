"""APIView для получения списка продуктов в баннерах."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .._models import Product
from ..serialization import ProductSerializer


class BannerListAPIView(APIView):

    """Представление для получения списка продуктов для баннеров."""

    def get(self, request):
        """
        Возвращает сериализованный список всех продуктов.

        Используется для отображения баннеров на главной странице.
        """
        products = Product.objects.all()
        serializer = ProductSerializer(
            products,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
