from django.urls import path
from . import views
urlpatterns=[
    path('user_home',views.user_home),
    path('shop_home',views.shop_home),
# ===============================================
    path('add_deswedding',views.add_deswedding),

# ===============================================

    path('register',views.register),
    path('',views.shop_login),
    path('logout',views.shop_logout),

    path('destination_wedding',views.destination_wedding),
    path('item_category_list',views.item_category_list),
    path('invitation_list',views.invitation_list),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('view_des_wed/<id>',views.view_des_wed),   

    # path('contact_vendor/<int:id>/<str:type>/', views.contact_vendor, name='contact_vendor'),  
    # path('contact_vendor/<int:id>/', views.contact_vendor, name='contact_vendor'),      
    path('contact_vendor/', views.contact_vendor, name='contact_vendor'),  
    path('contact_vendor/<int:id>/', views.contact_vendor, name='contact_vendor'),  
    path('contact_vendor/<int:id>/<str:type>/', views.contact_vendor, name='contact_vendor'),  

    path('wedding_planners',views.wedding_planners),
    path('photographers',views.photographers),
    path('beauty',views.beauty),


    path('view_bookings/', views.user_view_bookings, name='user_view_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

]