# import serializer from rest_framework
from rest_framework import serializers
from .models import Employee

# create a serializer
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','name','date','jsonData']
