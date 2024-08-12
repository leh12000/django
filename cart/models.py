from django.db import models


# Create your models here.

from store.models import Product,Variations
from account.models import Customer
from great import settings



class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    variations = models.ManyToManyField(Variations,blank=True)

    def sub_total(self):
        return self.product.price*self.quantity

    def __str__(self):
        return self.product.name



class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    orders=models.ManyToManyField(Order,related_name="cart",blank=True)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


    def total_price(self):
        total=0
        for item in self.orders.all():
            total+=item.sub_total()
        return total


