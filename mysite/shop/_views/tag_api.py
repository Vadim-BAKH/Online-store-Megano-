"""API-представление для получения списка всех тегов."""

from rest_framework.generics import ListAPIView

from .._models import Tag
from ..serialization import TagSerializer


class TagListAPIView(ListAPIView):

    """
    Представление для получения списка тегов.

    Использует `TagSerializer` для отображения данных.
    Возвращает все теги, отсортированные по id.
    """

    queryset = Tag.objects.all().prefetch_related("products").order_by("id")
    serializer_class = TagSerializer
