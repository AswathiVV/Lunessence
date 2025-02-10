from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone


def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    else:
    
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
                    req.session['shop']=uname      
                    return redirect(shop_home)
                else:
                    req.session['user']=uname      
                    return redirect(user_home)
            else:
                messages.warning(req,"invalid uname or password")  
        return render(req,'login.html') 
    
def shop_logout(req):
    logout(req)
    req.session.flush()              
    return redirect(shop_login) 

def  register(req):
     if req.method=='POST':
        name=req.POST['name']       
        email=req.POST['email']
        password=req.POST['password']
        send_mail('Lunessence registration', 'Welcome to Lunessence! Your account has been created successfully', settings.EMAIL_HOST_USER, [email])

        try:
            data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"user details already exits")
            return redirect(register)
     else:
         return render(req,'register.html')
     

#--------------------- admin-------------------------------------------------------------------------------------------  
def shop_home(req):
    if 'shop' in req.session:
        return render(req,'shop/shop_home.html')
    else:
        return redirect(shop_login)

# #------------------------------------- User--------------------------------------------------------------

def user_home(req):
    if 'user' in req.session:
        return render(req,'user/user_home.html')  
    else:
        return redirect(shop_login)
    
def destination_wedding(request):
    if 'user' in request.session: 
        weddings = DestinationWedding.objects.all() 
        return render(request, 'user/destination_wedding.html', {'weddings': weddings})
    else:
        return redirect('login')  
    
# def view_cake(req,id):
#      if 'user' in req.session:
#         user=User.objects.get(username=req.session['user'])
#         weddings=DestinationWedding.objects.get(pk=id)
#         try:
#             cart=Cart.objects.get(Cake=cake,user=user)
#         except:
#             cart=None    
#         return render(req,'user/view_cakes.html',{'cake':cake,'cart':cart}) 
#      else:
#          return redirect(shop_login)      
def view_des_wed(req,id):
     if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        weddings=DestinationWedding.objects.get(pk=id)
        # try:
        #     cart=Cart.objects.get(Cake=cake,user=user)
        # except:
        #     cart=None    
        return render(req,'user/des_wed_details.html',{'DestinationWedding':weddings}) 
     else:
         return redirect(shop_home)   

# def add_to_wishlist(req,id):
#      Product=DestinationWedding.objects.get(pk=id)
#      print(Product)
#      user=User.objects.get(username=req.session['user'])
#      print(user)
#      data=Cart.objects.create(user=user,cake=Product)
#      data.save()
#      return redirect(cart_display)     

# from django.shortcuts import render, redirect, 
# from .models import Buy, Category
# from django.contrib.auth.decorators import login_required

# @login_required
# def contact_vendor(request, id):
#     category = get_object_or_404(Category, id=id) 

#     if request.method == 'POST':
#         customer_name = request.POST.get('name')
#         customer_email = request.POST.get('email')
#         customer_phone = request.POST.get('phone')

#         buy = Buy.objects.create(
#             user=request.user,
#             category=category,
#             customer_name=customer_name,
#             customer_email=customer_email,
#             customer_phone=customer_phone,
#             price=category.price 
#         )
#         buy.save()

#         return redirect('user_view_bookings')

#     return render(request, 'user/contact_vendor.html', {
#         'category': category,
#     })


# def contact_vendor(request, id):
#     destination_wedding = get_object_or_404(DestinationWedding, id=id)
#     if request.method == 'POST':
#         customer_name = request.POST.get('name')
#         customer_email = request.POST.get('email')
#         customer_phone = request.POST.get('phone')
#         message = request.POST.get('message', '') 

#         buy = Buy.objects.create(
#             user=request.user,
#             customer_name=customer_name,
#             customer_email=customer_email,
#             customer_phone=customer_phone,
#             message=message,
#             status='Pending',
#         )
#         buy.save()


#         return redirect('user_view_bookings')  

#     return render(request, 'user/contact_vendor.html', {
#         'destination_wedding': destination_wedding,
#     })



def contact_vendor(request, id):
    destination_wedding = get_object_or_404(DestinationWedding, id=id)
    if request.method == 'POST':
        customer_name = request.POST.get('name')
        customer_email = request.POST.get('email')
        customer_phone = request.POST.get('phone')
        message = request.POST.get('message', '')  # Optional field

        # Save the Buy entry
        buy = Buy.objects.create(
            user=request.user,
            category=destination_wedding.category,  # Assuming DestinationWedding has a category field
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            message=message,
            status='Pending',
        )
        buy.save()

        # return redirect('user_home')  

    return render(request, 'user/contact_vendor.html', {
        'destination_wedding': destination_wedding,
    })

def user_view_bookings(request):
    if 'user' in request.session:
        user = request.user
        data = Buy.objects.filter(user=user).order_by('-purchase_date')  # Retrieve bookings for the logged-in user
        for booking in data:
            booking.is_cancellable = (date.today() - booking.purchase_date) <= timedelta(days=2)
        return render(request, 'user/bookings.html', {'data': data})
    else:
        return redirect('login')  

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Buy, id=booking_id, user=request.user)
    if booking.status == 'Pending' and (date.today() - booking.purchase_date).days <= 2:
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, "Booking has been canceled successfully.")
    else:
        messages.error(request, "Booking cannot be canceled.")
    return redirect('user_view_bookings')

