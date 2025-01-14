from rest_framework import serializers
from student.models import *

class employeeserializer(serializers.ModelSerializer):
       class Meta:
              model = EmployeeData
              fields='__all__'