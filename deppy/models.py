from django.db import models

# Create your models here.

class Users(models.Model):
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    password= models.CharField(max_length=200)

class Chats(models.Model):
    email = models.CharField(max_length=100)
    inpchat = models.TextField()
    replychat = models.TextField()
    sessionuid = models.CharField(max_length=100)

class Sentiments(models.Model):
    sessionno = models.IntegerField(null=True,blank=True)
    email = models.CharField(max_length=100)
    sessionuid = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=100,default='NA')
    
    
    

