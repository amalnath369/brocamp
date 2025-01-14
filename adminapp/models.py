from django.db import models

# Create your models here.
class admin_data(models.Model):
        name=models.CharField(max_length=100,null=False)
        empid=models.CharField(max_length=20,null=False)
        password = models.CharField(max_length=128, null=False) 
        phonenumber=models.CharField(max_length=10,null=False,unique=True)
        email=models.EmailField(max_length=255,null=False,unique=True)