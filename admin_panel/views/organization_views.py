from dataclasses import Field
from django.views import generic
from utils import permissions
from base.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.views import CustomListBaseView
from django.shortcuts import render
from django.views import View
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from admin_panel.forms import *
from django.contrib.auth.decorators import user_passes_test
# login required decorator renamed to shorter name

login_required_m = method_decorator(user_passes_test(lambda u: u.is_authenticated and hasattr(u, 'user_type') and u.user_type == 'ADMIN', login_url='login'), name="dispatch")

class CardUrlView(View):
    def get(self,request,slug):
        try:
            organization = Organization.objects.select_related('organization_type').get(card_url=slug)
            shareek_phonenumber = organization.shareeks.first().user.phonenumber
            branches = Branch.objects.filter(organization=organization)
            return render(request,'admin_panel/QR_Info.html',context={'organization':organization,'shareek_phonenumber':shareek_phonenumber,'branches':branches})
        except Exception as e:
            return render(request, '404.html', status=400)


@login_required_m
class ListOrganizationType(CustomListBaseView):
    model = OrganizationType
    context_object_name = 'types'
    context_fields = ['id','name']
    template_name = 'admin_panel/organization/types.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = super().get_queryset()
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/types_partial.html'
        if q:
            return queryset.filter(name__icontains=q)
        else:
            return queryset


@login_required_m
class CreateOrganizationType(generic.CreateView):
    model = OrganizationType
    template_name = 'admin_panel/organization/type_form.html'
    fields = ['name']
    success_url = '/dashboard/organization/types'


@login_required_m
class UpdateOrganizationType(generic.UpdateView):
    model = OrganizationType
    template_name = 'admin_panel/organization/type_form.html'
    fields = ['name']
    success_url = '/dashboard/organization/types'
    pk_url_kwarg = 'id'


@login_required_m
class OrganizationTypesBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            OrganizationType.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('organization-types'))


@login_required_m
class ListOrganizationsView(CustomListBaseView):
    model = Organization
    context_object_name = 'organizations'
    context_fields = ['id','name','organization_type','card_url']
    template_name = 'admin_panel/organization/info/organizations.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization_type')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = super().get_queryset().select_related('organization_type')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/organizations_partial.html'
        if q:
            return queryset.filter(name__istartswith=q)
        else:
            return queryset

    def get_context_data(self):
        context = super().get_context_data()
        for organization in context['organizations']:
            organization.card_url = self.request.build_absolute_uri(organization.get_absolute_card_url())
        return context


@login_required_m
class OrganizationInfoView(generic.UpdateView):
    model = Organization
    fields = ['name','logo','website','description','organization_type','commercial_register_id']
    template_name = 'admin_panel/organization/info/organization_info.html'
    success_url = '/dashboard/organization/organizations'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization_type')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


@login_required_m
class CreateOrganizationView(generic.CreateView):
    model = Organization
    template_name = 'admin_panel/organization/info/organization_info.html'
    fields = ['name','organization_type','logo','website','description']
    success_url = '/dashboard/organization/organizations'


@login_required_m
class ListCatalogsView(CustomListBaseView):
    model = Catalog
    context_object_name = 'catalogs'
    context_fields = ['id','catalog_type','organization','visits','short_url']
    template_name = 'admin_panel/organization/catalogs/catalogs.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for catalog in context['catalogs']:
            catalog.short_url = self.request.build_absolute_uri(catalog.get_absolute_url())
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization')
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/catalogs_partial.html'
        if q:
            return queryset.filter(organization__name__icontains=q)
        else:
            return queryset


@login_required_m
class CreateCatalogView(generic.CreateView):
    model = Catalog
    template_name = 'admin_panel/organization/catalogs/catalog_form.html'
    form_class = CatalogForm
    success_url = '/dashboard/organization/catalogs'

@login_required_m
class UpdateCatalogView(generic.UpdateView):
    model = Catalog
    template_name = 'admin_panel/organization/catalogs/catalog_form.html'
    fields = ['file', 'organization', 'catalog_type']
    success_url = '/dashboard/organization/catalogs'
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        if 'file' in form.changed_data:
            form.instance.visits = 0
        return super().form_valid(form)

@login_required_m
class CatalogBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            Catalog.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('catalogs'))



class ListImagesGalleryView(CustomListBaseView):
    model = ImageGallery
    context_object_name = 'images'
    context_fields = ['id','organization','createdAt']
    template_name = 'admin_panel/organization/gallery/images_gallery.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = super().get_queryset().select_related('organization')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/images_gallery_partial.html'
        if q:
            return queryset.filter(organization__name__icontains=q)
        else:
            return queryset

class CreateImageGalleryView(generic.CreateView):
    model = ImageGallery
    template_name = 'admin_panel/organization/gallery/image_gallery_form.html'
    fields = ['image','organization']
    success_url = '/dashboard/organization/images-gallery'

class UpdateImageGalleryView(generic.UpdateView):
    model = ImageGallery
    template_name = 'admin_panel/organization/gallery/update_image_gallery.html'
    fields = ['image','organization']
    success_url = '/dashboard/organization/images-gallery'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = self.object.image
        return context

class ImageGalleryBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            ImageGallery.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('images-gallery'))

class ListReelsGalleryView(CustomListBaseView):
    model = ReelsGallery
    context_object_name = 'reels'
    context_fields = ['id','organization','createdAt']
    template_name = 'admin_panel/organization/gallery/reels_gallery.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = super().get_queryset().select_related('organization')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/reels_gallery_partial.html'
        if q:
            return queryset.filter(organization__name__icontains=q)
        else:
            return queryset

class CreateReelGalleryView(generic.CreateView):
    model = ReelsGallery
    template_name = 'admin_panel/organization/gallery/reel_gallery_form.html'
    fields = ['video','organization']
    success_url = '/dashboard/organization/reels-gallery'

class UpdateReelGalleryView(generic.UpdateView):
    model = ReelsGallery
    template_name = 'admin_panel/organization/gallery/update_reel_gallery.html'
    fields = ['video','organization']
    success_url = '/dashboard/organization/reels-gallery'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video'] = self.object.video
        return context

class ReelGalleryBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            ReelsGallery.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('reels-gallery'))







@login_required_m
class ListDeliveryCompanies(CustomListBaseView,generic.ListView):
    model = DeliveryCompany
    context_object_name = 'companies'
    context_fields=['id','name','icon_thumbnail']
    template_name = 'admin_panel/links/delivery/delivery_company_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/delivery_companies_partial.html'
        if q:
            return queryset.filter(name__icontains=q)
        else:
            return queryset

        

@login_required_m
class CreateDeliveryCompany(generic.CreateView):
    model = DeliveryCompany
    template_name = 'admin_panel/links/delivery/delivery_company_form.html'
    fields = ['name','icon']
    success_url = '/dashboard/organization/delivery-companies'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.create_delivery_urls()
        return response 

@login_required_m
class UpdateDeliveryCompany(generic.UpdateView):
    model = DeliveryCompany
    template_name = 'admin_panel/links/delivery/delivery_company_form.html'
    form_class = DeliveryCompanyForm
    success_url = '/dashboard/organization/delivery-companies'
    pk_url_kwarg = 'id'

    def get_context_data(self):
        context = super().get_context_data()
        context['icon'] = self.object.icon
        return context

@login_required_m
class DeliveryCompanyActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            DeliveryCompany.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('delivery-companies'))


@login_required_m
class ListDeliveryLinksView(CustomListBaseView):
    model = DeliveryCompanyUrl
    context_object_name = 'links'
    context_fields = ['id','organization','delivery_company','active','visits','short_url']
    template_name = 'admin_panel/links/delivery/delivey_links.html'
    
    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = super().get_queryset().select_related('organization','delivery_company').filter(deleted=False)
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/delivery_links_partial.html'
        if q:
            return queryset.filter(organization__name__icontains=q)
        else:
            return queryset
    
    def get_context_data(self):
        context = super().get_context_data()
        for link in context['links']:
            link.short_url = self.request.build_absolute_uri(link.get_absolute_url())
        return context


@login_required_m
class CreateDeliveryLinkView(generic.CreateView):
    model = DeliveryCompanyUrl
    template_name = 'admin_panel/links/delivery/delivery_link_form.html'
    fields = ['url', 'delivery_company','active' ,'organization']
    success_url = '/dashboard/organization/delivery-links'

@login_required_m
class UpdateDeliveryLinkView(generic.UpdateView):
    model = DeliveryCompanyUrl
    template_name = 'admin_panel/links/delivery/delivery_link_form.html'
    fields = ['url', 'delivery_company','active' ,'organization']
    success_url = '/dashboard/organization/delivery-links'
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        if 'url' in form.changed_data:
            form.instance.visits = 0
        return super().form_valid(form)

@login_required_m
class DeliveryLinkBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            DeliveryCompanyUrl.objects.delete_delivery_urls(selected_ids)
        elif action == 'activate':
            DeliveryCompanyUrl.objects.filter(id__in=selected_ids).update(active=True)
        elif action == 'deactivate':
            DeliveryCompanyUrl.objects.filter(id__in=selected_ids).update(active=False)
        return HttpResponseRedirect(reverse('delivery-links'))


@login_required_m
class ListSocialMedia(CustomListBaseView):
    model = SocialMedia
    context_object_name = 'socials'
    context_fields = ['id','name','icon_thumbnail']
    template_name = 'admin_panel/links/social/social_media_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/social_media_partial.html'
        if q:
            return queryset.filter(name__icontains=q)
        else:
            return queryset

        

@login_required_m
class CreateSocialMedia(generic.CreateView):
    model = SocialMedia
    template_name = 'admin_panel/links/social/social_media_form.html'
    fields = ['name', 'icon']
    success_url = '/dashboard/organization/social-media'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.create_social_urls()
        return response

@login_required_m
class SocialMediaActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            SocialMedia.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('social-media'))


@login_required_m
class UpdateSocialMedia(generic.UpdateView):
    model = SocialMedia
    template_name = 'admin_panel/links/social/social_media_form.html'
    form_class = SocialMediaForm
    success_url = '/dashboard/organization/social-media'
    pk_url_kwarg = 'id'

    def get_context_data(self):
        context = super().get_context_data()
        context['icon'] = self.object.icon
        return context

@login_required_m
class ListSocialLinksView(CustomListBaseView):
    model = SocialMediaUrl
    context_object_name = 'links'
    context_fields = ['id','organization','social_media','active','visits','short_url']
    template_name = 'admin_panel/links/social/social_links.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization','social_media').filter(deleted=False)
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/social_links_partial.html'
        if q:
            return queryset.filter(organization__name__icontains=q , deleted=False)
        else:
            return queryset

    def get_context_data(self):
        context = super().get_context_data()
        for link in context['links']:
            link.short_url = self.request.build_absolute_uri(link.get_absolute_url())
        return context


@login_required_m
class CreateSocialLinkView(generic.CreateView):
    model = SocialMediaUrl
    template_name = 'admin_panel/links/social/social_link_form.html'
    fields = ['url', 'social_media','active','organization']
    success_url = '/dashboard/organization/social-links'

@login_required_m
class UpdateSocialLinkView(generic.UpdateView):
    model = SocialMediaUrl
    template_name = 'admin_panel/links/social/social_link_form.html'
    fields = ['url', 'social_media','active','organization']
    success_url = '/dashboard/organization/social-links'
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        if 'url' in form.changed_data:
            form.instance.visits = 0
        return super().form_valid(form)

@login_required_m
class SocialUrlBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            SocialMediaUrl.objects.delete_social_urls(selected_ids)
        elif action == 'activate':
            SocialMediaUrl.objects.filter(id__in=selected_ids).update(active=True)
        elif action == 'deactivate':
            SocialMediaUrl.objects.filter(id__in=selected_ids).update(active=False)
        return HttpResponseRedirect(reverse('social-links'))


@login_required_m
class ListBranches(CustomListBaseView):
    model = Branch
    context_object_name = 'branches'
    context_fields = ['id','organization','name','short_url'] # add visits
    template_name = 'admin_panel/organization/branches/branches.html'
    success_url = '/dashboard/organization/branches'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization')
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/branches_partial.html'
        if q:
            return queryset.filter(organization__name__icontains=q)
        else:
            return queryset

    def get_context_data(self):
        context = super().get_context_data()
        for branch in context['branches']:
            branch.short_url = self.request.build_absolute_uri(branch.get_absolute_url())
        return context


@login_required_m
class CreateBranch(generic.CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'admin_panel/organization/branches/branch_form.html'
    success_url = '/dashboard/organization/branches'

@login_required_m
class BranchActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            # Branch.objects.filter(id__in=selected_ids).delete()
            pass
        return HttpResponseRedirect(reverse('branches'))


@login_required_m
class UpdateBranch(generic.UpdateView):
    model = Branch
    template_name = 'admin_panel/organization/branches/branch_form.html'
    form_class = BranchForm
    success_url = '/dashboard/organization/branches'
    pk_url_kwarg = 'id'


@login_required_m
class ListClientOffers(CustomListBaseView,generic.ListView):
    model = ClientOffer
    context_object_name = 'offers'
    context_fields = ['id','organization','expiresAt','createdAt']
    template_name = 'admin_panel/organization/offers/client_offers.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization')
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/client_offers_partial.html'
        if q:
            return queryset.filter(organization__name__icontains=q)
        else:
            return queryset
        

@login_required_m
class CreateClientOffer(generic.CreateView):
    model = ClientOffer
    template_name = 'admin_panel/organization/offers/client_offer_form.html'
    form_class = ClientOfferForm
    success_url = '/dashboard/organization/client-offers'

@login_required_m
class UpdateClientOffer(generic.UpdateView):
    model = ClientOffer
    template_name = 'admin_panel/organization/offers/update_client_offer.html'
    form_class = ClientOfferForm
    success_url = '/dashboard/organization/client-offers'
    pk_url_kwarg = 'id'

    def get_context_data(self):
        context = super().get_context_data()
        context['cover'] = self.object.cover
        return context


@login_required_m
class ClientOfferBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            ClientOffer.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('client-offers'))


@login_required_m
class ListServiceOffers(CustomListBaseView,generic.ListView):
    model = ServiceOffer
    context_object_name = 'offers'
    context_fields = ['id','organization','expiresAt','createdAt']
    template_name = 'admin_panel/organization/offers/service_offers.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization')
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/service_offers_partial.html'
        if q:
            return queryset.filter(organization__name__icontains=q)
        else:
            return queryset
        

@login_required_m
class CreateServiceOffer(generic.CreateView):
    model = ServiceOffer
    template_name = 'admin_panel/organization/offers/service_offer_form.html'
    form_class = ServiceOfferForm
    success_url = '/dashboard/organization/service-offers'

@login_required_m
class UpdateServiceOffer(generic.UpdateView):
    model = ServiceOffer
    template_name = 'admin_panel/organization/offers/service_offer_form.html'
    form_class = ServiceOfferForm
    success_url = '/dashboard/organization/service-offers'
    pk_url_kwarg = 'id'

@login_required_m
class ServiceOfferBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':  
            ServiceOffer.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('service-offers'))


class ListOfferTemplates(CustomListBaseView):
    model = Template
    context_object_name = 'templates'
    context_fields = ['id','name','createdAt']
    template_name = 'admin_panel/organization/offers/offer_templates.html'
    

class CreateOfferTemplate(generic.CreateView):
    model = Template
    template_name = 'admin_panel/organization/offers/offer_template_form.html'
    fields = ['name','template']
    success_url = '/dashboard/organization/offer-templates'


class UpdateOfferTemplate(generic.UpdateView):
    model = Template
    template_name = 'admin_panel/organization/offers/offer_template_form.html'
    fields = ['name','template']
    success_url = '/dashboard/organization/offer-templates'
    pk_url_kwarg = 'id'

    def get_context_data(self):
        context = super().get_context_data()
        context['template'] = self.object.template
        return context

class DeleteOfferTemplate(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            Template.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('offer-templates'))

