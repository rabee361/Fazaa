from django.contrib import admin
from .models import *
from utils.forms import *

# Register your models here.


class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon']
    search_fields = ['name']


class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'social_media', 'original_link', 'short_link']
    list_filter = ['organization', 'social_media']


class DeliveryCompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon']
    search_fields = ['name']


class DeliveryCompanyMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'delivery_company', 'original_link', 'short_link']
    list_filter = ['organization', 'delivery_company']


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'organization_type']
    list_filter = ['organization_type']
    search_fields = ['name', 'description']


class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','createAt']
    search_fields = ['name']


class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'organization', 'long', 'lat']
    list_filter = ['organization']
    search_fields = ['name', 'description']




class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'image', 'createdAt']
    list_filter = ['organization', 'createdAt']


class ReelsGalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'video', 'createdAt']
    list_filter = ['organization', 'createdAt']


class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'file', 'createdAt']
    list_filter = ['organization', 'createdAt']




class DeliveryCompanyLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'delivery_company', 'short_link', 'createdAt']
    list_filter = ['delivery_company', 'createdAt']


class TemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'createdAt']


class ServiceOfferAdmin(admin.ModelAdmin):
    list_display = ['id','organization__name','content','expiresAt']

class ClientOfferAdmin(admin.ModelAdmin):
    list_display = ['id','organization__name','content','expiresAt']



admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(Branch, BranchAdmin)
# admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(ReelsGallery, ReelsGalleryAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(SocialMediaLink, SocialMediaLinkAdmin)
admin.site.register(DeliveryCompany, DeliveryCompanyAdmin)
admin.site.register(DeliveryCompanyLink, DeliveryCompanyLinkAdmin)
admin.site.register(ClientOffer, ClientOfferAdmin)
admin.site.register(ServiceOffer, ServiceOfferAdmin)
admin.site.register(Template, TemplateAdmin)
