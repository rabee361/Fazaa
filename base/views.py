from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from fcm_django.models import FCMDevice
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from utils.helper import generate_code
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'p'





class SocialMediaView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SocialMediaLinkSerializer
    
    def get_queryset(self,request,id):
        return SocialMediaLink.objects.filter(organization__id=id)
    

class UpdateSocialMediaLinkView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SocialMediaLinkSerializer
    queryset = SocialMediaLink.objects.all()




class DeliveryLinkView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryCompanyLinkSerializer
    
    def get_queryset(self,request,id):
        return SocialMediaLink.objects.filter(organization__id=id)
    

class UpdateDeliveryLinkView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryCompanyLinkSerializer
    queryset = DeliveryCompanyLink.objects.all()



class OrganizationReelsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = ReelsGallerySerializer
    
    def get_queryset(self,request,id):
        return ReelsGallery.objects.filter(organization__id=id)


class CreateOrganizationReelsView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReelsGallerySerializer
    queryset = ReelsGallery.objects.all()


class DeleteOrganizationReelsView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReelsGallerySerializer
    queryset = ReelsGallery.objects.all()






class OrganizationGalleryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImagesGallerySerializer
    pagination_class = CustomPagination

    def get_queryset(self,request,id):
        return ImageGallery.objects.filter(organization__id=id)


class CreateOrganizationGalleryView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImagesGallerySerializer
    queryset = ImageGallery.objects.all()


class DeleteOrganizationGalleryView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImagesGallerySerializer
    queryset = ImageGallery.objects.all()









class OrganizationCatalogView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CatalogSerializer
    pagination_class = CustomPagination

    def get_queryset(self,request,id):
        return Catalog.objects.filter(organization__id=id)

class DeleteOrganizationCatalogView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.all()

class CreateOrganizationCatalogView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.all()




class ListClientOffers(generics.ListAPIView):
    pass

class CreateClientOffer(generics.CreateAPIView):
    pass

class UpdateClientOffer(generics.ListAPIView):
    pass

class DeleteClientOffer(generics.DestroyAPIView):
    pass



class ListShareekOffers(generics.ListAPIView):
    pass

class CreateShareekOffer(generics.CreateAPIView):
    pass

class UpdateShareekOffer(generics.ListAPIView):
    pass

class DeleteShareekOffer(generics.DestroyAPIView):
    pass





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
