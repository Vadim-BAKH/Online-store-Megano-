"""Сериализатор для создания отзыва на товар."""

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)

from .._models import Review


class ReviewCreateSerializer(ModelSerializer):

    """Обрабатывает сериализацию и валидацию данных отзыва."""

    class Meta:

        """Метаданные модели с полями."""

        model = Review
        fields = (
            "author",
            "email",
            "text",
            "rate",
        )

    def create(self, validated_data):
        """
        Создаёт отзыв, привязанный к товару из контекста.

        Raises:
            ValidationError: если товар не передан в контексте.

        """
        product = self.context.get("product")
        if not product:
            raise ValidationError("Для отзыва выберите товар")
        return Review.objects.create(
            product=product,
            **validated_data,
        )
