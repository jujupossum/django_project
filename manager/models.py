from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models
from django.conf import settings
import datetime, calendar


class ClassRoom(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    location = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name;

class Class(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete= models.CASCADE)
    name = models.CharField(max_length = 50)
    teacher = models.CharField(max_length = 20)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    capacity = models.IntegerField(default=10)
    description = models.CharField(max_length = 800)
    price = models.IntegerField(null=True, blank=True)
    total_classes = models.IntegerField(null=True, blank=True)
    
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
    course = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    age = models.IntegerField(default = 4)
    phone = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 10)
    email = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.name;

class ClientProfile(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 50)
    age = models.IntegerField(default = 4)
    phone = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 10)
    email = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.name;
        
class ClassHistory(models.Model):
    client_name = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    class_name = models.CharField(max_length = 50)
    registered_date = models.DateTimeField(null=True, blank=True)