import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from orders.forms import CommandeForm
from orders.models import Commande

from cart.models import Cart


# Create your views here.

def placeOrder(request):
    user=request.user
    cart_items=Cart.objects.filter(user=user)
    cart_count=cart_items.count()
    if cart_count<1:
        return redirect("store")

    total=0
    tax=0
    for item in cart_items.all():
        total+=item.sub_total()
    tax=(total*2)/100
    grand_total=total+tax

    if request.method=="POST":
        form=CommandeForm(request.POST)
        if form.is_valid():
            data=Commande()
            data.first_name=form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.email=form.cleaned_data["email"]
            data.phone=form.cleaned_data["phone"]
            data.address_line_1=form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country=form.cleaned_data["country"]
            data.state=form.cleaned_data["state"]
            data.order_note=form.cleaned_data["order_note"]
            data.order_total=total
            data.tax=tax
            data.ip=request.META.get("REMOTE_ADDR")
            data.save()

            yr=int(datetime.date.today().strftime("%y"))
            dt=int(datetime.date.today().strftime("%d"))
            mt=int(datetime.date.today().strftime("%m"))
            current_date=datetime.date(yr,dt,mt)

            return HttpResponse("ok")