from rest_framework.serializers import ModelSerializer , Serializer
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from app.base.models import OrganizationType
from app.base.serializers import OrganizationTypeSerializer

class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','fullName','phonenumber','user_type','image']

class LoginSerializer(Serializer):
    phonenumber = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phonenumber = data.get('phonenumber')
        password = data.get('password')

        if not phonenumber or not password:
            raise serializers.ValidationError({"error":["رقم الهاتف وكلمة المرور مطلوب"]})
        
        return data



class SignUpUserSerializer(ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','fullName','phonenumber','user_type','password2','password']

    def validate(self, data):
        phonenumber = data.get('phonenumber')
        password = data.get('password')
        password2 = data.get('password2')
 
        if password != password2:
            raise serializers.ValidationError({'error':['كلمات المرور غير متطابقة']})        
        if CustomUser.objects.filter(phonenumber=phonenumber).exists():
            raise serializers.ValidationError({'error': ['رقم الهاتف موجود بالفعل']})
        
        validate_password(password)
        return data
       
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    



class ResetPasswordSerializer(Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        new_password = data.get('new_password')
        validate_password(new_password)
        return data







class ShareekRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)
    job = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        type_id = attrs.get('organization_type')
        if not OrganizationType.objects.get(id=type_id):
            raise serializers.ValidationError('لا يوجد منظمة من هذا النوع')
        
        return super().validate(attrs)



class ShareekSerializer(ModelSerializer):
    class Meta:
        model = Shareek
        fields = '__all__'  


# class ClientSerializer(ModelSerializer):
#     class Meta:
#         model = Client
#         fields = '__all__' 


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

