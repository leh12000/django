from django.http import HttpResponse
from django.shortcuts import render


from store.models import Product

def index(request):
    products=Product.objects.filter(is_available=True)
    return render(request,'index.html',{"products":products})