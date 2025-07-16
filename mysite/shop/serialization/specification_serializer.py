"""Сериализатор для характеристики товара (Specification)."""

from rest_framework.serializers import ModelSerializer

from .._models import Specification


class SpecificationSerializer(ModelSerializer):

    """Сериализует поля name и value характеристики товара."""

    class Meta:

        """Метаданные модели."""

        model = Specification
        fields = ("name", "value")
