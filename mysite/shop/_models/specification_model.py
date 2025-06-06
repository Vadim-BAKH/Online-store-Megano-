from django.db import models

from .soft_delete_model import SoftDeleteModel
from .product_model import Product

class Specification(SoftDeleteModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    name = models.CharField(null=True, blank=True, max_length=20)
    value = models.CharField(null=True, blank=True, max_length=10)

    def __str__(self):
        return self.name
