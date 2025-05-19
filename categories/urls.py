from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add-category/", views.add_category, name="add_cat"),
    path("product-list/<int:cat_id>", views.product_list, name="products_list"),
    path("product/<int:cat_id>/add_product", views.add_product, name="add_product"),
    path(
        "product/<int:cat_id>/<int:prod_id>/", views.product_details, name="product_det"
    ),
    path(
        "category/<int:cat_id>/product/<int:prod_id>/update",
        views.update_prod,
        name="update_prod",
    ),
    path(
        "category/<int:cat_id>/delete/product/<int:prod_id>",
        views.soft_del_prod,
        name="soft_del_prod",
    ),
    # path for new_product_using_modelform
    path("new-product/<int:cat_id>", views.new_product, name="new_product"),
    # path for update_product_using_regular_form
    path(
        "category/<int:cat_id>/update-product/<int:prod_id>",
        views.prod_update_form,
        name="prod_update_form",
    ),
    # path list products using view class based
    path(
        "prod-list-class/<int:cat_id>",
        views.list_products_class.as_view(),
        name="prod_list_class",
    ),
    #path for hard delete using class based view
    path(
        "category/<int:cat_id>/hard-delete/product/<int:prod_id>",
        views.product_del_class.as_view(),
        name="hard_del",
    ),
]
