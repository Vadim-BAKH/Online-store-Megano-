from django import forms

class ProductConfirmForm(forms.Form):
    product_id = forms.IntegerField(label="ID товара", min_value=1)
