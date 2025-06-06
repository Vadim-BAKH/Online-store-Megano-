from django.db import models

from .soft_delete_model import SoftDeleteModel

from .product_model import Product

def product_image_directory_path(instance: "Product", filename: str) -> str:
    """
    Путь для изображений товара.
    """
    return f"images_{instance.pk}/product/{filename}"

class ProductImage(SoftDeleteModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    src = models.ImageField(null=True, blank=True, upload_to=product_image_directory_path)
    alt = models.CharField(null=True, blank=True, max_length=50)
