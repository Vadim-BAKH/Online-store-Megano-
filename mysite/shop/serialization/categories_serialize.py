"""Сериализатор категорий с рекурсивными подкатегориями."""

from rest_framework import serializers

from .._models import Category


class CategorySerializer(serializers.ModelSerializer):

    """Сериализует категорию с полями."""

    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:

        """Метаданные модели с полями."""

        model = Category
        fields = ("id", "title", "image", "subcategories")

    def get_image(self, obj):
        """Возвращает словарь с URL и описанием изображения."""
        return {
            "src": obj.src.url if obj.src else None,
            "alt": obj.alt or obj.title,
        }

    def get_subcategories(self, obj):
        """Рекурсивно сериализует подкатегории текущей категории."""
        subcat = obj.subcategories.all()
        return CategorySerializer(subcat, many=True).data
