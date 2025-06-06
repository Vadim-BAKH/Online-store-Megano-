from rest_framework import serializers

from .tag_serializer import TagSerializer
from .image_serialize import ProductImageSerializer
from .._models import Product

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'images', 'tags', 'count', 'freeDelivery')
