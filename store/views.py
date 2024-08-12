from django.db.models import Q
from django.shortcuts import render, HttpResponse, get_object_or_404

# Create your views here.
from .models import Product
from category.models import Category
from .models import Variations



def store(request,category_slug=None):
    if category_slug:
        products=Product.objects.filter(category__slug=category_slug,is_available=True)
    else:
        products=Product.objects.filter(is_available=True)

    return render(request,"store/store.html",{"products":products})



def details(request,category_slug,product_slug):
    categorie=get_object_or_404(Category,slug=category_slug)
    product=Product.objects.get(slug=product_slug,category=categorie)

    return render(request,'store/details.html',{"product":product})


def search(request):
    keyword=request.GET.get("search")
    products=Product.objects.filter(Q(descriptions__icontains=keyword) | Q(name__icontains=keyword))
    return render(request,'store/store.html',{"products":products})