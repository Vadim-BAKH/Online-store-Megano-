"""Сериализатор для отображения полной информации о продукте."""

from django.db.models import Avg
from rest_framework import serializers

from .._models import Product
from .image_serialize import ProductImageSerializer
from .review_serializer import ReviewCreateSerializer
from .specification_serializer import SpecificationSerializer
from .tag_serializer import TagSerializer


class ProductSerializer(serializers.ModelSerializer):

    """
    Сериализатор для полной информации о продукте.

    Включает изображения, теги, характеристики, отзывы, рейтинг.
    """

    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    reviews = ReviewCreateSerializer(many=True, read_only=True)
    specifications = SpecificationSerializer(
        many=True,
        read_only=True,
    )
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    date = serializers.DateTimeField(
        format="%a %b %d %Y %H:%M:%S GMT%z (%Z)",
    )

    class Meta:

        """Метаданные модели с полями."""

        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        )

    def get_rating(self, obj) -> float | None:
        """
        Вычисляет средний рейтинг продукта по всем отзывам.

        Возвращает округлённое значение до 1 знака после запятой,
        либо None, если отзывов нет.
        """
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        avg = reviews.aggregate(avg_rate=Avg("rate"))["avg_rate"]
        if avg is None:
            return None
        return round(avg, 1)
