from django.urls import path
from . import views
urlpatterns=[
    path('user_home',views.user_home),
    path('register',views.register),
    path('',views.shop_login),
    path('logout',views.shop_logout),

    path('destination_wedding',views.destination_wedding),

    path('view_des_wed/<id>',views.view_des_wed),   

]