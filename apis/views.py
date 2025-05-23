from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from categories.models import *
from products.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404


# add & list product endpoint using function based view
# Create your views here.
@api_view(["GET", "POST"])
# Turns a regular Python function into an API endpoint that understands these HTTP methods.
def product_list_api(req):
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


# update product using class based
class ProductAPIView(APIView):

    def get_object(self, name):
        try:
            return Product.objects.get(name=name)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, name):
        product = self.get_object(name)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, name):
        product = self.get_object(name)
        serializer = ProductSerializer(product, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, name):
        product = self.get_object(name)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=400)


# update,getbyid,delete product using generic
class Product_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(status=True)
    serializer_class = ProductSerializer


# product crud using View Set
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status=True)
    serializer_class = ProductSerializer
