from django.contrib import admin
from .models import *
from utils.forms import *
from leaflet.admin import LeafletGeoAdmin
# Register your models here.


class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon']
    search_fields = ['name']


class SocialMediaUrlAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'social_media', 'short_url']
    list_filter = ['organization', 'social_media']


class DeliveryCompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon']
    search_fields = ['name']


class DeliveryCompanyUrlAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'delivery_company', 'short_url']
    list_filter = ['organization', 'delivery_company']


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'organization_type']
    list_filter = ['organization_type']
    search_fields = ['name', 'description']


class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','createdAt']
    search_fields = ['name']

class BranchAdmin(LeafletGeoAdmin):
    list_display = ['id', 'name', 'organization', 'location']
    list_filter = ['organization']
    search_fields = ['name', 'description']


class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'image', 'createdAt']
    list_filter = ['organization', 'createdAt']

class ReelsGalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'video', 'createdAt']
    list_filter = ['organization', 'createdAt']

class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization' ,'catalog_type', 'file']
    list_filter = ['organization']

class TemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'createdAt']

class ServiceOfferAdmin(admin.ModelAdmin):
    list_display = ['id','organization__name','expiresAt']

class ClientOfferAdmin(admin.ModelAdmin):
    list_display = ['id','organization__name','expiresAt']


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'organization', 'content', 'createdAt']
    list_filter = ['client', 'organization', 'createdAt']
    search_fields = ['content']


class CommonQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'answer', 'createdAt']
    search_fields = ['question', 'answer']

class TermsPrivacyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'createdAt']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationType, OrganizationTypeAdmin)
admin.site.register(Branch, BranchAdmin)
# admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(ReelsGallery, ReelsGalleryAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(SocialMediaUrl, SocialMediaUrlAdmin)
admin.site.register(DeliveryCompany, DeliveryCompanyAdmin)
admin.site.register(DeliveryCompanyUrl, DeliveryCompanyUrlAdmin)
admin.site.register(ClientOffer, ClientOfferAdmin)
admin.site.register(ServiceOffer, ServiceOfferAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(CommonQuestion, CommonQuestionAdmin)
admin.site.register(TermsPrivacy, TermsPrivacyAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
