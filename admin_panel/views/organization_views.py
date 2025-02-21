from dataclasses import Field
from django.views import generic
from utils import permissions
from base.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from utils.views import CustomListBaseView
from django.shortcuts import render , redirect
from django.views import View
from django.core.paginator import Paginator
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from admin_panel.forms import *
from django.views.generic.edit import UpdateView

# login required decorator renamed to shorter name
login_required_m =  method_decorator(login_required(login_url='login') , name="dispatch")

# @login_required_m
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
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
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
class DeleteOrganizationType(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            OrganizationType.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
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
    context_fields = ['id','catalog_type','organization','short_url']
    template_name = 'admin_panel/organization/catalogs/catalogs.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for catalog in context['catalogs']:
            catalog.short_url = self.request.build_absolute_uri(catalog.get_absolute_url())
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(organization__name__icontains=search_query)
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

@login_required_m
class DeleteCatalogView(View):
    def post(self, request):
            selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
            if selected_ids:
                Catalog.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
            return HttpResponseRedirect(reverse('catalogs'))


@login_required_m
class ListDeliveryCompanies(CustomListBaseView,generic.ListView):
    model = DeliveryCompany
    context_object_name = 'companies'
    context_fields=['id','name','icon']
    template_name = 'admin_panel/links/delivery_company_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
        

@login_required_m
class CreateDeliveryCompany(generic.CreateView):
    model = DeliveryCompany
    template_name = 'admin_panel/links/delivery_company_form.html'
    fields = ['name','icon']
    success_url = '/dashboard/organization/delivery-companies'

@login_required_m
class UpdateDeliveryCompany(generic.UpdateView):
    model = DeliveryCompany
    template_name = 'admin_panel/links/update_delivery_company.html'
    form_class = DeliveryCompanyForm
    success_url = '/dashboard/organization/delivery-companies'
    pk_url_kwarg = 'id'

    def get_context_data(self):
        context = super().get_context_data()
        context['icon'] = self.object.icon
        return context

@login_required_m
class DeleteDeliveryCompany(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            DeliveryCompany.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
        return HttpResponseRedirect(reverse('delivery-companies'))


@login_required_m
class ListDeliveryLinksView(CustomListBaseView):
    model = DeliveryCompanyUrl
    context_object_name = 'links'
    context_fields = ['id','organization','delivery_company','active','short_url']
    template_name = 'admin_panel/links/delivery/delivey_links.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization','delivery_company')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(organization__name__icontains=search_query)
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

@login_required_m
class DeleteDeliveryLinkView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            DeliveryCompanyUrl.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('delivery-links'))


@login_required_m
class ListSocialMedia(CustomListBaseView):
    model = SocialMedia
    context_object_name = 'socials'
    context_fields = ['id','name','icon']
    template_name = 'admin_panel/links/social_media_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
        
@login_required_m
class CreateSocialMedia(generic.CreateView):
    model = SocialMedia
    template_name = 'admin_panel/links/social_media_form.html'
    fields = ['name', 'icon']
    success_url = '/dashboard/organization/social-media'

@login_required_m
class DeleteSocialMedia(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            SocialMedia.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('social-media'))


@login_required_m
class UpdateSocialMedia(generic.UpdateView):
    model = SocialMedia
    template_name = 'admin_panel/links/update_social_media.html'
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
    context_fields = ['id','organization','social_media','active','short_url']
    template_name = 'admin_panel/links/social/social_links.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization','social_media')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(organization__name__icontains=search_query)
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

@login_required_m
class DeleteSocialLinkView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            SocialMediaUrl.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
        return HttpResponseRedirect(reverse('social-links'))


@login_required_m
class ListBranches(CustomListBaseView,generic.ListView):
    model = Branch
    template_name = 'branch_list.html'

@login_required_m
class CreateBranch(generic.CreateView):
    model = Branch
    template_name = 'branch_form.html'
    fields = ['name', 'address', 'phone', 'email', 'organization']
    success_url = '/admin/branches/'

@login_required_m
class DeleteBranch(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            Branch.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
        return HttpResponseRedirect(reverse('branches'))


@login_required_m
class UpdateBranch(generic.UpdateView):
    model = Branch
    template_name = 'branch_form.html'
    fields = ['name', 'address', 'phone', 'email', 'organization']
    success_url = '/admin/branches/'
    pk_url_kwarg = 'id'


@login_required_m
class ListClientOffers(CustomListBaseView,generic.ListView):
    model = ClientOffer
    context_object_name = 'offers'
    context_fields = ['id','organization','expiresAt','createdAt']
    template_name = 'admin_panel/organization/offers/client_offers.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization','template')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(organization__name__icontains=search_query)
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
    template_name = 'admin_panel/organization/offers/client_offer_form.html'
    form_class = ClientOfferForm
    success_url = '/dashboard/organization/client-offers'
    pk_url_kwarg = 'id'

@login_required_m
class DeleteClientOffer(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
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
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(organization__name__icontains=search_query)
        return queryset
        

@login_required_m
class CreateServiceOffer(generic.CreateView):
    model = ServiceOffer
    template_name = 'admin_panel/organization/offers/service_offer_form.html'
    fields = ['content', 'organization','expiresAt']
    success_url = '/dashboard/organization/service-offers'

@login_required_m
class UpdateServiceOffer(generic.UpdateView):
    model = ServiceOffer
    template_name = 'admin_panel/organization/offers/service_offer_form.html'
    fields = ['content', 'organization','expiresAt']
    success_url = '/dashboard/organization/service-offers'
    pk_url_kwarg = 'id'


@login_required_m
class DeleteServiceOffer(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
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


class DeleteOfferTemplate(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            Template.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('offer-templates'))

