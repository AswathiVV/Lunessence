from django.urls import path
from . import views
urlpatterns=[
    path('user_home',views.user_home),
    path('register',views.register),
    path('',views.shop_login),
    path('logout',views.shop_logout),

    path('destination_wedding',views.destination_wedding),
    path('item_category_list',views.item_category_list),
    path('invitation_list',views.invitation_list),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('view_des_wed/<id>',views.view_des_wed),   

    path('contact_vendor/<int:id>/<str:type>/', views.contact_vendor, name='contact_vendor'),  # Pattern 1
    path('contact_vendor/<int:id>/', views.contact_vendor, name='contact_vendor'),           # Pattern 2



    # path('contact_vendor/<id>', views.contact_vendor, name='contact_vendor'),
    # path('cancel-order/<int:id>/', views.cancel_order, name='cancel_order'),
    # path('bookings/', views.booking_list, name='booking_list'),
    path('view_bookings/', views.user_view_bookings, name='user_view_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

]