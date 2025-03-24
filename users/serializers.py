from rest_framework.serializers import ModelSerializer , Serializer
from .models import *
from rest_framework import serializers
from base.models import OrganizationType
from django.core.exceptions import ValidationError
from utils.validators import *


class UserSerializer(ModelSerializer):
    image = serializers.SerializerMethodField()
    chat_id = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','full_name','phonenumber','email','user_type','image','get_notifications','chat_id']

    def get_image(self,obj):
        if obj.image:   
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_chat_id(self,obj):
        try:
            chat = SupportChat.objects.get(user=obj)
            return chat.id
        except SupportChat.DoesNotExist:
            return 0



class LoginSerializer(Serializer):
    phonenumber = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phonenumber = data.get('phonenumber')
        password = data.get('password')

        if not phonenumber and not password:
            # Return single error message instead of list
            raise serializers.ValidationError({"error": "رقم الهاتف وكلمة المرور مطلوب"})
        
        validate_required_field(phonenumber, "رقم الهاتف")
        validate_required_field(password, "كلمة المرور")
        validate_phone_format(phonenumber)
        
        return data



class SignUpUserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)  
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phonenumber', 'user_type', 'password2', 'password']

    def validate(self, data):
        phonenumber = data.get('phonenumber' , None)
        password = data.get('password' , None)
        password2 = data.get('password2' , None)
        if not phonenumber or not password or not password2:
            raise ErrorResult({"error": "رقم الهاتف وكلمة المرور مطلوب"})

        # Validate passwords
        validate_password_match(password, password2)
        validate_password_strength(password)
            
        return data

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except ValidationError as e:
            raise serializers.ValidationError({"error": str(e)})




class SignUpClientSerializer(SignUpUserSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, user_type='CLIENT')
        client = Client.objects.create(user=user)
        return user


class SignUpShareekSerializer(SignUpUserSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, user_type='SHAREEK')
        return user

class UpdateClientSerializer(ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['full_name','phonenumber','email','image']

    def validate(self, data):
        validate_required_field(data['full_name'], "الاسم الكامل")
        validate_required_field(data['phonenumber'], "رقم الهاتف")
        return data


class ChangePasswordSerializer(Serializer):
    password = serializers.CharField(required=True , error_messages={
        'required': 'كلمة المرور مطلوبة',
        'blank': 'كلمة المرور مطلوبة'
    })
    new_password = serializers.CharField(required=True , error_messages={
        'required': 'كلمة المرور الجديدة مطلوبة',
        'blank': 'كلمة المرور الجديدة مطلوبة'
    })
    confirm_password = serializers.CharField(required=True , error_messages={
        'required': 'تأكيد كلمة المرور مطلوب',
        'blank': 'تأكيد كلمة المرور مطلوب'
    })

    def validate(self, data):
        validate_password_match(data['confirm_password'], data['new_password'])
        validate_password_strength(data['new_password'])
        return data




class ResetPasswordSerializer(Serializer):  
    new_password = serializers.CharField(required=True , error_messages={
        'required': 'كلمة المرور مطلوبة',
        'blank': 'كلمة المرور مطلوبة'
    })
    confirm_password = serializers.CharField(required=True , error_messages={
        'required': 'تأكيد كلمة المرور مطلوب',
        'blank': 'تأكيد كلمة المرور مطلوب'
    })

    def validate(self, attrs):
        validate_password_match(attrs['confirm_password'], attrs['new_password'])
        validate_password_strength(attrs['new_password'])
        return attrs








class ShareekRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(error_messages={
        'required': 'الاسم الكامل مطلوب',
        'blank': 'الاسم الكامل مطلوب'
    })
    job = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    organization_type = serializers.IntegerField(error_messages={
        'required': 'نوع المنظمة مطلوب',
        'null': 'نوع المنظمة مطلوب',
        'blank': 'نوع المنظمة مطلوب'
    })
    organization_name = serializers.CharField(error_messages={
        'required': 'اسم المنظمة مطلوب',
        'blank': 'اسم المنظمة مطلوب',
        'null': 'اسم المنظمة مطلوب'
    })
    image = serializers.ImageField(required=False)

    def validate(self, data):
        type_id = data.get('organization_type')
        validate_organization_type(type_id)
        return data


class UpdateShareekSerializer(UpdateClientSerializer):
    job = serializers.CharField(required=False, allow_blank=True)
    organization_type_id = serializers.IntegerField(required=False)
    organization_name = serializers.CharField(required=False, allow_blank=True)
    commercial_register_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['full_name','phonenumber','email','image','job','organization_type_id','organization_name','commercial_register_id']
    
    def validate(self, data):
        type_id = data['organization_type_id']
        try:
            OrganizationType.objects.get(id=type_id)
        except OrganizationType.DoesNotExist:
            # Return single error message instead of list
            raise ErrorResult({"error": "لا يوجد منظمة من هذا النوع"})
        return super().validate(data)

    def update(self, instance, validated_data):
        # Handle organization-related fields if they exist in validated_data
        shareek = Shareek.objects.get(user=instance)
        if any(field in validated_data for field in ['organization_type_id', 'organization_name', 'commercial_register_id', 'job']):
            org_type = OrganizationType.objects.get(id=validated_data.pop('organization_type_id', None))
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
        exclude = ['user']


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__' 


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'



class UserNotificationSerializer(ModelSerializer):
    class Meta:
        model = UserNotification
        exclude = ['user']




class SupportChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportChat
        fields = '__all__'



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'