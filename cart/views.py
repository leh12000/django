from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import messages
# Create your views here.

from .models import Cart,Order
from store.models import Product,Variations


def cart(request):
    user=request.user
    if user:
        cart,created=Cart.objects.get_or_create(user=user)
        orders=cart.orders.all()
        total=cart.total_price()
        tax=(2*total)/100
        grand_total=total+tax
        return render(request,'store/cart.html',{"orders":orders,"total":total,"tax":tax,"grand_total":grand_total})




def add_to_cart(request,product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    user = request.user

    try:
        cart,created=Cart.objects.get_or_create(user=user)
    except:
        messages.info(request, "Create or Sign in to your account before adding any product.")
        return redirect("signin_user")

    if request.method=="POST":
        list_variation=[]
        for v in request.POST:
            key=v
            value=request.POST.get(key)
            try:
                variation = Variations.objects.get(product=product, category=key,value=value )
                list_variation.append(variation)
                print(variation)
            except:
                pass



        exist=Order.objects.filter(product=product,user=user,is_active=True).exists()
        if exist:
            variation_orders=[]
            orders=Order.objects.filter(product=product,user=user,is_active=True)
            id_order=[]
            for o in orders.all():
                variation_orders.append(list(o.variations.all()))
                id_order.append(o.id)

            if list_variation in variation_orders:
                pos=variation_orders.index(list_variation)
                id_i=id_order[pos]
                order=Order.objects.get(product=product,user=user,is_active=True,id=id_i)
                order.quantity += 1
                order.save()
            else:
                order=Order.objects.create(product=product,user=user)
                order.quantity += 1
                order.save()
                if list_variation:
                    for v in list_variation:
                        order.variations.add(v)
                    order.save()
                cart.orders.add(order)
                cart.save()

        else:
            order = Order.objects.create(product=product, user=user, is_active=True)
            order.quantity += 1
            order.save()
            if list_variation:
                for v in list_variation:
                    print(v)
                    order.variations.add(v)
                order.save()
            cart.orders.add(order)
            cart.save()
    return redirect('cart')


def retrieve(request,product_slug,order_id):
    user=request.user
    cart=user.cart
    if user:
        try:
            order = Order.objects.get(user=user,is_active=True,id=order_id)
            orders=cart.orders.all()
            if order in orders:
                if order.quantity>1:
                    order.quantity+=-1
                    order.save()
                else:
                    order.delete()
        except:
            pass
    return redirect('cart')

def remove(request,order_id):
    user = request.user
    cart = user.cart
    if user:
        order = Order.objects.get(user=user, is_active=True,id=order_id)
        orders = cart.orders.all()
        if order in orders:
            order.delete()

    return redirect('cart')


def checkout(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    orders = cart.orders.all()
    total = cart.total_price()
    tax = (2 * total) / 100
    grand_total = total + tax
    return render(request, "store/checkout.html",{"orders": orders, "total": total, "tax": tax, "grand_total": grand_total})
