"""Сериализатор для отображения информации об активных акциях."""

from rest_framework import serializers

from .._models import Sale
from .image_serialize import ProductImageSerializer


class SaleSerializer(serializers.ModelSerializer):

    """
    Сериализатор акции с привязанным товаром.

    Отображает:
    - цену товара (price),
    - цену со скидкой (salePrice),
    - даты действия акции (dateFrom, dateTo),
    - название товара (title),
    - изображения (images).
    """

    id = serializers.IntegerField(source="product.id")
    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
    )
    salePrice = serializers.DecimalField(
        source="sale_price",
        max_digits=10,
        decimal_places=2,
    )
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()
    title = serializers.CharField(source="product.title")
    images = ProductImageSerializer(
        source="product.images",
        many=True,
        read_only=True,
    )

    class Meta:

        """Метаданные модели с полями."""

        model = Sale
        fields = (
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images",
        )

    def get_dateFrom(self, obj: Sale) -> str:
        """
        Преобразует дату начала акции в строку формата "дд.мм.гггг".

        Args:
            obj (Sale): объект акции.

        Returns:
            str: отформатированная дата начала или пустая строка.

        """
        if obj.date_from:
            return obj.date_from.strftime("%d.%m.%Y")
        return ""

    def get_dateTo(self, obj: Sale) -> str:
        """
        Преобразует дату окончания акции в строку формата "дд.мм.гггг".

        Args:
            obj (Sale): объект акции.

        Returns:
            str: отформатированная дата окончания или пустая строка.

        """
        if obj.date_to:
            return obj.date_to.strftime("%d.%m.%Y")
        return ""
