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
        fields = ['id','full_name','phonenumber','user_type','image']

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
        fields = ['id','full_name','phonenumber','user_type','password2','password']

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




class SignUpClientSerializer(SignUpUserSerializer):
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data, user_type='CLIENT')
        client = Client.objects.create(user=user)
        return user


class SignUpShareekSerializer(SignUpUserSerializer):
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data, user_type='SHAREEK')
        shareek = Shareek.objects.create(user=user)
        return user


class UpdateClientSerializer(ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = CustomUser
        fields = ['full_name','phonenumber','email','image']

    def update(self, instance, validated_data):
        if 'image' in validated_data and validated_data['image'] is None:
            validated_data.pop('image')
        return super().update(instance, validated_data)





class ResetPasswordSerializer(Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        new_password = data.get('new_password')
        validate_password(new_password)
        return data







class ShareekRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True , allow_blank=True)
    job = serializers.CharField(required=False , allow_blank=True)
    email = serializers.EmailField(required=False , allow_blank=True)
    organization_type = serializers.IntegerField(required=True)

    def validate(self, data):
        type_id = data['organization_type']
        try:
            OrganizationType.objects.get(id=type_id)
        except OrganizationType.DoesNotExist:
            raise serializers.ValidationError({'error':['لا يوجد منظمة من هذا النوع']})
        return super().validate(data)


class UpdateShareekSerializer(UpdateClientSerializer):
    job = serializers.CharField(required=False, allow_blank=True)
    organization_type = serializers.IntegerField(required=False)
    organization_name = serializers.CharField(required=False, allow_blank=True)
    commercial_register_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['full_name','phonenumber','email','image','job','organization_type','organization_name','commercial_register_id']
    
    def validate(self, data):
        type_id = data['organization_type']
        try:
            OrganizationType.objects.get(id=type_id)
        except OrganizationType.DoesNotExist:
            raise serializers.ValidationError({'error':['لا يوجد منظمة من هذا النوع']})
        return super().validate(data)

    def update(self, instance, validated_data):
        # Handle organization-related fields if they exist in validated_data
        shareek = Shareek.objects.get(user=instance)
        if any(field in validated_data for field in ['organization_type', 'organization_name', 'commercial_register_id', 'job']):
            org_type = OrganizationType.objects.get(id=validated_data.pop('organization_type', None))
            shareek.update_organization(
                organization_type=org_type,
                organization_name=validated_data.pop('organization_name', None), 
                commercial_register_id=validated_data.pop('commercial_register_id', None),
                job=validated_data.pop('job', None)
            )

        # Remove any None/empty values from validated_data
        validated_data = {k:v for k,v in validated_data.items() if v not in [None, '']}
        
        return super().update(instance, validated_data)



class ShareekSerializer(ModelSerializer):
    class Meta:
        model = Shareek
        fields = '__all__'  


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__' 


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

