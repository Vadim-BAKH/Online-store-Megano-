"""Generated by Django 5.2.1 on 2025-06-25 10:28."""

from django.db import migrations, models


class Migration(migrations.Migration):

    """Модель миграции."""

    dependencies = [
        ("shop", "0017_sale"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_error",
            field=models.TextField(blank=True, null=True, verbose_name="Ошибка оплаты"),
        ),
    ]
