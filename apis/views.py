from django.shortcuts import render
from rest_framework import viewsets
from categories.models import *
from products.models import *
from .serializers import *

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status = True)
    serializer_class = ProductSerializer
    