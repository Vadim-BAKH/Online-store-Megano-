from rest_framework import serializers

from .._models import Category

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories',)

    def get_image(self, obj):
        return {
            "src": obj.src.url if obj.src else None,
            "alt": obj.alt or obj.title
        }

    def get_subcategories(self, obj):
        # Рекурсивно сериализуем подкатегории
        subcat = obj.subcategories.all()
        return CategorySerializer(subcat, many=True).data
