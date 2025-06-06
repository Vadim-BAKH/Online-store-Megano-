from rest_framework.generics import ListAPIView

from .._models import Category
from ..serialization import CategorySerializer

class CategoryApiView(ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)\
                               .prefetch_related('subcategories')\
                               .order_by('title')
    serializer_class = CategorySerializer
