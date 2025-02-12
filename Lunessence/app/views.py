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
    
    
def add_deswedding(req):
    if req.method == 'POST':
        name = req.POST['name']
        about = req.POST['about']
        file = req.FILES['img']
        location = req.POST['location']
        package_price = req.POST['package_price']

        if not all([name, about, file, location, package_price]):
            return HttpResponse("All fields are required.", status=400)

        data = DestinationWedding.objects.create(
            name=name, 
            about=about, 
            img=file, 
            location=location, 
            package_price=package_price
        )
        
        data.save()
        return redirect(shop_home)  

    return render(req, 'shop/add_deswedding.html')

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
    
    
def view_des_wed(req,id):
     if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        weddings=DestinationWedding.objects.get(pk=id)
          
        return render(req,'user/des_wed_details.html',{'DestinationWedding':weddings}) 
     else:
         return redirect(shop_home)  
     
def wedding_planners(req):
    return render(req,'user/event_planners.html')
     
def photographers(req):
    return render(req,'user/photographers.html')

def beauty(req):
    return render(req,'user/beauty.html')
# def user_view_bookings(request):
#     if 'user' in request.session:
#         user = request.user
#         data = Buy.objects.filter(user=user).order_by('-purchase_date')
#         for booking in data:
#             booking.is_cancellable = (date.today() - booking.purchase_date) <= timedelta(days=2)
#         return render(request, 'user/bookings.html', {'data': data})
#     else:
#         return redirect('login')  

# def user_view_bookings(request):
#     if 'user' in request.session:
#         user = request.user
#         data = Buy.objects.filter(user=user).prefetch_related('buyitem_set__item__category').order_by('-purchase_date')
#         for booking in data:
#             booking.is_cancellable = (date.today() - booking.purchase_date) <= timedelta(days=2)
#         return render(request, 'user/bookings.html', {'data': data})
#     else:
#         return redirect('login')

def user_view_bookings(request):
    if 'user' in request.session:
        user = request.user
        data = Buy.objects.filter(user=user).prefetch_related('buyitem_set__item__category').order_by('-purchase_date')
        for booking in data:
            booking.is_cancellable = (date.today() - booking.purchase_date) <= timedelta(days=2)

            # Debugging logs to check if wedding and invitation exist
            print("Booking ID:", booking.id)
            print("Wedding:", booking.wedding)  # Should print the related DestinationWedding object if exists
            print("Invitation:", booking.invitation)  # Should print the related InvitationCard object if exists
            
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

def item_category_list(req):
    categories = ItemCategory.objects.all()
    return render(req, 'user/categories.html', {'categories': categories})



def contact_vendor(request, id=None, type=None): 
    if request.method == "POST":
        customer_name = request.POST.get("name")
        customer_email = request.POST.get("email")
        customer_phone = request.POST.get("phone")
        message = request.POST.get("message", "")

        wedding_id = request.POST.get("wedding_id")
        invitation_id = request.POST.get("invitation_id")
        item_ids = request.POST.getlist("item_ids")  

        buy = Buy.objects.create(
            user=request.user,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            message=message,
            status="Pending",
        )

        if wedding_id:
            buy.wedding = get_object_or_404(DestinationWedding, id=wedding_id)
        if invitation_id:
            buy.invitation = get_object_or_404(InvitationCard, id=invitation_id)

        buy.save()

        for item_id in item_ids:
            item = get_object_or_404(Item, id=item_id)
            BuyItem.objects.create(buy=buy, item=item, quantity=1)

        return redirect("user_view_bookings")

    items = Item.objects.all()
    context = {"items": items}

    if type == "wedding":
        context["wedding"] = get_object_or_404(DestinationWedding, id=id)
    elif type == "invitation":
        context["invitation"] = get_object_or_404(InvitationCard, id=id)

    return render(request, "user/contact_vendor.html", context)




def item_category_list(request):
    categories = ItemCategory.objects.prefetch_related('item_set').all()
    item = Item.objects.all()
    return render(request, "user/categories.html", {"categories": categories, "item": item})

def invitation_list(request):
    categories = InvitationCategory.objects.all()
    invitation_cards = InvitationCard.objects.all()
    return render(request, 'user/invitation.html', {'categories': categories, 'invitation_cards': invitation_cards})


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Buy, id=booking_id)

    if booking.is_cancellable():
        booking.status = 'Cancelled'
        booking.save()
        return redirect("user_view_bookings")

    return redirect("user_view_bookings") 

