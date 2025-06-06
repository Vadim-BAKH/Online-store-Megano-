from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from loguru import logger
from django.http import Http404

from .._models import Product
from ..forms import ProductConfirmForm

class ProductDeleteByIdView(UserPassesTestMixin, View):
    template_name = "shop/product_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        form = ProductConfirmForm()
        return render(request, self.template_name, {"form": form})



    def post(self, request):
        form = ProductConfirmForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                form.add_error('product_id', 'Товар с таким ID не найден, или уже архивирован.')
                return render(request, self.template_name, {"form": form})

            product.delete()
            messages.success(request, f"Товар ID #{product_id} успешно архивирован")
            logger.debug(f"Товар {product_id} удален а архив")
            return redirect("shop:products_table")
        return render(request, self.template_name, {"form": form})

