from django.db import models
from django.core.validators import MinValueValidator
from utils.helper import generateShortUrl , generate_img_thumbnail
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models as gis_models
from utils.managers import DeliveryCompanyUrlManager , SocialMediaUrlManager
from utils.types import CATALOG_TYPES



class OrganizationType(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الانشاء')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']


class Organization(models.Model):
    commercial_register_id = models.IntegerField(null=True , blank=True , validators=[MinValueValidator(1000)], verbose_name='رقم السجل التجاري')
    logo = models.ImageField(upload_to='media/organizations/logos/', default='media/images/default.jpg', verbose_name='الشعار')
    logo_thumbnail = models.ImageField(upload_to='media/images/thumbnails/', verbose_name='الصورة المصغرة', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='الاسم')
    description = models.CharField(max_length=255 , null=True, blank=True, verbose_name='المعلومات التعريفية')
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True, verbose_name='نوع المنظمة')
    website = models.CharField(max_length=300 , null=True, blank=True, verbose_name='الموقع الإلكتروني')
    website_short_url = models.SlugField(max_length=50 , default=generateShortUrl, verbose_name='اختصار الموقع الإلكتروني')
    card_url = models.SlugField(max_length=50 , default=generateShortUrl, verbose_name='البطاقة التعريفية')
    # deep_link = models.CharField(max_length=300 , null=True, blank=True, verbose_name='رابط الملف الشخصية')
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الانشاء')

    def clean(self):
        if self.logo and self.logo.size > 2 * 1024 * 1024:  # 2MB in bytes
            raise ValidationError('حجم الشعار يجب أن لا يتجاوز 2 ميجابايت')

    def __str__(self) -> str:
        return self.name

    def create_social_media(self):
        social_medias = SocialMedia.objects.all()
        for social in social_medias:
            social_media , created = SocialMediaUrl.objects.get_or_create(organization=self,social_media=social,)

    def create_delivery_company(self):
        delivery_companies = DeliveryCompany.objects.all()
        for delivery in delivery_companies:
            delivery_company , created = DeliveryCompanyUrl.objects.get_or_create( organization=self,delivery_company=delivery,)
    
    def get_absolute_card_url(self):
        return f"/card/{self.card_url}/"

    def get_absolute_website_url(self):
        return f"/website/{self.website_short_url}/"

    def save(self, *args, **kwargs):
        # First save to ensure the image is saved to disk
        super().save(*args, **kwargs)
        
        # Using the updated generate_img_thumbnail function
        try:
            print(f"Image path: {self.logo.path}")
            content_file, thumb_filename = generate_img_thumbnail(self.logo.path)
            self.logo_thumbnail.save(thumb_filename, content_file, save=False)
            print(self.logo_thumbnail.size)
            print(self.logo.size)
            # Save again to update the thumbnail field
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error saving thumbnail: {str(e)}")

    class Meta:
        ordering = ['-id']


class Branch(gis_models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name='المنظمة')
    name = models.CharField(max_length=255 , verbose_name='الاسم') # default method for settings name ex: org-branch2
    location = gis_models.PointField(srid=4326 , verbose_name='الموقع')
    description = models.CharField(max_length=255,null=True ,blank=True , verbose_name='الوصف')
    short_url = models.SlugField(max_length=50 , default=generateShortUrl , verbose_name='الرابط المختصر')
    visits = models.IntegerField(default=0 , verbose_name= "الزيارات")

    def get_absolute_url(self):
        return f"/branch/{self.short_url}/"

    def __str__(self) -> str:
        return self.name


class ImageGallery(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='المنظمة')
    image = models.ImageField(upload_to='media/images/image_galleries/', verbose_name='الصورة')
    thumbnail = models.ImageField(upload_to='media/images/thumbnails/', verbose_name='الصورة المصغرة', null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        ordering = ['-id']  

    def save(self, *args, **kwargs):
        # First save to ensure the image is saved to disk
        super().save(*args, **kwargs)
        
        # Using the updated generate_img_thumbnail function
        try:
            print(f"Image path: {self.image.path}")
            content_file, thumb_filename = generate_img_thumbnail(self.image.path)
            self.thumbnail.save(thumb_filename, content_file, save=False)
            print(self.thumbnail.size)
            print(self.image.size)
            # Save again to update the thumbnail field
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error saving thumbnail: {str(e)}")


class ReelsGallery(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='المنظمة')
    video = models.FileField(upload_to='media/images/reels_galleries/', verbose_name='الفيديو')
    video_thumbnail = models.ImageField(upload_to='media/images/thumbnails/', verbose_name='الصورة المصغرة',null=True , blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        ordering = ['-id']  

    def clean(self):
        if self.video:
            # Check file size
            if self.video.size > 15 * 1024 * 1024:  # 15MB in bytes
                raise ValidationError('حجم الفيديو يجب أن لا يتجاوز 15 ميجابايت')
            
            # Check if file is video format
            import mimetypes
            file_type = mimetypes.guess_type(self.video.name)[0]
            if not file_type or not file_type.startswith('video/'):
                raise ValidationError('يجب أن يكون الملف بتنسيق فيديو')
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)   
    #     self.video_thumbnail = generate_video_thumbnail(self.video.path)



class Catalog(models.Model):
    catalog_type = models.CharField(max_length=255 , choices=CATALOG_TYPES.choices , verbose_name='النوع')
    file = models.FileField(upload_to='media/images/catalogs/',verbose_name='الملف')
    short_url = models.SlugField(max_length=300 , default=generateShortUrl , verbose_name='الرابط المختصر')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name="المنظمة", related_name='catalogs')
    visits = models.IntegerField(default=0 , verbose_name= "الزيارات")

    def clean(self):
        if self.file and self.file.size > 10 * 1024 * 1024:  # 10MB in bytes
            raise ValidationError('حجم الملف يجب أن لا يتجاوز 10 ميجابايت')

    def save(self, *args, **kwargs) -> None:
        existing_catalog = Catalog.objects.filter(organization=self.organization,catalog_type=self.catalog_type)
        if existing_catalog:
            existing_catalog.delete()
        if not self.file:
            self.file = f"{self.organization.name}-{self.catalog_type}.pdf"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/catalog/{self.short_url}/"

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.catalog_type}"

    class Meta:
        ordering = ['-id']  
        

class SocialMedia(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    icon = models.ImageField(upload_to='media/images/social_media/', default='media/images/default.jpg',verbose_name='الصورة')
    icon_thumbnail = models.ImageField(upload_to='media/images/thumbnails/', verbose_name='الصورة المصغرة', null=True, blank=True)

    def clean(self):
        if self.icon and self.icon.size > 1 * 1024 * 1024:  # 1MB in bytes
            raise ValidationError('حجم الأيقونة يجب أن لا يتجاوز 1 ميجابايت')

    def save(self, *args, **kwargs):
        # First save to ensure the image is saved to disk
        super().save(*args, **kwargs)
        
        # Using the updated generate_img_thumbnail function
        try:
            print(f"Image path: {self.icon.path}")
            content_file, thumb_filename = generate_img_thumbnail(self.icon.path)
            self.icon_thumbnail.save(thumb_filename, content_file, save=False)
            # Save again to update the thumbnail field
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error saving thumbnail: {str(e)}")

    def create_social_urls(self):
        organizations = Organization.objects.all()
        for org in organizations:
            SocialMediaUrl.objects.get_or_create(
                organization=org,
                social_media=self,
                defaults={'active': False}
            )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']



class SocialMediaUrl(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name= "المنظمة", related_name='socials')
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE , verbose_name= "موقع التواصل الاجتماعي")
    url = models.URLField(max_length=300, null=True , blank=True , verbose_name= "الرابط")
    short_url = models.SlugField(max_length=50 , default=generateShortUrl , verbose_name= "الرابط المختصر")
    active = models.BooleanField(default=False , verbose_name= "مفعل")
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name= "تاريخ الإنشاء")
    deleted = models.BooleanField(default=False , verbose_name= "محذوف")
    visits = models.IntegerField(default=0 , verbose_name= "الزيارات")

    objects = SocialMediaUrlManager()

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.social_media.name}"

    def get_absolute_url(self):
        return f"/social/{self.short_url}/"

    def save(self, *args, **kwargs):
        if self.url:
            self.deleted = False
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']


class DeliveryCompany(models.Model):
    name = models.CharField(max_length=255,verbose_name='الاسم')
    icon = models.ImageField(upload_to='media/images/delivery_company/', default='media/images/default.jpg',verbose_name='الصورة')
    icon_thumbnail = models.ImageField(upload_to='media/images/thumbnails/', verbose_name='الصورة المصغرة', null=True, blank=True)

    def clean(self):
        if self.icon and self.icon.size > 1 * 1024 * 1024:  # 1MB in bytes
            raise ValidationError('حجم الأيقونة يجب أن لا يتجاوز 1 ميجابايت')

    def save(self, *args, **kwargs):
        # First save to ensure the image is saved to disk
        super().save(*args, **kwargs)
        
        # Using the updated generate_img_thumbnail function
        try:
            print(f"Image path: {self.icon.path}")
            content_file, thumb_filename = generate_img_thumbnail(self.icon.path)
            self.icon_thumbnail.save(thumb_filename, content_file, save=False)
            # Save again to update the thumbnail field
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error saving thumbnail: {str(e)}")

    def create_delivery_urls(self):
        organizations = Organization.objects.all()
        for org in organizations:
            DeliveryCompanyUrl.objects.get_or_create(
                organization=org,
                delivery_company=self,
                defaults={'active': False}
            )

    def __str__(self) -> str:
        return self.name
    
    class Meta: 
        ordering = ['-id']


class DeliveryCompanyUrl(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name= "المنظمة" , related_name='delivery')
    delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.CASCADE , verbose_name= "شركة التوصيل")
    url = models.URLField(max_length=300 , null=True , blank=True , verbose_name= "الرابط")
    short_url = models.SlugField(max_length=50 , default=generateShortUrl , verbose_name= "الرابط المختصر")
    active = models.BooleanField(default=False , verbose_name= "مفعل")
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name= "تاريخ الإنشاء")
    deleted = models.BooleanField(default=False , verbose_name= "محذوف")
    visits = models.IntegerField(default=0 , verbose_name= "الزيارات")
    
    objects = DeliveryCompanyUrlManager()

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.delivery_company.name}"

    def get_absolute_url(self):
        return f"/delivery/{self.short_url}/"

    def save(self, *args, **kwargs):
        if self.url:
            self.deleted = False
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']


class Template(models.Model):
    name = models.CharField(max_length=255, verbose_name='الاسم')
    template = models.ImageField(upload_to='media/images/templates/', verbose_name='القالب')
    template_thumbnail = models.ImageField(upload_to='media/images/thumbnails/', verbose_name='الصورة المصغرة', null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الانشاء')   

    def save(self, *args, **kwargs):
        # First save to ensure the image is saved to disk
        super().save(*args, **kwargs)
        
        # Using the updated generate_img_thumbnail function
        try:
            print(f"Image path: {self.template.path}")
            content_file, thumb_filename = generate_img_thumbnail(self.template.path)
            self.template_thumbnail.save(thumb_filename, content_file, save=False)
            print(self.template_thumbnail.size)
            print(self.template.size)
            # Save again to update the thumbnail field
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error saving thumbnail: {str(e)}")

    def __str__(self) -> str:
        return self.name
    
    def clean(self):
        if self.template and self.template.size > 1 * 1024 * 1024:  # 1MB in bytes
            raise ValidationError('حجم القالب يجب أن لا يتجاوز 1 ميجابايت')

    class Meta:
        ordering = ['-id']



class ServiceOffer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name='المنظمة')
    content = models.CharField(max_length=500 , verbose_name='المحتوى')
    expiresAt = models.DateField(verbose_name='تاريخ الانتهاء')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الانشاء')
    organizations = models.ManyToManyField(OrganizationType , verbose_name='المنظمات')

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.id}"

    class Meta:
        ordering = ['-id']



class ClientOffer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name='المنظمة')
    cover = models.ImageField(upload_to='media/images/client_offers/', verbose_name='الغلاف',default='media/images/default.jpg')
    content = models.CharField(max_length=500 , verbose_name='المحتوى')
    expiresAt = models.DateField(verbose_name='تاريخ الانتهاء')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الانشاء')
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True , verbose_name='القالب')

    def clean(self):
        if self.cover and self.cover.size > 1 * 1024 * 1024:  # 1MB in bytes
            raise ValidationError('حجم الغلاف يجب أن لا يتجاوز 1 ميجابايت')

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.id}"
    
    class Meta:
        ordering = ['-id']





class ContactUs(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    link = models.CharField(max_length=255 , verbose_name='الرابط')
    icon = models.ImageField(upload_to='media/images/about_us/', default='media/images/default.jpg', verbose_name='الشعار')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']


class AboutUs(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    link = models.CharField(max_length=255 , verbose_name='الرابط')
    icon = models.ImageField(upload_to='media/images/about_us/', default='media/images/default.jpg', verbose_name='الشعار')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']



class TermsPrivacy(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']



class CommonQuestion(models.Model):
    question = models.CharField(max_length=255 , verbose_name='السؤال')
    answer = models.CharField(max_length=255 , verbose_name='الجواب')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الإنشاء')

    def __str__(self) -> str:
        return self.question
    
    class Meta:
        ordering = ['-id']


class Report(models.Model):
    client = models.IntegerField(verbose_name='العميل')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name='المنظمة')
    content = models.CharField(max_length=255 , verbose_name='المحتوى')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الإنشاء')

    def __str__(self) -> str:
        return f"{self.client} - {self.organization.name}"


class Subscription(models.Model):
    name = models.CharField(max_length=100 , verbose_name="اسم الاشتراك")
    price = models.FloatField(verbose_name="السعر")
    days = models.IntegerField(validators=[MinValueValidator(1)] , verbose_name="الفترة (الأيام)")

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"

    class Meta:
        ordering = ['-id']