from rest_framework.generics import ListAPIView
from .._models import Tag
from ..serialization import TagSerializer

class TagListAPIView(ListAPIView):
    queryset = Tag.objects.all().prefetch_related("products").order_by("id")
    serializer_class = TagSerializer
