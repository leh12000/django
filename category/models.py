import os.path

from django.db import models

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=150,unique=True)
    slug=models.SlugField(max_length=150,unique=True)
    descriptions=models.TextField(max_length=500)
    image=models.ImageField(upload_to=os.path.join("photos","category"),blank=True,null=True)

    def __str__(self):
        return self.name