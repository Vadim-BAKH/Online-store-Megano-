"""Generated by Django 5.2.1 on 2025-06-22 13:05."""

from django.db import migrations, models


class Migration(migrations.Migration):

    """Модель миграции."""

    dependencies = [
        ("shop", "0015_alter_order_delivery_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sort_index",
            field=models.IntegerField(default=0, verbose_name="Индекс сортировки"),
        ),
    ]
