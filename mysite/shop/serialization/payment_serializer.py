"""Сериализатор для данных платежной карты."""

from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):

    """Валидирует данные для проведения платежа по заказу."""

    number = serializers.CharField(max_length=16)
    name = serializers.CharField(max_length=100)
    month = serializers.CharField(max_length=2)
    year = serializers.CharField(max_length=4)
    code = serializers.CharField(max_length=4)

    def validate_number(self, value: str) -> str:
        """Проверка: номер должен содержать 16 цифр."""
        if not value.isdigit():
            raise serializers.ValidationError(
                "Номер должен содержать только цифры.",
            )
        if len(value) != 16:
            raise serializers.ValidationError(
                "Номер карты содержит 16 цифр.",
            )
        return value

    def validate_month(self, value: str) -> str:
        """Проверка: месяц от 01 до 12."""
        if not value.isdigit() or not (1 <= int(value) <= 12):
            raise serializers.ValidationError(
                "Месяц должен быть от 01 до 12.",
            )
        return value

    def validate_year(self, value: str) -> str:
        """Проверка: год должен быть в формате YYYY."""
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError(
                "Год должен быть в формате YYYY."
            )
        return value

    def validate_code(self, value: str) -> str:
        """Проверка: код из 3 цифр."""
        if not value.isdigit() or len(value) != 3:
            raise serializers.ValidationError("Код должен содержать 3 цифры.")
        return value
