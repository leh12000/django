from django.db import models
from account.models import Customer
from store.models import Product,Variations
# Create your models here.

class Payment(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    amount_paid=models.IntegerField(default=0)
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id




class Commande(models.Model):
    statu = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number=models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    address_line_1=models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    order_note=models.TextField(blank=True,max_length=1000)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(choices=statu,max_length=20,default="New")
    ip=models.CharField(blank=True,max_length=20)
    is_order=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

class OrderProduct(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    commande = models.ForeignKey(Commande,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation=models.ForeignKey(Variations,on_delete=models.CASCADE)
    color=models.CharField(max_length=50)
    size=models.CharField(max_length=50)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    orderd=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def str(self):
        return self.product.name