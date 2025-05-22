from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=200)
    username = models.CharField(max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = MyUserManager()
