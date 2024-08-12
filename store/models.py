import os

from django.db import models
from category.models import Category
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=150)
    slug=models.SlugField(unique=True)
    descriptions=models.TextField()
    stock=models.IntegerField(default=1)
    price=models.FloatField(default=0.0)
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to=os.path.join("photos","products"),blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

choices=("")

variation_categorie=(("color","color"),("size","size"),)


class VariationsManager(models.Manager):

    def color(self):
        return super(VariationsManager,self).filter(category="color",is_active=True)

    def size(self):
        return super(VariationsManager,self).filter(category="size",is_active=True)

    def all(self, *args, **kwargs):
        return super().all(*args, **kwargs).order_by('category')

class Variations(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    category=models.CharField(max_length=100,choices=variation_categorie)
    value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    date_created=models.DateTimeField(auto_now_add=True)

    objects=VariationsManager()

    def __str__(self):
        return self.value