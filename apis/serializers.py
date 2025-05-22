from rest_framework import serializers
from categories.models import *
from products.models import *


# Create your models here.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ["name", "price", "stock", "sku"]
        
