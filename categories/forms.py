from django import forms
from products.models import *
from django.core.validators import FileExtensionValidator


class ProductFormModel(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "stock", "sku", "desc", "image"]


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.DecimalField(decimal_places=2)
    stock = forms.IntegerField(initial=0)
    sku = forms.CharField(max_length=30)
    desc = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        required=False
    )
    image = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ]
    )
