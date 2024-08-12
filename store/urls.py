from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from store import views


urlpatterns = [
    path('', views.store,name="store"),
    path('category/<slug:category_slug>/', views.store,name="category"),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.details,name="details"),
    path('search/', views.search,name="search"),

]
