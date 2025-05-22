from django.urls import path, include
from rest_framework import routers
from .views import *

urlpatterns = [
    path('', product_list, name="product_list_def")
]
