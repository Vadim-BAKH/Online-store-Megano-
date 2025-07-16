"""Сериализатор для модели тега."""

from rest_framework import serializers

from .._models import Tag


class TagSerializer(serializers.ModelSerializer):

    """Сериализатор, возвращающий ID и название тега."""

    class Meta:

        """Метаданные модели с полями."""

        model = Tag
        fields = (
            "id",
            "name",
        )
