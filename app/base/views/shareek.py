from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from fcm_django.models import FCMDevice
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from app.users.views.common import BaseAPIView
from django.shortcuts import redirect
# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'p'




class OrganizationTypes(BaseAPIView,generics.ListAPIView):
    serializer_class = OrganizationTypeSerializer
    queryset = OrganizationType


class GetOrganizationView(BaseAPIView, generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()


class DeleteOrganizationView(generics.DestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer



class SocialMediaUrlView(BaseAPIView):
    def get(self,request,id):
        socials = SocialMediaUrl.objects.filter(organization__id=id)
        serializer = SocialMediaUrlSerializer(socials , many=True , context={'request':request})
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class UpdateSocialMediaUrlView(BaseAPIView , generics.UpdateAPIView):
    serializer_class = SocialMediaUrlSerializer
    queryset = SocialMediaUrl.objects.all()




class DeliveryUrlView(BaseAPIView):
    def get(self,request,id):
        companies = DeliveryCompanyUrl.objects.filter(organization__id=id)
        serializer = DeliveryCompanyUrlSerializer(companies , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)



class UpdateDeliveryUrlView(generics.UpdateAPIView):
    serializer_class = DeliveryCompanyUrlSerializer
    queryset = DeliveryCompanyUrl.objects.all()



class ReelsView(BaseAPIView):
    pagination_class = CustomPagination
    
    def get(self,request,id):
        reels = ReelsGallery.objects.filter(organization__id=id)
        serializer = ReelsGallerySerializer(reels , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class CreateReelsView(generics.CreateAPIView):
    serializer_class = ReelsGallerySerializer
    queryset = ReelsGallery.objects.all()


class DeleteReelsView(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            ReelsGallery.objects.get(id=id).delete()
            return Response({"message":["تم الحذف بنجاح"]})
        except ReelsGallery.DoesNotExist:
            return Response({"error":["الفيديو غير موجود"]})





class GalleryView(BaseAPIView):
    pagination_class = CustomPagination

    def get(self,request,id):
        gallery = ImageGallery.objects.filter(organization__id=id)
        serializer = ImagesGallerySerializer(gallery , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class CreateGalleryView(generics.CreateAPIView):
    serializer_class = ImagesGallerySerializer
    queryset = ImageGallery.objects.all()


class DeleteGalleryView(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            ImageGallery.objects.get(id=id).delete()
            return Response({"message":["تم الحذف بنجاح"]})
        except ImageGallery.DoesNotExist:
            return Response({"error":["الصورة غير موجود"]})









class CatalogView(BaseAPIView):

    def get(self,request,id):
        catalogs = Catalog.objects.filter(organization__id=id)
        serializer = CatalogSerializer(catalogs , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    


class DeleteCatalogView(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            Catalog.objects.get(id=id).delete()
            return Response({"message":["تم الحذف بنجاح"]})
        except Catalog.DoesNotExist:
            return Response({"error":["الكاتالوج غير موجود"]})


class CreateCatalogView(generics.CreateAPIView):
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.all()




class ClientOfferView(generics.ListAPIView):
    def get(self,request,id):
        offers = ClientOffer.objects.filter(organization__id=id)
        serializer = ClientOfferSerializer(offers , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class CreateClientOffer(generics.CreateAPIView):
    queryset = ClientOffer
    serializer_class = ClientOfferSerializer


class UpdateClientOffer(generics.ListAPIView):
    queryset = ClientOffer
    serializer_class = ClientOfferSerializer


class DeleteClientOffer(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            ClientOffer.objects.get(id=id).delete()
            return Response({"message":["تم الحذف بنجاح"]})
        except ClientOffer.DoesNotExist:
            return Response({"error":["العرض غير موجود"]})



class ServiceOfferView(generics.ListAPIView):
    def get(self,request,id):
        offers = ServiceOffer.objects.filter(organization__id=id)
        serializer = ServiceOfferSerializer(offers , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class CreateServiceOffer(generics.CreateAPIView):
    queryset = ServiceOffer
    serializer_class = ServiceOfferSerializer


class UpdateServiceOffer(generics.ListAPIView):
    queryset = ServiceOffer
    serializer_class = ServiceOfferSerializer

class DeleteServiceOffer(BaseAPIView):
    def delete(self,request,id):
        try:
            ServiceOffer.objects.get(id=id).delete()
            return Response({"message":["تم الحذف بنجاح"]})
        except ServiceOffer.DoesNotExist:
            return Response({"error":["العرض غير موجود"]})




class TemplatesView(generics.ListAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer