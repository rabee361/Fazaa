from django.shortcuts import render
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

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'p'




class OrganizationTypes(BaseAPIView,generics.ListAPIView):
    serializer_class = OrganizationTypeSerializer
    queryset = OrganizationType




class SocialMediaView(BaseAPIView):
    def get(self,request,id):
        socials = SocialMediaLink.objects.filter(organization__id=id)
        serializer = SocialMediaLinkSerializer(socials , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class UpdateSocialMediaLinkView(BaseAPIView):
    def put(self,request):
        pass




class DeliveryLinkView(BaseAPIView):
    def get(self,request,id):
        companies = DeliveryCompanyLink.objects.filter(organization__id=id)
        serializer = DeliveryCompanyLinkSerializer(companies , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    


class UpdateDeliveryLinkView(generics.UpdateAPIView):
    serializer_class = DeliveryCompanyLinkSerializer
    queryset = DeliveryCompanyLink.objects.all()



class OrganizationReelsView(BaseAPIView):
    pagination_class = CustomPagination
    
    def get(self,request,id):
        reels = ReelsGallery.objects.filter(organization__id=id)
        serializer = ReelsGallerySerializer(reels , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class CreateOrganizationReelsView(generics.CreateAPIView):
    serializer_class = ReelsGallerySerializer
    queryset = ReelsGallery.objects.all()


class DeleteOrganizationReelsView(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            ReelsGallery.objects.get(id=id).delete()
            return Response({"message":["تم الحذف بنجاح"]})
        except ReelsGallery.DoesNotExist:
            return Response({"error":["الفيديو غير موجود"]})





class OrganizationGalleryView(BaseAPIView):
    pagination_class = CustomPagination

    def get(self,request,id):
        gallery = ImageGallery.objects.filter(organization__id=id)
        serializer = ImagesGallerySerializer(gallery , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class CreateOrganizationGalleryView(generics.CreateAPIView):
    serializer_class = ImagesGallerySerializer
    queryset = ImageGallery.objects.all()


class DeleteOrganizationGalleryView(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            ImageGallery.objects.get(id=id).delete()
            return Response({"message":["تم الحذف بنجاح"]})
        except ImageGallery.DoesNotExist:
            return Response({"error":["الصورة غير موجود"]})









class OrganizationCatalogView(BaseAPIView):

    def get(self,request,id):
        catalogs = Catalog.objects.filter(organization__id=id)
        serializer = CatalogSerializer(catalogs , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class DeleteOrganizationCatalogView(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            Catalog.objects.get(id=id).delete()
            return Response({"message":["تم الحذف بنجاح"]})
        except Catalog.DoesNotExist:
            return Response({"error":["الكاتالوج غير موجود"]})


class CreateOrganizationCatalogView(generics.CreateAPIView):
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.all()




class ListClientOffers(generics.ListAPIView):
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



class ListServiceOffers(generics.ListAPIView):
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




class CreateCatalogView(generics.CreateAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    

class CatalogView(APIView):
    def get(self , request ,id):
        try:
            catalogs = Catalog.objects.filter(id=id)
            if catalogs.exists():
                serializer = CatalogSerializer(catalogs , many=True)
                return Response(serializer.data , status=status.HTTP_200_OK)
            return Response({"message":"المنظمة هذه لا تملك كاتالوجات"} , status=status.HTTP_404_NOT_FOUND)
        except Catalog.DoesNotExist:
            return Response({"message":"المنظمة غير موجودة"} , status=status.HTTP_404_NOT_FOUND)



class ListTemplatesView(generics.ListAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer