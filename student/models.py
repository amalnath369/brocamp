from django.db import models
from django.contrib.auth.hashers import make_password

class EmployeeData(models.Model):
    Name = models.CharField(max_length=100, null=False)
    Dept = models.CharField(max_length=100, null=False)
    Designation=models.CharField(max_length=100,null=False)
    Work_location=models.CharField(max_length=50,null=False)
    Empid = models.CharField(max_length=30, null=False, primary_key=True)
    password = models.CharField(max_length=128, null=False) 
    phonenumber=models.CharField(max_length=10,null=False,unique=True)
    email=models.EmailField(max_length=255,null=False,default='test')

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.Empid


class StudentData(models.Model):
      HUB_CHOICES = [
        ('BCK', 'Calicut'),
        ('BCE', 'Kochi'),
        ('BCT', 'Thiruvananthapuram'),
        ('BCB', 'Bangalore'),
        ('BCR', 'Remote'),
        ('BCCO','Coimbatore'),
        ('BCCH','Chennai')
      ]
      name=models.CharField(max_length=100,null=False)
      hub=models.CharField(max_length=6,null=False,choices=HUB_CHOICES,default='test')
      batch=models.CharField(max_length=20,null=False)
      domain=models.CharField(max_length=20,null=False)
      email=models.EmailField(max_length=255,null=False,default='example@example.com')
      phonenumber=models.CharField(max_length=10,null=False,unique=True)
      guardianname=models.CharField(max_length=100,null=False,default='test')
      guardiannumber=models.CharField(max_length=10)
      mentor=models.ForeignKey(EmployeeData ,on_delete=models.CASCADE)
      

      def __str__(self):
        return self.name
      