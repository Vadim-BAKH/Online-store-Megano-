"""
API-представление.

Фильтрация, сортировка и пагинация каталога товаров.
"""

from math import ceil

from django.db.models import Avg
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .._models import Product
from ..serialization import ProductSerializer


class ProductCatalogAPIView(APIView):

    """
    Представление для получения списка товаров по фильтрам.

    Поддержка сортировки и постраничного вывода.
    """

    def get(self, request: Request) -> Response:
        """
        Обрабатывает GET-запрос на получение каталога товаров.

        Поддерживает фильтрацию по:
        - названию (name)
        - цене (minPrice, maxPrice)
        - наличию (available)
        - бесплатной доставке (freeDelivery)
        - категории (category)
        - тегам (tags)

        Поддерживает сортировку по:
        - рейтингу, цене и другим полям

        Возвращает:
            JSON-ответ со списком товаров и метаинформацией о пагинации.
        """
        params = request.query_params

        # Собираем фильтры из параметров с префиксом filter[...]
        filter_params = {}
        for key, value in params.items():
            if key.startswith("filter[") and key.endswith("]"):
                param_name = key[7:-1]
                filter_params[param_name] = value

        name = filter_params.get("name", "").strip()
        min_price = float(filter_params.get("minPrice", 0))
        max_price = float(filter_params.get("maxPrice", 50000))

        free_delivery = filter_params.get("freeDelivery")
        if free_delivery is not None:
            free_delivery = free_delivery.lower() == "true"

        available = filter_params.get("available")
        if available is not None:
            available = available.lower() == "true"

        category_id = params.get("category")
        sort_field = params.get("sort")
        sort_type = params.get("sortType")
        tags = params.getlist("tags[]") or params.getlist("tags")
        limit = int(params.get("limit", 20))
        current_page = int(params.get("currentPage", 1))

        products = Product.objects.all()

        # Фильтрация
        if name:
            products = products.filter(title__icontains=name)

        products = products.filter(price__gte=min_price, price__lte=max_price)

        if free_delivery is not None and free_delivery:
            products = products.filter(freeDelivery=True)

        if available is not None:
            if available:
                products = products.filter(count__gt=0)
            else:
                products = products.filter(count=0)

        if category_id:
            try:
                category_id = int(category_id)
                products = products.filter(category_id=category_id)
            except ValueError:
                pass

        if tags:
            try:
                tags_ids = list(map(int, tags))
                products = products.filter(tags__id__in=tags_ids).distinct()
            except ValueError:
                pass

        products = products.annotate(rating=Avg("reviews__rate"))

        # Сортировка
        if sort_field:
            if sort_field == "rating":
                order_prefix = "-" if sort_type == "dec" else ""
                products = products.order_by(f"{order_prefix}rating")
            else:
                if sort_type == "dec":
                    sort_field = "-" + sort_field
                products = products.order_by(sort_field)

        # Пагинация
        total = products.count()
        last_page = ceil(total / limit)
        offset = (current_page - 1) * limit
        products = products[offset : offset + limit]

        serializer = ProductSerializer(products, many=True)
        return Response(
            {
                "items": serializer.data,
                "currentPage": current_page,
                "lastPage": last_page,
                "total": total,
            },
            status=status.HTTP_200_OK,
        )
