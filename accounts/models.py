from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True, max_length=200)
    status = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    
