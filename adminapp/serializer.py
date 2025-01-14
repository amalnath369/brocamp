from rest_framework import serializers
from adminapp.models import *

class adminserialiser(serializers.ModelSerializer):
      class Meta:
            model= admin_data
            fields='__all__'