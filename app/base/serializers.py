from rest_framework.serializers import ModelSerializer , Serializer
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate





class OrganizationSerializer(ModelSerializer):
    website_short_url = serializers.SerializerMethodField()
    card_url = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ['id','name','description','organization_type','website','website_short_url','card_url']
    
    def get_website_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_website_url())

    def get_card_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_card_url())




class OrganizationTypeSerializer(ModelSerializer):
    class Meta:
        model = OrganizationType
        fields = '__all__'




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




class ReelsGallerySerializer(ModelSerializer):
    class Meta:
        model = ReelsGallery
        fields = '__all__'


class ImagesGallerySerializer(ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = '__all__'


class CatalogSerializer(ModelSerializer):
    class Meta:
        model = Catalog
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

