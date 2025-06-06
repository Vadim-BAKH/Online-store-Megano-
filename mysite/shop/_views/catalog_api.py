from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .._models import Product, Tag, Category
from ..serialization import ProductSerializer
from math import ceil

class ProductCatalogAPIView(APIView):
    def get(self, request):
        params = request.query_params

        # Парсим фильтры
        filter_params = params.get('filter')
        if filter_params:

            filter_params = json.loads(filter_params)
        else:
            filter_params = {}

        name = filter_params.get('name', '').strip()
        min_price = float(filter_params.get('minPrice', 0))
        max_price = float(filter_params.get('maxPrice', 50000))
        free_delivery = filter_params.get('freeDelivery')
        available = filter_params.get('available')

        category_id = params.get('category')
        sort_field = params.get('sort')
        sort_type = params.get('sortType')
        tags = params.getlist('tags[]') or params.getlist('tags')  # массив тегов
        limit = int(params.get('limit', 20))
        current_page = int(params.get('currentPage', 1))

        products = Product.objects.all()

        # Фильтрация
        if name:
            products = products.filter(title__icontains=name)
        products = products.filter(price__gte=min_price, price__lte=max_price)

        if free_delivery is not None:
            if free_delivery in ['true', 'True', True]:
                products = products.filter(freeDelivery=True)
            elif free_delivery in ['false', 'False', False]:
                products = products.filter(freeDelivery=False)

        if available is not None:
            if available in ['true', 'True', True]:
                products = products.filter(count__gt=0)
            elif available in ['false', 'False', False]:
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

        # Сортировка
        if sort_field:
            if sort_type == 'dec':
                sort_field = '-' + sort_field
            products = products.order_by(sort_field)

        # Пагинация
        total = products.count()
        last_page = ceil(total / limit)
        offset = (current_page - 1) * limit
        products = products[offset:offset + limit]

        serializer = ProductSerializer(products, many=True)
        return Response({
            'items': serializer.data,
            'currentPage': current_page,
            'lastPage': last_page,
            'total': total,
        }, status=status.HTTP_200_OK)
