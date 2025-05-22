from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from categories.models import *
from products.models import *
from .serializers import *

# Create your views here.
@api_view(['GET', 'POST'])
# Turns a regular Python function into an API endpoint that understands these HTTP methods.
def product_list(req):
    if req.method == 'GET':
        products = Product.objects.filter(status=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif req.method == 'POST':
        serializer = ProductSerializer(data=req.data)
        if serializer.is_valid():
            cat = Category.objects.get(name="smartphone")
            serializer.save(category=cat)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

