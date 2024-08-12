from django.contrib import admin
from .models import Payment,Commande,OrderProduct
# Register your models here.
admin.site.register(Payment)
admin.site.register(Commande)
admin.site.register(OrderProduct)