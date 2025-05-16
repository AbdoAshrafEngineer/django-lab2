from django.shortcuts import render  # type: ignore
from models import Category

# Create your views here.


def home(req):
    context = {"cat": Category.getall()}
    return render(req, "categories/home.html", context)





