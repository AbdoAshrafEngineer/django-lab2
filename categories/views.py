from django.shortcuts import render, get_object_or_404, redirect  # type: ignore
from .models import Category
from products.models import Product
from django.utils.text import slugify

# Create your views here.


def home(req):  # show all categoires need all categories from database
    context = {"cat": Category.objects.all()}
    return render(req, "categories/home.html", context)


def add_category(
    req,
):  # add new category to database so i need to deal with the data come that come from post request
    name = ""
    desc = ""

    if req.method == "POST":
        name = req.POST["name"].strip()
        desc = req.POST["desc"].strip()

        if name:
            Category.objects.create(name=name, desc=desc, slug=slugify(name))
            return redirect("home")

    return render(req, "categories/add_category.html")


def product_list(req, cat_id):
    category = Category.objects.get(id=cat_id)
    products = Product.objects.filter(category=category)
    context = {"cat": category, "prod": products}
    return render(req, "categories/product_list.html", context)


def add_product(req, cat_id):
    name = ""
    price = ""
    sku = ""
    cat = Category.objects.get(id=cat_id)
    context = {"cat": cat}

    if req.method == "POST":
        name = req.POST["name"]
        price = req.POST["price"]
        stock = req.POST["stock"]
        sku = req.POST["sku"]
        desc = req.POST["desc"]

        if name and price and sku:
            Product.objects.create(
                name=name, price=price, stock=stock, sku=sku, desc=desc, category=cat
            )
            return redirect("products_list", cat_id=cat_id)

    return render(req, "categories/add_product.html", context)


def product_details(req):
    pass

def hard_del_cat(req, cat_id):
    pass

def soft_del_cat(req, cat_id):
    pass

def hard_del_prod(req, prod_id):
    pass

def soft_del_prod(req, prod_id):
    pass
