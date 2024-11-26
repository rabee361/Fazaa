from rest_framework.serializers import ModelSerializer , Serializer
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate





# class OrganizationSerializer(ModelSerializer):
#     class Meta:
#         model = Organization
#         fields = '__all__'




# class OrganizationTypeSerializer(ModelSerializer):
#     class Meta:
#         model = OrganizationType
#         fields = '__all__'




# class SocialMediaSerializer(ModelSerializer):
#     class Meta:
#         model = SocialMedia
#         fields = '__all__'



class SocialMediaLinkSerializer(ModelSerializer):
    class Meta:
        model = SocialMediaLink 
        fields = '__all__'



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


class DeliveryCompanyLinkSerializer(ModelSerializer):
    class Meta:
        model = DeliveryCompanyLink
        fields = '__all__'


# class DeliveryCompanySerializer(ModelSerializer):
#     class Meta:
#         model = DeliveryCompany
#         fields = '__all__'
