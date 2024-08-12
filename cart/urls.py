from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from great import settings
from . import views


urlpatterns = [

    path('', views.cart,name="cart"),
    path('add/<slug:product_slug>', views.add_to_cart,name="add_to_cart"),
    path('retrieve/<slug:product_slug>/<int:order_id>', views.retrieve,name="retrieve"),
    path('remove/<int:order_id>', views.remove,name="remove"),
    path('checkout/', views.checkout,name="checkout"),
]