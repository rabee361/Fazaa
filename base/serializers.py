from rest_framework.serializers import ModelSerializer , Serializer
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User




class OrganizationListSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id','name','description','logo']


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id','name']




class OrganizationTypeSerializer(ModelSerializer):
    class Meta:
        model = OrganizationType
        fields = ['id','name']




class SocialMediaSerializer(ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = SocialMedia
        fields = ['icon','name']

    def get_icon(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.icon.url)


class SocialMediaUrlSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    social_media = SocialMediaSerializer()
    class Meta:
        model = SocialMediaUrl 
        fields = ['id','organization','short_url','social_media','active']
    
    def get_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())






class DeliveryCompanySerializer(ModelSerializer):
    class Meta:
        model = DeliveryCompany
        fields = '__all__'

    def get_icon(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.icon.url)



class DeliveryCompanyUrlSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    class Meta:
        model = DeliveryCompanyUrl
        fields = ['id','organization','short_url','delivery_company','active']
    
    def get_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())


class CatalogSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Catalog
        fields = ['id','short_url','catalog_type','organization']

    def get_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())


class ReelsGallerySerializer(ModelSerializer):
    class Meta:
        model = ReelsGallery
        fields = '__all__'


class ImagesGallerySerializer(ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = '__all__'



# class NotificationSerializer(ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = '__all__'





class ServiceOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOffer
        fields = '__all__'


class ClientOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOffer
        fields = '__all__'



class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'



class TermsPrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsPrivacy
        fields = '__all__'



class CommonQuestionsSerializer(ModelSerializer):
    class Meta:
        model = CommonQuestion
        fields = '__all__'



class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
    
    def validate_client(self,value):
        if not User.objects.filter(id=value, user_type='CLIENT').exists():
            raise serializers.ValidationError('لا يوجد عميل بهذا الرقم')
        return value







class CatalogUrlsSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    class Meta:
        model = Catalog
        fields = ['catalog_type','short_url']

    def get_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())


class SocialUrlSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    name = serializers.CharField(source='social_media.name')
    icon = serializers.ImageField(source='social_media.icon')
    class Meta:
        model = SocialMediaUrl
        fields = ['short_url','name','icon']

    def get_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())


class DeliveryUrlSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    name = serializers.CharField(source='delivery_company.name')
    icon = serializers.ImageField(source='delivery_company.icon')
    class Meta:
        model = DeliveryCompanyUrl
        fields = ['short_url','name','icon']

    def get_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())


class OrganizationSerializer(ModelSerializer):
    website_short_url = serializers.SerializerMethodField()
    card_url = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ['id','name','description','organization_type','website_short_url','card_url']
    
    def get_website_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_website_url())

    def get_card_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_card_url())

