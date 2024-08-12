
from django.contrib import admin
from django.urls import path, include
from orders import views


urlpatterns = [
    path('place_order/',views.placeOrder,name="placeOrder"),
]
