from django.shortcuts import render, get_object_or_404  # type: ignore
from .models import Category
from products.models import Product

# Create your views here.


def home(req):
    context = {"cat": Category.getall()}
    return render(req, "categories/home.html", context)


def product_list(req, cat_slug = None):
    products = Product.objects.all()
    category = get_object_or_404(Category, slug=cat_slug)
    


def add_category(req):
    pass


def product_details(req):
    pass


def add_product(req):
    pass
