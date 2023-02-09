from django.db import models

# Create your models here.
class user(models.Model):
    
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    email = models.CharField(max_length=40, primary_key=True)
    phoneNumber = models.CharField(max_length=20)
    role = models.CharField(max_length=11)
    password = models.CharField(max_length=20)
    #Needs field for toolbox