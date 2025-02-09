from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class DestinationWedding(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=255) 
    about = models.TextField() 
    img = models.FileField()
    location = models.CharField(max_length=255) 
    # estimated_guests = models.PositiveIntegerField()
    # event_date = models.DateField()
    package_price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return self.name
    
class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
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
    