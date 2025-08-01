"""Generated by Django 5.2.1 on 2025-06-21 08:19."""

from django.db import migrations, models


class Migration(migrations.Migration):

    """Модель миграции."""

    dependencies = [
        ("shop", "0013_remove_order_products_payment"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliverySettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "free_delivery_threshold",
                    models.DecimalField(
                        decimal_places=2,
                        default=2000,
                        max_digits=10,
                        verbose_name="Порог бесплатной доставки",
                    ),
                ),
                (
                    "delivery_fee",
                    models.DecimalField(
                        decimal_places=2,
                        default=200,
                        max_digits=10,
                        verbose_name="Стоимость доставки при сумме ниже порога",
                    ),
                ),
                (
                    "express_delivery_fee",
                    models.DecimalField(
                        decimal_places=2,
                        default=500,
                        max_digits=10,
                        verbose_name="Стоимость экспресс-доставки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Настройка доставки",
                "verbose_name_plural": "Настройки доставки",
            },
        ),
        migrations.AlterField(
            model_name="order",
            name="delivery_type",
            field=models.CharField(
                choices=[
                    ("delivery", "Доставка"),
                    ("express", "Экспресс-доставка"),
                ],
                default="delivery",
                max_length=50,
                verbose_name="Тип доставки",
            ),
        ),
    ]
