from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
        
class EmployeeGroupSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=Manager.objects.all(), required=True)
    class Meta: 
        model = EmployeeGroup
        fields = '__all__'
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'password', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = Employee(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=Manager.objects.all())
    assigned_group = serializers.PrimaryKeyRelatedField(queryset=EmployeeGroup.objects.all())
    class Meta:
        model = Task
        fields = '__all__' 

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__' 
        
class CustomTokenObtain(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        is_manager = Manager.objects.filter(user=self.user).exists()
        data['is_manager'] = is_manager
        return data