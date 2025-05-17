from django.db import models # type: ignore
from django.core.validators import RegexValidator # type: ignore
from categories.models import Category

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/imgs", blank=True, null=True)
    sku = models.CharField(max_length=30,unique=True)
    desc = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

