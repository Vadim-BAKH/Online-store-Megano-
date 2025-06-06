from rest_framework import serializers

from .._models import ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('src', 'alt',)
