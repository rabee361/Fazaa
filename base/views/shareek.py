from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from fcm_django.models import FCMDevice
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.views import BaseAPIView
from django.shortcuts import redirect
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from utils.pagination import CustomPagination
# Create your views here.





class OrganizationTypes(BaseAPIView,generics.ListAPIView):
    queryset = OrganizationType.objects.all()
    serializer_class = OrganizationTypeSerializer


class OrganizatinosListView(BaseAPIView,generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = BranchSerializer

    def get_queryset(self):
        queryset = Branch.objects.all()
        distance = self.request.query_params.get('distance', None)

        if distance:
            try:
                distance = float(distance)

                user_location = Point(35.882744 , 34.885522, srid=4326)
                
                queryset = queryset.filter(
                    location__distance_lte=(user_location, D(km=distance))
                ).annotate(
                    distance=Distance('location', user_location)
                ).order_by('distance').distinct()

            except ValueError:
                pass

        return queryset


class GetOrganizationView(BaseAPIView):
    def get(self,request,pk):

        organization = Organization.objects.get(id=pk)

        socials = SocialMediaUrl.objects.select_related('social_media').filter(organization__id=pk)

        delivery = DeliveryCompanyUrl.objects.select_related('delivery_company').filter(organization__id=pk)

        catalogs = Catalog.objects.filter(organization__id=pk)

        serializer = OrganizationSerializer(organization, many=False , context={'request':request})

        data = {
            **serializer.data,
            'socials': SocialUrlSerializer(socials, many=True , context={'request':request}).data,
            'delivery': DeliveryUrlSerializer(delivery, many=True , context={'request':request}).data,
            'catalogs': CatalogUrlsSerializer(catalogs, many=True , context={'request':request}).data
        }

        return Response(data , status=status.HTTP_200_OK)



class DeleteOrganizationView(generics.DestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer



class SocialMediaUrlView(BaseAPIView):
    def get(self,request,pk):
        socials = SocialMediaUrl.objects.filter(organization__id=pk)
        serializer = SocialMediaUrlSerializer(socials , many=True , context={'request':request})
        return Response(serializer.data , status=status.HTTP_200_OK)


class UpdateSocialMediaUrlView(BaseAPIView , generics.UpdateAPIView):
    queryset = SocialMediaUrl.objects.all()
    serializer_class = SocialMediaUrlSerializer



class SocialMediaView(BaseAPIView , generics.ListAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer




class DeliveryUrlView(BaseAPIView):
    def get(self,request,pk):
        companies = DeliveryCompanyUrl.objects.filter(organization__id=pk)
        serializer = DeliveryCompanyUrlSerializer(companies , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)



class UpdateDeliveryUrlView(generics.UpdateAPIView):
    serializer_class = DeliveryCompanyUrlSerializer
    queryset = DeliveryCompanyUrl.objects.all()




class DeliveryCompanyView(BaseAPIView , generics.ListAPIView):
    queryset = DeliveryCompany.objects.all()
    serializer_class = DeliveryCompanySerializer







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
        serializer = CatalogSerializer(catalogs , many=True , context={'request':request})
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


