from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add-category/", views.add_category, name="add_cat"),
    path("product-list/<int:cat_id>", views.product_list, name="products_list"),
    path("product/<int:cat_id>/add_product", views.add_product, name="add_product"),
    path("product<int:cat_id>/<int:prod_id>/", views.product_details, name="product_det"),
]
