from django.urls import path
from . import views
urlpatterns=[
    path('',views.user_home),
    path('register',views.register),
    path('login',views.login),

]