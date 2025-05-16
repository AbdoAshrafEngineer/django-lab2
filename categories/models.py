from django.db import models # type: ignore


# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=50)
    desc = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)

    @classmethod
    def getall(cls):
        return cls.objects.filter(status=True)
