from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models
from django.conf import settings
import datetime, calendar
from cloudinary.models import CloudinaryField

class Photo(models.Model):
    image = CloudinaryField('image')
  
class Class(models.Model):
    user = models.ForeignKey(User, default=1)
    organisation_name = models.CharField(max_length=200, default='unset')
    name = models.CharField(max_length=50)
    teacher = models.CharField(max_length=20)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    capacity = models.IntegerField(default=10)
    description = models.CharField(max_length = 800)
    price = models.IntegerField(null=True, blank=True)
    total_classes = models.IntegerField(null=True, blank=True)
    image = CloudinaryField('image')
    #fields inherited from classroom
    address = models.CharField(max_length = 100)
    phone_number = models.IntegerField(null=True, blank=True);
    #day of the week booleans
    monday = models.BooleanField(default= False)
    tuesday = models.BooleanField(default= False)
    wednesday = models.BooleanField(default= False)
    thursday = models.BooleanField(default= False)
    friday = models.BooleanField(default= False)
    saturday = models.BooleanField(default= False)
    sunday = models.BooleanField(default= False)
    
    def __str__(self):
        return self.name;

class Client(models.Model):
    organisation_name= models.CharField(max_length=200, default='unset')
    course = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    age = models.IntegerField(default = 4)
    phone = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 10)
    email = models.CharField(max_length = 50)
    address = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name;

class ClientProfile(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    course_id = models.IntegerField()
    organisation = models.CharField(max_length=200)
    name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    age = models.IntegerField(default = 4)
    phone = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 10)
    email = models.CharField(max_length = 20)
    address = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name;
        
class ClassHistory(models.Model):
    user = models.ForeignKey(User, default=1)
    class_name = models.CharField(null=True, max_length = 50)
    registered_date = models.DateTimeField(null=True, blank=True)
    organisation_name = models.CharField(max_length=200, default='unset')
    name = models.CharField(null=True, max_length=50)
    teacher = models.CharField(null=True, max_length=20)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    capacity = models.IntegerField(null=True, default=10)
    description = models.CharField(null=True, max_length = 800)
    price = models.IntegerField(null=True, blank=True)
    image = CloudinaryField('image', null=True)
    #fields inherited from classroom
    address = models.CharField(null=True, max_length = 100)
    phone_number = models.IntegerField(null=True, blank=True);
    
    def __str__(self):
        return self.name;

class StripeInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    business_name = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    stripe_user_id = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.stripe_user_id;
        
        
        
        
        