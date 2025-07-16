"""API-представление списка категорий верхнего уровня."""

from rest_framework.generics import ListAPIView

from .._models import Category
from ..serialization import CategorySerializer


class CategoryApiView(ListAPIView):

    """
    Возвращает список категорий верхнего уровня с их подкатегориями.

    Использует queryset с prefetch_related для оптимизации
    связанных подкатегорий.
    """

    queryset = (
        Category.objects.filter(parent__isnull=True)
        .prefetch_related("subcategories")
        .order_by("title")
    )
    serializer_class = CategorySerializer
