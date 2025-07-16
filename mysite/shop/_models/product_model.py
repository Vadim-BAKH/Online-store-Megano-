from django.core.validators import MaxLengthValidator, MinValueValidator
from django.db import models

from .category_model import Category
from .soft_delete_model import SoftDeleteModel
from .tag_model import Tag


class Product(SoftDeleteModel):

    """Модель товара интернет магазина."""

    class Meta:
        ordering = ("title",)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    price = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(
        null=True,
        blank=True,
        validators=[
            MaxLengthValidator(200),
        ],
    )
    fullDescription = models.TextField(
        null=True,
        blank=True,
        validators=[
            MaxLengthValidator(500),
        ],
    )
    freeDelivery = models.BooleanField(default=False)
    limited_edition = models.BooleanField(default=False)
    sort_index = models.IntegerField(
        default=0,
        verbose_name="Индекс сортировки",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="products",
    )

    def __str__(self) -> str:
        return (
            f"Product(pk={self.pk}," f" title={self.title!r}," f" price={self.price})"
        )
