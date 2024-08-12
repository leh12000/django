
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.dashboard,name="dashboard"),
    path('signup/', views.signup_user,name="signup_user"),
    path('signin/', views.signin_user,name="signin_user"),
    path('logout/', views.logout_user,name="logout_user"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path("activate/<uidb64>/<token>",views.activate,name="activate"),
    path("rest",views.rest,name="rest"),
    path("restpassword/<uidb64>/<token>",views.restpassword,name="restpassword"),
    path("restpage",views.restpage,name="restpage"),

]
