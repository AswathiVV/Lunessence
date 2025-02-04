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

def login(req):
    return render(req,'login.html')
def register(req):
    return render(req,'register.html')
def user_home(req):
    return render(req,'user/user_home.html')
