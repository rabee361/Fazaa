from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers
from users.models import User
from django.contrib.gis.geos import Point



class OrganizationListSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id','name','description','logo']


class BranchSerializer(ModelSerializer):
    location = serializers.SerializerMethodField()
    class Meta:
        model = Branch
        fields = ['id','name','location']

    def get_location(self,obj):
        return {"longitude":obj.location.x, "latitude":obj.location.y}






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

    def validate_icon(self, icon):
        if icon and icon.size > 2 * 1024 * 1024:  # 2MB in bytes
            raise serializers.ValidationError('حجم الأيقونة يجب أن لا يتجاوز 2 ميجابايت')
        


class SocialMediaUrlSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    social_media = SocialMediaSerializer()
    icon = serializers.ImageField(source='social_media.icon', read_only=True)
    name = serializers.CharField(source='social_media.name', read_only=True)
    class Meta:
        model = SocialMediaUrl 
        fields = ['id','organization','short_url','social_media','active','icon','name']


    def get_icon(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.social_media.icon.url)

    def get_short_url(self,obj):
        request = self.context.get('request')

        if obj.url:
            return f"http://145.223.80.125:8080/social/{obj.short_url}/"
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
    
    def validate_icon(self, icon):
        if icon and icon.size > 2 * 1024 * 1024:  # 2MB in bytes
            raise serializers.ValidationError('حجم الأيقونة يجب أن لا يتجاوز 2 ميجابايت')
        

class DeliveryCompanyUrlSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    icon = serializers.ImageField(source='delivery_company.icon', read_only=True)
    name = serializers.CharField(source='delivery_company.name', read_only=True)
    class Meta:
        model = DeliveryCompanyUrl
        fields = ['id','organization','short_url','delivery_company','active','icon','name']
    
    def get_icon(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.delivery_company.icon.url)


    def get_short_url(self,obj):
        request = self.context.get('request')

        if obj.url:
            return f"http://145.223.80.125:8080/delivery/{obj.short_url}/"
        return None









class DeliveryUrlUpdateSerializer(ModelSerializer):
    class Meta:
        model = DeliveryCompanyUrl
        fields = ['id', 'organization', 'delivery_company', 'url', 'short_url', 'active', 'createdAt']
        read_only_fields = ['id', 'organization', 'delivery_company', 'short_url', 'createdAt']



    
class CatalogSerializer(ModelSerializer):
    short_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Catalog
        fields = ['id','short_url','catalog_type','organization']

    def get_short_url(self,obj):
        request = self.context.get('request')
        if obj.file:
            return f"http://145.223.80.125:8080/catalog/{obj.short_url}/"
        return None



class ReelsGallerySerializer(ModelSerializer):
    video = serializers.SerializerMethodField()
    class Meta:
        model = ReelsGallery
        fields = '__all__'

    def get_video(self, obj):
        request = self.context.get('request')
        if obj.video:
            return request.build_absolute_uri(obj.video.url)
        return None

    def validate_reel(self, reel):
        if reel and reel.size > 25 * 1024 * 1024:  # 25MB in bytes
            raise serializers.ValidationError('حجم الفيديو يجب أن لا يتجاوز 25 ميجابايت')
        
        # Check if organization has reached daily limit of 20 reels
        today = timezone.now().date()
        today_reels_count = ReelsGallery.objects.filter(
            organization=self.initial_data['organization'],
            createdAt__date=today
        ).values('id').count()

        if today_reels_count >= 10:
            raise serializers.ValidationError('لا يمكن إضافة أكثر من 10 فيديو في اليوم')
            
        return reel



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
        if image and image.size > 2 * 1024 * 1024:  # 2MB in bytes

            raise serializers.ValidationError('حجم الصورة يجب أن لا يتجاوز 2 ميجابايت')
        
        # Check if organization has reached daily limit of 20 images
        today = timezone.now().date()
        today_images_count = ImageGallery.objects.filter(
            organization=self.initial_data['organization'],
            createdAt__date=today
        ).values('id').count()

        if today_images_count >= 20:
            raise serializers.ValidationError('لا يمكن إضافة أكثر من 20 صورة في اليوم')
            
        return image



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

    def validate_template(self, template):
        if template and template.size > 5 * 1024 * 1024:  # 5MB in bytes
            raise serializers.ValidationError('حجم الصورة يجب أن لا يتجاوز 5 ميجابايت')
        
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



class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
    
    def validate_client(self,value):
        if not User.objects.filter(id=value, user_type='CLIENT').exists():
            raise serializers.ValidationError('لا يوجد عميل بهذا الرقم')
        
        today = timezone.now().date()
        reports = Report.objects.filter(
            client=value,
            createdAt__date=today
        )
        if reports.count() >= 5:
            raise serializers.ValidationError('لا يمكنك إضافة أكثر من 5 تقارير في اليوم الواحد')

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


class UpdateOrganizationSerializer(ModelSerializer):
    branches = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ['logo','description','website','branches']

    def get_branches(self,obj):
        return BranchSerializer(obj.branches, many=True).data

    def validate_branches(self,value):
        if len(value) == 0:
            raise serializers.ValidationError('يجب إضافة على الأقل فرع واحد')
        return value
    
    def update(self, instance, validated_data):
        branches = validated_data.get('branches')
        instance = super().update(instance, validated_data)
        if branches:
            for branch in branches:
                if isinstance(branch, dict):
                    point = Point(branch['longitude'], branch['latitude'])
                    Branch.objects.get_or_create(organization=instance, location=point)
            else:
                raise serializers.ValidationError('يجب إضافة فرع بشكل صالح')

        return instance

