from tabnanny import verbose
from typing import Iterable
from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator
from utils.helper import generateShortLink
# Create your models here.




class OrganizationType(models.Model):
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    createAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الانشاء')

    def __str__(self) -> str:
        return self.name


class Organization(models.Model):
    commercial_register_id = models.IntegerField()
    logo = models.ImageField(upload_to='media/organizations/logos/', default='media/images/organizations/logos/default.png')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255 , null=True, blank=True)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True)
    website = models.CharField(max_length=300 , null=True, blank=True)
    website_short_link = models.CharField(max_length=30 , null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    long = models.FloatField(null=True ,blank=True)
    lat = models.FloatField(null=True ,blank=True)

    def __str__(self) -> str:
        return self.name


class Branch(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # default method for settings name ex: org-branch2
    long = models.FloatField()
    lat = models.FloatField()
    description = models.CharField(max_length=255,null=True ,blank=True)

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

    catalog_type = models.CharField(max_length=255 , choices=CATALOG_TYPES.choices)
    file = models.FileField(upload_to='media/images/catalogs/')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

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



class SocialMediaLink(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    original_link = models.URLField(max_length=300)
    short_link = models.URLField(max_length=30)
    active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = generateShortLink(self.original_link)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.social_media.name}"



class DeliveryCompany(models.Model):
    name = models.CharField(max_length=255,verbose_name='الاسم')
    icon = models.ImageField(upload_to='media/images/delivery_company/', default='media/images/delivery_company/default_company.png',verbose_name='الصورة')

    def __str__(self) -> str:
        return self.name


class DeliveryCompanyLink(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.CASCADE)
    original_link = models.URLField(max_length=300)
    short_link = models.URLField(max_length=30)
    active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = generateShortLink(self.original_link)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.delivery_company.name}"





class Template(models.Model):
    name = models.CharField(max_length=255)
    template = models.ImageField(upload_to='media/images/templates/')
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name





class ServiceOffer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    expiresAt = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    organizations = models.ManyToManyField(OrganizationType)

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.id}"







class ClientOffer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    expiresAt = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)

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