from tabnanny import verbose
from typing import Iterable
from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator
from utils.helper import generateShortUrl
# Create your models here.




class OrganizationType(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    createAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الانشاء')

    def __str__(self) -> str:
        return self.name


class Organization(models.Model):
    commercial_register_id = models.IntegerField(null=True , blank=True)
    logo = models.ImageField(upload_to='media/organizations/logos/', default='media/images/organizations/logos/default.png')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255 , null=True, blank=True)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True)
    website = models.CharField(max_length=300 , null=True, blank=True)
    website_short_url = models.SlugField(max_length=50 , default=generateShortUrl)
    card_url = models.SlugField(max_length=50 , default=generateShortUrl)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_card_url(self):
        return f"/card/{self.card_url}/"

    def get_absolute_website_url(self):
        return f"/website/{self.website_short_url}/"


class Branch(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # default method for settings name ex: org-branch2
    long = models.FloatField()
    lat = models.FloatField()
    description = models.CharField(max_length=255,null=True ,blank=True)

    def __str__(self) -> str:
        return self.name
    

# class BranchUrl(models.Model):
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     url = models.URLField(max_length=300)
#     short_url = models.CharField(max_length=50)

#     def __str__(self) -> str:
#         return f"{self.branch.organization.name} - {self.branch.name}"



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
    file = models.FileField(upload_to='media/images/catalogs/')
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

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.catalog_type}"

    


class SocialMedia(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    icon = models.ImageField(upload_to='media/images/social_media/', default='media/images/social_media/default_media.png',verbose_name='الصورة')

    def __str__(self) -> str:
        return self.name



class SocialMediaUrl(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    url = models.URLField(max_length=300, null=True , blank=True)
    short_url = models.SlugField(max_length=50 , default=generateShortUrl)
    active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.social_media.name}"

    def get_absolute_url(self):
        return f"/social/{self.short_url}/"


class DeliveryCompany(models.Model):
    name = models.CharField(max_length=255,verbose_name='الاسم')
    icon = models.ImageField(upload_to='media/images/delivery_company/', default='media/images/delivery_company/default_company.png',verbose_name='الصورة')

    def __str__(self) -> str:
        return self.name


class DeliveryCompanyUrl(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.CASCADE)
    url = models.URLField(max_length=300 , null=True , blank=True)
    short_url = models.SlugField(max_length=50 , default=generateShortUrl)
    active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

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






class AboutUs(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='media/images/about_us/', default='images/about_us/default_about_us.png')

    def __str__(self) -> str:
        return self.name





class CommonQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.question