from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from loguru import logger

from .._models import Product
from ..forms import ProductConfirmForm

class ProductReturnByIdView(UserPassesTestMixin, View):
    template_name = "shop/product_return.html"

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> HttpResponse:
        form = ProductConfirmForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProductConfirmForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data["product_id"]
            try:
                product = Product.all_objects.get(pk=product_id)
            except Product.DoesNotExist:
                form.add_error('product_id', 'Товар с таким ID не найден.')
                return render(request, self.template_name, {"form": form})
            product.undelete()
            messages.success(request, f"Товар ID #{product_id} успешно разархивирован")
            logger.debug(f"Товар {product_id} возвращён из архива")
            return redirect("shop:products_table")
        return render(request, self.template_name, {"form": form})
