"""Сериализатор продукта для отображения в корзине."""

from django.db.models import Avg
from rest_framework import serializers

from .._models import Product
from .image_serialize import ProductImageSerializer
from .tag_serializer import TagSerializer


class ProductInCartSerializer(serializers.ModelSerializer):

    """
    Сериализатор продукта для вывода в корзине.

    Включает изображения, теги, количество отзывов и среднюю оценку.
    """

    category = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateTimeField(
        format="%a %b %d %Y %H:%M:%S GMT%z (%Z)",
    )
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:

        """Метаданные подели с полями."""

        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )

    def get_reviews(self, obj):
        """Возвращает количество отзывов у продукта."""
        return obj.reviews.count()

    def get_rating(self, obj):
        """Вычисляет и возвращает средний рейтинг продукта."""
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        avg = reviews.aggregate(avg_rate=Avg("rate"))["avg_rate"]
        if avg is None:
            return None
        return round(avg, 1)
