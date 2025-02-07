from django.urls import path
from . import views
urlpatterns=[
    path('user_home',views.user_home),
    path('register',views.register),
    path('',views.shop_login),
    path('destination_wedding',views.destination_wedding),


]