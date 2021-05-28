from django.core.checks import messages
from django.db import models
from datetime import datetime
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.
class Registration(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100,unique=True)
    username=models.CharField(max_length=100,unique=True,primary_key=True)
    password=models.CharField(max_length=100)
    img=models.ImageField(upload_to='pics')
class Groups(models.Model):
    room=models.CharField(max_length=255,primary_key=True)
    created_by=models.ForeignKey(Registration,on_delete=CASCADE)
class Messages(models.Model):
    username=models.CharField(max_length=255)
    room=models.ForeignKey(Groups,on_delete=models.CASCADE)
    message=models.TextField()
    datetime=models.DateTimeField(default=datetime.now,blank=True)
class Personal(models.Model):
    me=models.ForeignKey(Registration,on_delete=CASCADE,related_name='me')
    user=models.ForeignKey(Registration,on_delete=CASCADE,related_name='user')
class PersonalMessage(models.Model):
    people=models.ForeignKey(Personal,on_delete=models.CASCADE)
    sender=models.CharField(max_length=255)
    messages=models.TextField()
    datetime=models.DateTimeField(default=datetime.now,blank=True)
class OnlineOffline(models.Model):
    user=models.ForeignKey(Registration,on_delete=CASCADE) 
    status=models.CharField(max_length=255)