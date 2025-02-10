from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

    
class DestinationWedding(models.Model):
    name = models.CharField(max_length=255) 
    about = models.TextField() 
    img = models.FileField()
    location = models.CharField(max_length=255) 
    package_price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    img = models.FileField()
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.FileField()

    def __str__(self):
        return self.name    
  
class Invitation_Category(models.Model):
    img = models.FileField()
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name    
    
class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    wedding = models.ForeignKey(DestinationWedding, on_delete=models.CASCADE,null=True) 
    items = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=255)  
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)  
    message = models.TextField(blank=True, null=True)
    purchase_date = models.DateField(auto_now_add=True)  
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )      
    def is_cancellable(self):
        return (date.today() - self.purchase_date) <= timedelta(days=2)
    
    def calculate_total(self):
        total_price = sum(buy_item.item.price * buy_item.quantity for buy_item in self.buyitem_set.all())
        return total_price





    