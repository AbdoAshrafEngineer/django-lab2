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
    products = Product.objects.filter(category=category, status=True)
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
        img = req.FILES["image"]

        if name and price and sku and img:
            Product.objects.create(
                name=name,
                price=price,
                stock=stock,
                sku=sku,
                desc=desc,
                category=cat,
                image=img,
            )
            return redirect("products_list", cat_id=cat_id)

    return render(req, "categories/add_product.html", context)


def product_details(req, cat_id, prod_id):
    cat = Category.objects.get(id=cat_id)
    prod = Product.objects.get(id=prod_id, status=True)
    context = {"cat": cat, "p": prod}
    return render(req, "categories/product_details.html", context)


def update_prod(req, cat_id, prod_id):
    cat = Category.objects.get(id=cat_id)
    prod = Product.objects.get(id=prod_id)

    if req.method == "POST":
        prod.name = req.POST.get("name", prod.name)
        prod.price = req.POST.get("price", prod.price)
        prod.stock = req.POST.get("stock", prod.stock)
        prod.sku = req.POST.get("sku", prod.sku)
        prod.desc = req.POST.get("desc", prod.desc)

        if "image" in req.FILES:
            prod.image = req.FILES["image"]

        prod.save()
        return redirect("product_det", cat_id, prod_id)

    context = {"cat": cat, "p": prod}
    return render(req, "categories/update_prod.html", context)


def soft_del_prod(req, cat_id, prod_id):
    if req.method != "POST":
        return redirect("product_det", cat_id, prod_id)
    p = Product.objects.get(id=prod_id, status=True)
    p.status = False
    p.save()
    return redirect("products_list", cat_id=cat_id)


# def hard_del_prod(req, prod_id):
#     pass
