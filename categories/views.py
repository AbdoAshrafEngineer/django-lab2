from django.shortcuts import render, get_object_or_404, redirect  # type: ignore
from .models import Category
from products.models import Product
from django.utils.text import slugify
from .forms import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


# class based for list products
class list_products_class(View):
    def get(self, req, cat_id):
        category = Category.objects.get(id=cat_id)
        products = Product.objects.filter(category=category, status=True)
        context = {"prod": products, "cat": category}
        return render(req, "categories/list_prods.html", context)


class product_del_class(View):
    def post(self, req, cat_id, prod_id):
        prod = Product.objects.get(id=prod_id)
        prod.delete()
        return redirect("prod_list_class", cat_id=cat_id)


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
# ===============================================================================


# add new product using model form from forms.py
def new_product(req, cat_id):
    form = ProductFormModel()
    cat = Category.objects.get(id=cat_id)

    context = {"f": form, "cat": cat}

    if req.method == "POST":
        form = ProductFormModel(data=req.POST, files=req.FILES)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.category = cat
            updated.save()
            return redirect("products_list", cat_id=cat_id)

    return render(req, "categories/new_product.html", context)


# update using regular form
def prod_update_form(req, cat_id, prod_id):
    cat = Category.objects.get(id=cat_id)
    prod = Product.objects.get(id=prod_id)
    context = {"p": prod, "cat": cat}
    initial_data = {
        "name": prod.name,
        "price": prod.price,
        "stock": prod.stock,
        "sku": prod.sku,
        "desc": prod.desc,
    }

    if req.method == "POST":
        form = ProductForm(data=req.POST, files=req.FILES)
        if form.is_valid():
            prod.name = form.cleaned_data["name"]
            prod.price = form.cleaned_data["price"]
            prod.stock = form.cleaned_data["stock"]
            prod.sku = form.cleaned_data["sku"]
            prod.desc = form.cleaned_data["desc"]

            if form.cleaned_data["image"]:
                prod.image = form.cleaned_data["image"]

            prod.save()

            return redirect("product_det", cat_id=cat_id, prod_id=prod_id)
        else:
            msg = form.errors
    else:
        form = ProductForm(initial=initial_data)
        msg = ""

    context = {"p": prod, "cat": cat, "f": form, "msg": msg}

    return render(req, "categories/update_prod_form.html", context)

    # ======================================================================

    # lab 4 (insert, update, delete, list) using generic views
    # and register, login and logout


from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy


# insert
class Insert_cat_gen(CreateView):
    model = Category
    success_url = reverse_lazy("home")
    fields = ["name", "desc"]
    queryset = Category.objects.filter(status=True)
    context_object_name = "cat"
    template_name = "categories/insert_cat_gen.html"

    def generate_unique_slug(self, name):
        base_slug = slugify(name)
        unique_slug = base_slug
        counter = 1

        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1

        return unique_slug

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.slug = self.generate_unique_slug(instance.name)
        instance.save()
        return super().form_valid(form)


# list show for lgin user only
class List_cat_gen(LoginRequiredMixin, ListView):
    model = Category
    queryset = Category.objects.filter(status=True)
    template_name = "categories/home_cat_gen.html"
    context_object_name = "cat"


# update
class Update_cat_gen(UpdateView):
    model = Category
    queryset = Category.objects.filter(status=True)
    template_name = "categories/update_cat.html"
    success_url = reverse_lazy("home")
    fields = ["name", "desc"]
    context_object_name = "cat"


# delete
class Delete_cat(DeleteView):
    model = Category
    queryset = Category.objects.filter(status=True)
    success_url = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = False
        self.object.save()
        return redirect("home")


# =========================registrations=====================================
