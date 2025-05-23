from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"prodview", ProductViewSet, basename="product-viewset")

urlpatterns = [
    path("products/", product_list_api, name="product_list_api"),
    path("prod/<str:name>", ProductAPIView.as_view(), name="product_api_view"),
    path("product/<int:pk>", Product_RUD.as_view(), name="Product_RUD"),
    path('', include(router.urls))
]
