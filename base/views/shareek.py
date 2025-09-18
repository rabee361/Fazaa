from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from datetime import datetime
from ..models import *
from fcm_django.models import FCMDevice
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.db.models import Q, Min, Count, F, Subquery, OuterRef
from utils.views import BaseAPIView
from django.shortcuts import redirect
from users.models import Shareek
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from utils.pagination import CustomPagination
from users.serializers import UserSerializer
from django.db.models import FloatField
from django.db.models.functions import Cast
from utils.mixins import OrganizationCheckMixin
# Create your views here.




class OrganizationTypes(BaseAPIView,generics.ListAPIView):
    queryset = OrganizationType.objects.all()
    serializer_class = OrganizationTypeSerializer


class OrganizationsListView(BaseAPIView,generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = BranchListSerializer
    queryset = Branch.objects.select_related('organization').all()

    def get_queryset(self):
        queryset = super().get_queryset()
        distance_limit = self.request.query_params.get('distance', 1000)
        org_types = self.request.query_params.get('type', '')
        name = self.request.query_params.get('name', '')
        order = self.request.query_params.get('order', 0)  # visits / distance / offers / id
        long = self.request.query_params.get('long', None)  
        lat = self.request.query_params.get('lat', None)  
        order = int(order)
        # Convert distance_limit to float
        try:
            distance_limit = float(distance_limit) * 1000
        except ValueError:
            distance_limit = 1000000.0  # Default distance if invalid

        # Apply organization type filter if provided
        if org_types:
            org_types = org_types.split(',')    
            valid_type_ids = [int(type_id) for type_id in org_types if type_id.isdigit()]
            if valid_type_ids:
                queryset = queryset.filter(organization__organization_type_id__in=valid_type_ids)
        # Process user location for distance calculations
        user_location = None
        if long and lat:
            try:
                long_float = float(long)
                lat_float = float(lat)
                user_location = Point(long_float, lat_float, srid=4326)
            except (ValueError, TypeError):
                pass
        # Filter and annotate branches with distance if user location provided
        print("rrrrrrr",user_location)
        if user_location:
            # First, annotate distances without casting
            queryset = queryset.annotate(distance=Distance('location', user_location))
            
            # Debug print to see actual distances
            for branch in queryset:
                print(f"Branch {branch.name}: {branch.distance.m} meters")
            
            # Then filter with explicit comparison
            queryset = queryset.filter(
                distance__lte=distance_limit
            )
            
            # Verify the filter worked
            print(f"After filtering - distance limit: {distance_limit}m")
            print(f"Filtered branches: {list(queryset.values_list('name', flat=True))}")

        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(organization__name__icontains=name))
        
        # Order the results based on the specified order parameter
        if order == 1:
            queryset = queryset.order_by('-visits')
            
        elif order == 2:
            # Count client offers for each organization
            queryset = queryset.annotate(
            client_offers_count=Count('organization__clientoffer', distinct=True))
            queryset = queryset.order_by('-client_offers_count')

        elif order == 3 and user_location:
            queryset = queryset.order_by('distance')

        else:
            # Default ordering by id
            queryset = queryset.order_by('-id')
        
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['distance_limit'] = self.request.query_params.get('distance', 1000)
        context['long'] = self.request.query_params.get('long', None)
        context['lat'] = self.request.query_params.get('lat', None)
        return context


class OrganizationInfoView(BaseAPIView, OrganizationCheckMixin):
    def get(self, request, id):
        organization = self.get_organization(id)
        serializer = OrganizationSerializer(organization, context={'request': request})
        branches_serializer = BranchSerializer(organization.branch_set.all(), many=True)
        client_offers = ListClientOfferSerializer(organization.clientoffer_set.all(), many=True , context={'request':request})
        return Response({
            **serializer.data,
            'branches': branches_serializer.data,
            'client_offers': client_offers.data
        }, status=status.HTTP_200_OK)


class GetOrganizationView(BaseAPIView):
    def get(self,request,pk):
        try:
            organization = Organization.objects.get(id=pk)
            client_offers = ClientOffer.objects.filter(Q(organization__id=pk) & Q(expiresAt__gte=datetime.now()))
            branches = Branch.objects.filter(organization__id=pk)
            reels = ReelsGallery.objects.filter(organization__id=pk)
            socials = SocialMediaUrl.objects.select_related('social_media').filter(Q(organization__id=pk) & Q(active=True) & Q(url__isnull=False))
            delivery = DeliveryCompanyUrl.objects.select_related('delivery_company').filter(Q(organization__id=pk) & Q(active=True) & Q(url__isnull=False))
            catalogs = Catalog.objects.filter(organization__id=pk)
            gallery = ImageGallery.objects.filter(organization__id=pk)

            try:
                shareek_user = Shareek.objects.select_related('user').filter(organization=organization).first().user
                shareek_user_serializer = UserSerializer(shareek_user, many=False, context={'request':request})
            except Shareek.DoesNotExist:
                return ErrorResult("لا يوجد شريك مرتبط بهذه المنظمة")
            organization_serializer = OrganizationSerializer(organization, many=False , context={'request':request})

            data = {
                **shareek_user_serializer.data,
                **organization_serializer.data,
                'gallery': ImagesGallerySerializer(gallery, many=True, context={'request':request}).data,
                'reels': ReelsGallerySerializer(reels, many=True, context={'request':request}).data,
                'socials': SocialUrlSerializer(socials, many=True , context={'request':request}).data,
                'delivery': DeliveryUrlSerializer(delivery, many=True , context={'request':request}).data,
                'catalogs': CatalogUrlsSerializer(catalogs, many=True , context={'request':request}).data,
                'client_offers': ListClientOfferSerializer(client_offers, many=True , context={'request':request}).data,
                'branches': BranchSerializer(branches , many=True).data
            }

            return Response(data , status=status.HTTP_200_OK)
        except Organization.DoesNotExist:
            return Response({"error":"لا يوجد منظمة بهذا الرقم"} , status=status.HTTP_404_NOT_FOUND)




class UpdateOrganizationLogoView(BaseAPIView):
    def put(self, request, pk):
        organization = Organization.objects.get(id=pk)
        serializer = UpdateOrganizationLogoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            organization.logo = serializer.validated_data['logo']
            organization.save()
            return Response({
                'logo': serializer.get_logo(organization)
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvailableOffersView(BaseAPIView,OrganizationCheckMixin):
    def get(self,request,pk):
        organization = Organization.objects.select_related('organization_type').get(id=pk)
        offers = ServiceOffer.objects.prefetch_related('organizations').select_related('organization').filter(Q(organizations=organization.organization_type) & ~Q(organization__id=organization.id) & Q(expiresAt__gte=datetime.now()))
        paginator = CustomPagination()
        paginated_offers = paginator.paginate_queryset(offers, request)
        serializer = ServiceOfferSerializer(paginated_offers, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)


class DeleteOrganizationView(generics.DestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer



class UpdateOrganizationView(BaseAPIView,OrganizationCheckMixin):
    def put(self,request,id):
        organization = Organization.objects.get(id=id)
        serializer = UpdateOrganizationSerializer(organization , data=request.data , context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class SocialMediaUrlView(BaseAPIView):
    def get(self,request,pk):
        socials = SocialMediaUrl.objects.filter(organization__id=pk)
        serializer = SocialMediaUrlSerializer(socials , many=True , context={'request':request})
        return Response(serializer.data , status=status.HTTP_200_OK)


class UpdateSocialMediaUrlView(BaseAPIView , generics.UpdateAPIView):
    queryset = SocialMediaUrl.objects.all()
    serializer_class = SocialMediaUrlUpdateSerializer



class UpdateBulkSocialMediaUrlView(BaseAPIView):
    def post(self, request):
        urls_data = request.data
        updated_urls = []
        errors = []

        # Get all URLs in a single query
        url_ids = [data.get('id') for data in urls_data]
        existing_urls = SocialMediaUrl.objects.filter(id__in=url_ids)

        # Create mapping of id to URL object for easier lookup
        url_map = {url.id: url for url in existing_urls}

        # Validate all URLs exist
        if len(existing_urls) != len(urls_data):
            missing_ids = set(url_ids) - set(url.id for url in existing_urls)
            return Response(
                {"error": f"URLs with ids {list(missing_ids)} do not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update each URL individually
        for url_data in urls_data:
            url_id = url_data.get('id')
            url = url_map[url_id]
            
            serializer = SocialMediaUrlUpdateSerializer(url, data=url_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                updated_urls.append(serializer.data)
            else:
                errors.append({
                    'id': url_id,
                    'errors': serializer.errors
                })

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_urls, status=status.HTTP_200_OK)


class SocialMediaView(BaseAPIView , generics.ListAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer




class DeliveryUrlView(BaseAPIView):
    def get(self,request,pk):
        companies = DeliveryCompanyUrl.objects.filter(organization__id=pk)
        serializer = DeliveryCompanyUrlSerializer(companies , many=True , context={'request':request})
        return Response(serializer.data , status=status.HTTP_200_OK)



class UpdateDeliveryUrlView(generics.UpdateAPIView):
    serializer_class = DeliveryUrlUpdateSerializer
    queryset = DeliveryCompanyUrl.objects.all()




class DeliveryCompanyView(BaseAPIView , generics.ListAPIView):
    queryset = DeliveryCompany.objects.all()
    serializer_class = DeliveryCompanySerializer







class ReelsView(BaseAPIView):
    pagination_class = CustomPagination
    
    def get(self,request,id):
        reels = ReelsGallery.objects.filter(organization__id=id)
        serializer = ReelsGallerySerializer(reels , many=True, context={'request':self.request})
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class CreateReelsView(generics.CreateAPIView):
    serializer_class = ReelsGallerySerializer
    queryset = ReelsGallery.objects.all()


class DeleteReelsView(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            ReelsGallery.objects.get(id=id).delete()
            return Response({"message":"تم الحذف بنجاح"})
        except ReelsGallery.DoesNotExist:
            return Response({"error":"الفيديو غير موجود"})





class GalleryView(BaseAPIView):
    pagination_class = CustomPagination

    def get(self,request,id):
        gallery = ImageGallery.objects.filter(organization__id=id)
        serializer = ImagesGallerySerializer(gallery , many=True, context={'request':self.request})
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class CreateGalleryView(generics.CreateAPIView):
    serializer_class = ImagesGallerySerializer
    queryset = ImageGallery.objects.all()


class DeleteGalleryView(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            ImageGallery.objects.get(id=id).delete()
            return Response({"message":"تم الحذف بنجاح"})
        except ImageGallery.DoesNotExist:
            return Response({"error":"الصورة غير موجود"})




class CatalogView(BaseAPIView):

    def get(self,request,id):
        catalogs = Catalog.objects.filter(organization__id=id)
        serializer = CatalogSerializer(catalogs , many=True , context={'request':request})
        return Response(serializer.data , status=status.HTTP_200_OK)
    


class DeleteCatalogView(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            Catalog.objects.get(id=id).delete()
            return Response({"message":"تم الحذف بنجاح"})
        except Catalog.DoesNotExist:
            return Response({"error":"الكاتالوج غير موجود"})


class CreateCatalogView(BaseAPIView):
    def post(self,request):
        file = request.FILES.get('file' ,None)
        catalog_type = request.data.get('catalog_type', None)
        organization = request.data.get('organization', None)
        if not file or not catalog_type or not organization:
            return Response({"error":"الرجاء إدخال جميع البيانات"} , status=status.HTTP_400_BAD_REQUEST)
        
        try:
            Organization.objects.get(id=organization)
            serializer = CatalogSerializer(data=request.data , context={'request':request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except Organization.DoesNotExist:
            return Response({"error":"لا يوجد منظمة بهذا الرقم"} , status=status.HTTP_400_BAD_REQUEST)



class ClientOfferView(generics.ListAPIView):
    def get(self,request,id):
        offers = ClientOffer.objects.filter(organization__id=id)
        serializer = ClientOfferSerializer(offers , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

class CreateClientOffer(BaseAPIView):
    def post(self,request): 
        # content = request.data.get('content', None)
        # expiresAt = request.data.get('expiresAt', None)
        # organization = request.data.get('organization', None)
        # if not content or not expiresAt or not organization:
        #     return Response({"error":"الرجاء إدخال جميع البيانات"} , status=status.HTTP_400_BAD_REQUEST)
            
        # try:
        #     Organization.objects.get(id=organization)
        serializer = ClientOfferSerializer(data=request.data , context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        # except Organization.DoesNotExist:
        #     return Response({"error":"لا يوجد منظمة بهذا الرقم"} , status=status.HTTP_400_BAD_REQUEST)



class UpdateClientOffer(generics.UpdateAPIView):
    queryset = ClientOffer
    serializer_class = ClientOfferSerializer


class DeleteClientOffer(generics.DestroyAPIView):
    def delete(self,request,id):
        try:
            ClientOffer.objects.get(id=id).delete()
            return Response({"message":"تم الحذف بنجاح"})
        except ClientOffer.DoesNotExist:
            return Response({"error":"العرض غير موجود"})



class ServiceOfferView(generics.ListAPIView):
    def get(self,request,id):
        offers = ServiceOffer.objects.filter(organization__id=id)
        serializer = ServiceOfferSerializer(offers , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)


class CreateServiceOffer(BaseAPIView):
    def post(self,request): 
        serializer = ServiceOfferSerializer(data=request.data , context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)



class UpdateServiceOffer(generics.ListAPIView):
    queryset = ServiceOffer
    serializer_class = ServiceOfferSerializer

class DeleteServiceOffer(BaseAPIView):
    def delete(self,request,id):
        try:
            ServiceOffer.objects.get(id=id).delete()
            return Response({"message":"تم الحذف بنجاح"})
        except ServiceOffer.DoesNotExist:
            return Response({"error":"العرض غير موجود"})

