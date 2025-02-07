from django.shortcuts import render,redirect
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
