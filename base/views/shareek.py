from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from fcm_django.models import FCMDevice
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.db.models import Q, Min, Count, F, Subquery, OuterRef
from django.contrib.gis.measure import D
from utils.views import BaseAPIView
from django.shortcuts import redirect
from users.models import Shareek
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from utils.pagination import CustomPagination
from users.serializers import UserSerializer
# Create your views here.




class OrganizationTypes(BaseAPIView,generics.ListAPIView):
    queryset = OrganizationType.objects.all()
    serializer_class = OrganizationTypeSerializer


class OrganizationsListView(BaseAPIView,generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = BranchListSerializer
    queryset = Branch.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        distance_limit = self.request.query_params.get('distance', 1000)
        org_type_id = self.request.query_params.get('type', '')
        order = self.request.query_params.get('order', 'id')  # visits / distance / offers / id
        long = self.request.query_params.get('long', None)  
        lat = self.request.query_params.get('lat', None)  
        
        # Convert distance_limit to float
        try:
            distance_limit = float(distance_limit)
        except ValueError:
            distance_limit = 1000.0  # Default distance if invalid
        
        # Apply organization type filter if provided
        if org_type_id and org_type_id.isdigit():
            queryset = queryset.filter(organization__organization_type_id=org_type_id)
        
        # Process user location for distance calculations
        user_location = None
        if long and lat:
            try:
                long_float = float(long)
                lat_float = float(lat)
                user_location = Point(long_float, lat_float, srid=4326)
            except (ValueError, TypeError):
                pass
        
        # Generate a Google Maps URL for each organization's branches (if user location is provided)
        if user_location:
            # Annotate organizations with the minimum distance to any of their branches
            
            # Subquery to find the closest branch for each organization
            closest_branch = Branch.objects.filter(
                organization=OuterRef('organization')
            ).annotate(
                distance=Distance('location', user_location)
            ).order_by('distance').values('distance')[:1]
            
            # Annotate organizations with the distance to their closest branch
            queryset = queryset.annotate(
                min_distance=Subquery(closest_branch)
            )
            
            # Filter by distance if a user location is provided
            queryset = queryset.filter(min_distance__lte=distance_limit)
        
        # Count client offers for each organization
        queryset = queryset.annotate(
            client_offers_count=Count('organization__clientoffer', distinct=True)
        )
        
        # Order the results based on the specified order parameter
        if order == 'visits':
            queryset = queryset.order_by('-organization__visits')
        elif order == 'offers':
            queryset = queryset.order_by('-client_offers_count')
        elif order == 'distance' and user_location:
            queryset = queryset.order_by('min_distance')
        else:
            # Default ordering by id
            queryset = queryset.order_by('-id')
        
        return queryset


class OrganizationInfoView(BaseAPIView):
    def get(self, request, id):
        try:
            organization = Organization.objects.prefetch_related('branch_set').get(id=id)
            serializer = OrganizationSerializer(organization, context={'request': request})
            branches_serializer = BranchSerializer(organization.branch_set.all(), many=True)
            client_offers = ListClientOfferSerializer(organization.clientoffer_set.all(), many=True , context={'request':request})
            return Response({
                **serializer.data,
                'branches': branches_serializer.data,
                'client_offers': client_offers.data
            }, status=status.HTTP_200_OK)
            
        except Organization.DoesNotExist:
            raise ErrorResult({'error': 'لا يوجد منظمة بهذا الرقم'}, status=404)


class GetOrganizationView(BaseAPIView):
    def get(self,request,pk):
        organization = Organization.objects.get(id=pk)
        service_offers = ServiceOffer.objects.filter(organization__id=pk)
        branches = Branch.objects.filter(organization__id=pk)
        gallery = ImageGallery.objects.filter(organization__id=pk)
        socials = SocialMediaUrl.objects.select_related('social_media').filter(organization__id=pk)
        delivery = DeliveryCompanyUrl.objects.select_related('delivery_company').filter(organization__id=pk)
        catalogs = Catalog.objects.filter(organization__id=pk)

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
            'socials': SocialUrlSerializer(socials, many=True , context={'request':request}).data,
            'delivery': DeliveryUrlSerializer(delivery, many=True , context={'request':request}).data,
            'catalogs': CatalogUrlsSerializer(catalogs, many=True , context={'request':request}).data,
            'service_offers': ServiceOfferSerializer(service_offers, many=True , context={'request':request}).data,
            'branches': BranchSerializer(branches , many=True).data
        }

        return Response(data , status=status.HTTP_200_OK)



class UpdateOrganizationLogoView(generics.UpdateAPIView):
    queryset = Organization.objects.all()
    serializer_class = UpdateOrganizationLogoSerializer


class AvailableOffersView(BaseAPIView):
    def get(self,request,pk):
        try:
            organization = Organization.objects.select_related('organization_type').get(id=pk)
            offers = ServiceOffer.objects.prefetch_related('organizations').select_related('organization').filter(Q(organizations=organization.organization_type) & ~Q(organization__id=organization.id))
            paginator = CustomPagination()
            paginated_offers = paginator.paginate_queryset(offers, request)
            serializer = ServiceOfferSerializer(paginated_offers, many=True, context={'request':request})
            return paginator.get_paginated_response(serializer.data)
        except Organization.DoesNotExist:
            return Response({"error":"لا يوجد منظمة بهذا الرقم"} , status=status.HTTP_400_BAD_REQUEST)


class DeleteOrganizationView(generics.DestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer



class UpdateOrganizationView(BaseAPIView):
    def put(self,request,id):
        try:
            organization = Organization.objects.get(id=id)
            serializer = UpdateOrganizationSerializer(organization , data=request.data , context={'request':request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_200_OK)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except Organization.DoesNotExist:
            return Response({"error":"لا يوجد منظمة بهذا الرقم"} , status=status.HTTP_400_BAD_REQUEST)

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
        # template = request.data.get('template', None)
        # if not content or not expiresAt or not organization or not template:
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




class TemplatesView(generics.ListAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer



