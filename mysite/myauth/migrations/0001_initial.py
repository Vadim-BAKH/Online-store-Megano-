"""Generated by Django 5.2.1 on 2025-05-25 04:53."""

import django.db.models.deletion
import myauth.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    """Модель миграций."""

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("fullName", models.CharField(max_length=25)),
                (
                    "email",
                    models.EmailField(db_index=True, max_length=254, unique=True),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=12,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        null=True,
                        upload_to=myauth.models.profile_avatars_directory_path,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
