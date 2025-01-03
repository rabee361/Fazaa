from tabnanny import verbose
from typing import Iterable
from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator
from utils.helper import generateShortUrl

# Create your models here.


 

class OrganizationType(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الانشاء')

    def __str__(self) -> str:
        return self.name


class Organization(models.Model):
    commercial_register_id = models.IntegerField(null=True , blank=True , verbose_name='رقم السجل التجاري')
    logo = models.ImageField(upload_to='media/organizations/logos/', default='media/images/organizations/logos/default.png', verbose_name='الشعار')
    name = models.CharField(max_length=255, verbose_name='الاسم')
    description = models.CharField(max_length=255 , null=True, blank=True, verbose_name='المعلومات التعريفية')
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True, verbose_name='نوع المنظمة')
    website = models.CharField(max_length=300 , null=True, blank=True, verbose_name='الموقع الإلكتروني')
    website_short_url = models.SlugField(max_length=50 , default=generateShortUrl, verbose_name='الرابط المختصر')
    card_url = models.SlugField(max_length=50 , default=generateShortUrl, verbose_name='الرابط المختصر')
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الانشاء')

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


class Branch(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name='المنظمة')
    name = models.CharField(max_length=255 , verbose_name='الاسم') # default method for settings name ex: org-branch2
    long = models.FloatField(verbose_name='الطول')
    lat = models.FloatField(verbose_name='العرض')
    description = models.CharField(max_length=255,null=True ,blank=True , verbose_name='الوصف')

    def __str__(self) -> str:
        return self.name
    


class ImageGallery(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/images/image_galleries/')
    createdAt = models.DateTimeField(auto_now_add=True)



class ReelsGallery(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    video = models.FileField(upload_to='media/images/reels_galleries/')
    createdAt = models.DateTimeField(auto_now_add=True)
 


class Catalog(models.Model):
    class CATALOG_TYPES(models.TextChoices):
        MENU='MENU'
        DISCOUNT='DISCOUNT'
        OFFERS='OFFERS'

    catalog_type = models.CharField(max_length=255 , choices=CATALOG_TYPES.choices , verbose_name='النوع')
    file = models.FileField(upload_to='media/images/catalogs/',verbose_name='الملف')
    short_url = models.SlugField(max_length=300 , default=generateShortUrl , verbose_name='الرابط المختصر')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name="المنظمة")
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الإنشاء")

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

    


class SocialMedia(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    icon = models.ImageField(upload_to='media/images/social_media/', default='media/images/social_media/default_media.png',verbose_name='الصورة')

    def save(self, *args, **kwargs):        
        if not self.pk:
            super().save(*args, **kwargs)
            organizations = Organization.objects.all()
            for org in organizations:
                social , created = SocialMediaUrl.objects.get_or_create(
                    organization=org,
                    social_media=self,
                    active=False
                )

    def __str__(self) -> str:
        return self.name



class   SocialMediaUrl(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name= "المنظمة")
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE , verbose_name= "موقع التواصل الاجتماعي")
    url = models.URLField(max_length=300, null=True , blank=True , verbose_name= "الرابط")
    short_url = models.SlugField(max_length=50 , default=generateShortUrl , verbose_name= "الرابط المختصر")
    active = models.BooleanField(default=False , verbose_name= "مفعل")
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name= "تاريخ الإنشاء")

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.social_media.name}"

    def get_absolute_url(self):
        return f"/social/{self.short_url}/"


class DeliveryCompany(models.Model):
    name = models.CharField(max_length=255,verbose_name='الاسم')
    icon = models.ImageField(upload_to='media/images/delivery_company/', default='media/images/delivery_company/default_company.png',verbose_name='الصورة')

    def save(self, *args, **kwargs):        
        if not self.pk:
            super().save(*args, **kwargs)
            organizations = Organization.objects.all()
            for org in organizations:
                delivery , created = DeliveryCompanyUrl.objects.get_or_create(
                    organization=org,
                    delivery_company=self,
                    active=False
                )

    def __str__(self) -> str:
        return self.name


class DeliveryCompanyUrl(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name= "المنظمة")
    delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.CASCADE , verbose_name= "شركة التوصيل")
    url = models.URLField(max_length=300 , null=True , blank=True , verbose_name= "الرابط")
    short_url = models.SlugField(max_length=50 , default=generateShortUrl , verbose_name= "الرابط المختصر")
    active = models.BooleanField(default=False , verbose_name= "مفعل")
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name= "تاريخ الإنشاء")

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.delivery_company.name}"

    def get_absolute_url(self):
        return f"/delivery/{self.short_url}/"



class Template(models.Model):
    name = models.CharField(max_length=255)
    template = models.ImageField(upload_to='media/images/templates/')
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name





class ServiceOffer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name='المنظمة')
    content = models.CharField(max_length=500 , verbose_name='المحتوى')
    expiresAt = models.DateField(verbose_name='تاريخ الانتهاء')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الانشاء')
    organizations = models.ManyToManyField(OrganizationType , verbose_name='المنظمات')

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.id}"







class ClientOffer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , verbose_name='المنظمة')
    content = models.CharField(max_length=500 , verbose_name='المحتوى')
    expiresAt = models.DateField(verbose_name='تاريخ الانتهاء')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الانشاء')
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True , verbose_name='القالب')

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.id}"






class ContactUs(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    link = models.CharField(max_length=255 , verbose_name='الرابط')
    icon = models.ImageField(upload_to='media/images/about_us/', default='images/about_us/default_about_us.png', verbose_name='الشعار')

    def __str__(self) -> str:
        return self.name




class TermsPrivacy(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)




class CommonQuestion(models.Model):
    question = models.CharField(max_length=255 , verbose_name='السؤال')
    answer = models.CharField(max_length=255 , verbose_name='الجواب')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الإنشاء')

    def __str__(self) -> str:
        return self.question
    

class Report(models.Model):
    client = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.client} - {self.organization.name}"



class Subscription(models.Model):
    name = models.CharField(max_length=100 , verbose_name="اسم الاشتراك")
    price = models.FloatField(verbose_name="السعر")
    days = models.IntegerField(validators=[MinValueValidator(1)] , verbose_name="الفترة (الأيام)")

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"
