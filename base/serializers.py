from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers
from users.models import User
from django.contrib.gis.geos import Point
from django.db.models import Sum
from utils.validators import validate_catalog_size, validate_video_extension, validate_catalog_extension, validate_video_size, validate_image_size, validate_image_extension
from utils.exception_handlers import ErrorResult
from django.utils import timezone
import os

class OrganizationListSerializer(ModelSerializer):
    visits = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ['id','name','description','logo','visits']

    def get_visits(self,obj):
        visits = Branch.objects.filter(organization=obj).aggregate(total_visits=Sum('visits'))['total_visits'] or 0
        return visits


class BranchSerializer(ModelSerializer):
    location = serializers.SerializerMethodField()
    class Meta:
        model = Branch
        fields = ['id','name','location']

    def get_location(self,obj):
        return {"longitude":obj.location.x, "latitude":obj.location.y}



class BranchListSerializer(ModelSerializer):
    location = serializers.SerializerMethodField()
    organization = OrganizationListSerializer()
    distance = serializers.SerializerMethodField()
    offers = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = ['id','name','location','distance','organization','offers']

    def get_location(self,obj):
        return {"longitude":obj.location.x, "latitude":obj.location.y}

    def get_distance(self,obj):
        distance_limit = self.context.get('distance_limit')
        if distance_limit:
            distance_limit = float(distance_limit) * 1000
            return obj.location.distance(Point(float(self.context['long']), float(self.context['lat']))) * 100
        return 100

    def get_offers(self,obj):
        return obj.organization.clientoffer_set.all().count()





class OrganizationTypeSerializer(ModelSerializer):

    class Meta:
        model = OrganizationType
        fields = ['id','name']




class SocialMediaSerializer(ModelSerializer):
    icon = serializers.SerializerMethodField()
    icon_thumbnail = serializers.SerializerMethodField()
    class Meta:
        model = SocialMedia
        fields = ['icon','name','icon_thumbnail']

    def get_icon(self,obj):
        request = self.context.get('request')
        if obj.icon:
            return request.build_absolute_uri(obj.icon.url)
        return None
    
    def get_icon_thumbnail(self,obj):
        request = self.context.get('request')
        if obj.icon_thumbnail:
            return request.build_absolute_uri(obj.icon_thumbnail.url)
        return None
    
    def validate_icon(self, icon):
        validate_image_size(icon)
        validate_image_extension(icon)
        

class SocialMediaUrlSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    social_media = SocialMediaSerializer()  #TODO remove the icon and icon_thumbnail from the body response 
    icon = serializers.SerializerMethodField()
    icon_thumbnail = serializers.SerializerMethodField() 
    name = serializers.CharField(source='social_media.name', read_only=True)
    class Meta:
        model = SocialMediaUrl 
        fields = ['id','organization','short_url','social_media','active','icon','name','icon_thumbnail']

    def get_icon(self,obj):
        request = self.context.get('request')
        if obj.social_media and obj.social_media.icon:
            return request.build_absolute_uri(obj.social_media.icon.url)
        return None
    
    def get_icon_thumbnail(self,obj):
        request = self.context.get('request')
        if obj.social_media and obj.social_media.icon_thumbnail:
            return request.build_absolute_uri(obj.social_media.icon_thumbnail.url)
        return None

    def get_short_url(self,obj):
        request = self.context.get('request')

        if obj.url:
            return f"http://168.231.127.170/social/{obj.short_url}/"
        return None




class SocialMediaUrlUpdateSerializer(ModelSerializer):
    class Meta:
        model = SocialMediaUrl
        fields = ['id', 'organization', 'social_media', 'url', 'short_url', 'active', 'createdAt']
        read_only_fields = ['id', 'organization', 'social_media', 'short_url', 'createdAt']




class DeliveryCompanySerializer(ModelSerializer):
    class Meta:
        model = DeliveryCompany
        fields = '__all__'

    def get_icon(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.icon.url)
    
    def get_icon_thumbnail(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.icon_thumbnail.url)

    def validate_icon(self, icon):
        validate_image_size(icon)
        validate_image_extension(icon)
        

class DeliveryCompanyUrlSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    icon_thumbnail = serializers.SerializerMethodField()
    name = serializers.CharField(source='delivery_company.name', read_only=True)
    class Meta:
        model = DeliveryCompanyUrl
        fields = ['id','organization','short_url','delivery_company','active','icon','name','icon_thumbnail']
    
    def get_icon(self,obj):
        request = self.context.get('request')
        if obj.delivery_company and obj.delivery_company.icon:
            return request.build_absolute_uri(obj.delivery_company.icon.url)
        return None
    
    def get_icon_thumbnail(self,obj):
        request = self.context.get('request')
        if obj.delivery_company and obj.delivery_company.icon_thumbnail:
            return request.build_absolute_uri(obj.delivery_company.icon_thumbnail.url)
        return None

    def get_short_url(self,obj):
        request = self.context.get('request')

        if obj.url:
            return f"http://168.231.127.170/delivery/{obj.short_url}/"
        return None




class DeliveryUrlUpdateSerializer(ModelSerializer):
    class Meta:
        model = DeliveryCompanyUrl
        fields = ['id', 'organization', 'delivery_company', 'url', 'short_url', 'active', 'createdAt']
        read_only_fields = ['id', 'organization', 'delivery_company', 'short_url', 'createdAt']


    
class CatalogSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    class Meta:
        model = Catalog
        fields = ['id','short_url','catalog_type','organization','file','file_name']

    def get_short_url(self,obj):
        request = self.context.get('request')
        if obj.file:
            return f"http://168.231.127.170/catalog/{obj.short_url}/"
        return None

    def get_file_name(self, obj):
        return os.path.basename(obj.file.name)
    
    def validate(self, attrs):
        validate_catalog_size(attrs['file'])
        validate_catalog_extension(attrs['file'])
        return attrs



class ReelsGallerySerializer(ModelSerializer):
    class Meta:
        model = ReelsGallery
        fields = '__all__'

    def get_video(self, obj):
        request = self.context.get('request')
        if obj.video:
            return request.build_absolute_uri(obj.video.url)
        return None

    def validate_video(self, video):
        validate_video_extension(video)
        validate_video_size(video)
        # Check if organization has reached daily limit of 20 reels
        today = timezone.now().date()
        today_reels_count = ReelsGallery.objects.filter(
            organization=self.initial_data['organization'],
            createdAt__date=today
        ).values('id').count()

        if today_reels_count >= 10:
            raise ErrorResult({'error':'لا يمكن إضافة أكثر من 10 فيديو في اليوم'})
            
        return video



class ImagesGallerySerializer(ModelSerializer):

    class Meta:
        model = ImageGallery
        fields = '__all__'

    def get_image(self,obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    def validate_image(self, image):
        validate_image_size(image)
        validate_image_extension(image)
        # Check if organization has reached daily limit of 20 images
        today = timezone.now().date()
        today_images_count = ImageGallery.objects.filter(
            organization=self.initial_data['organization'],
            createdAt__date=today
        ).values('id').count()

        if today_images_count >= 20:
            raise ErrorResult({'error':'لا يمكن إضافة أكثر من 20 صورة في اليوم'})
            
        return image



# class NotificationSerializer(ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = '__all__'



class ServiceOfferSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    organization_logo = serializers.SerializerMethodField()
    class Meta:
        model = ServiceOffer
        fields = '__all__'

    def get_organization_logo(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.organization.logo.url)




class ListClientOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOffer
        fields = ['id','content','expiresAt','createdAt','cover','template','short_url']

    def get_cover(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.cover.url)



class ClientOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOffer
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'

    def validate_template(self, template):
        validate_image_size(template)
        validate_image_extension(template)
        return template


class TermsPrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsPrivacy
        fields = '__all__'



class CommonQuestionsSerializer(ModelSerializer):
    class Meta:
        model = CommonQuestion
        fields = '__all__'


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

    def get_image(self,obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)





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
    org_short_url = serializers.SerializerMethodField()
    card_url = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id','name','description','organization_type','logo','website','website_short_url','card_url','org_short_url']
    
    def get_website_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_website_url())
    
    def get_org_short_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_org_url())

    def get_logo(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.logo.url)

    def get_card_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_card_url())


class UpdateOrganizationLogoSerializer(ModelSerializer):
    logo = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ['logo']

    def validate_logo(self, logo):
        validate_image_size(logo)
        validate_image_extension(logo)
        return logo
    
    def get_logo(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.logo.url)


class UpdateOrganizationSerializer(ModelSerializer):
    branches = serializers.ListField(child=serializers.DictField(), required=False)
    
    class Meta:
        model = Organization
        fields = ['description','website','branches']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['branches'] = BranchSerializer(Branch.objects.filter(organization=instance), many=True).data
        return data

    def validate_branches(self,value):
        if len(value) == 0:
            raise ErrorResult({'error':'عليك إضافة فرع واحد على الأقل'})
        return value
    
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description) 
        instance.website = validated_data.get('website', instance.website)
        branches = validated_data.get('branches', None)
        if branches:
            for i, branch_data in enumerate(branches, 1):
                if isinstance(branch_data, dict):
                    point = Point(branch_data['longitude'], branch_data['latitude'])
                    branch, created = Branch.objects.get_or_create(organization=instance, location=point)
                    if created:
                        branch.name = f"{instance.name} - فرع {i}"
                        branch.save()
        instance.save()
        return instance




class ReportSerializer(ModelSerializer):
    # organization = OrganizationListSerializer(many=False)
    class Meta:
        model = Report
        fields = '__all__'
    
    def validate_client(self,value):
        if not User.objects.filter(id=value).exists():
            raise ErrorResult({'error':'لا يوجد مستخدم بهذا الرقم'})
        
        today = timezone.now().date()
        reports = Report.objects.filter(
            client=value,
            createdAt__date=today
        )
        if reports.count() >= 5:
            raise ErrorResult({'error':'لا يمكنك إضافة أكثر من 5 تقارير في اليوم الواحد'})

        return value
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization'] = OrganizationListSerializer(instance.organization).data
        return data


class OrganizationReportsSerializer(ModelSerializer):
    visits = serializers.SerializerMethodField()    
    logo = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ['id','name','logo','description','visits']

    def get_logo(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.logo.url)

    def get_visits(self,obj):
        visits = Branch.objects.filter(organization=obj).aggregate(total_visits=Sum('visits'))['total_visits'] or 0
        return visits



