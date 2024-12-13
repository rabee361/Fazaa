from django.views import generic
from utils import permissions
from base.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from utils.views import FieldListBaseView
login_required_m =  method_decorator(login_required(login_url='login') , name="dispatch")



class ListOrganizationType(FieldListBaseView, ListView):
    model = OrganizationType
    context_object_name = 'types'
    context_fields = ['id','name','createAt']
    template_name = 'admin_panel/organization/types.html'


class CreateOrganizationType(generic.CreateView):
    model = OrganizationType
    template_name = 'organization_type_form.html'
    fields = ['name']
    success_url = '/admin/organization-types/'


class UpdateOrganizationType(generic.UpdateView):
    model = OrganizationType
    template_name = 'organization_type_form.html'
    fields = ['name']
    success_url = '/admin/organization-types/'
    pk_url_kwarg = 'id'


class DeleteOrganizationType(generic.DeleteView):
    model = OrganizationType
    template_name = 'organization_type_confirm_delete.html'
    success_url = '/admin/organization-types/'
    pk_url_kwarg = 'id'





class ListCatalogsView(generic.ListView):
    model = Catalog
    template_name = 'catalog_list.html' 


class CreateCatalogView(generic.CreateView):
    model = Catalog
    template_name = 'catalog_form.html'
    fields = ['name', 'organization']
    success_url = '/admin/catalogs/'

class UpdateCatalogView(generic.UpdateView):
    model = Catalog
    template_name = 'catalog_form.html'
    fields = ['name', 'organization']
    success_url = '/admin/catalogs/'
    pk_url_kwarg = 'id'

class DeleteCatalogView(generic.DeleteView):
    model = Catalog
    template_name = 'catalog_confirm_delete.html'
    success_url = '/admin/catalogs/'
    pk_url_kwarg = 'id'



class ListDeliveryCompanies(generic.ListView):
    model = DeliveryCompany
    template_name = 'delivery_company_list.html'

class CreateDeliveryCompany(generic.CreateView):
    model = DeliveryCompany
    template_name = 'delivery_company_form.html'
    fields = ['name']
    success_url = '/admin/delivery-companies/'

class UpdateDeliveryCompany(generic.UpdateView):
    model = DeliveryCompany
    template_name = 'delivery_company_form.html'
    fields = ['name']
    success_url = '/admin/delivery-companies/'
    pk_url_kwarg = 'id'

class DeleteDeliveryCompany(generic.DeleteView):
    model = DeliveryCompany
    template_name = 'delivery_company_confirm_delete.html'
    success_url = '/admin/delivery-companies/'
    pk_url_kwarg = 'id'





class ListDeliveryLinks(generic.ListView):
    queryset = DeliveryCompanyLink
    template_name = 'delivery_link_list.html'

class CreateDeliveryCompanyLink(generic.CreateView):
    model = DeliveryCompanyLink
    template_name = 'delivery_link_form.html'
    fields = ['name', 'url', 'delivery_company']
    success_url = '/admin/delivery-links/'

class UpdateDeliveryCompanyLink(generic.UpdateView):
    model = DeliveryCompanyLink
    template_name = 'delivery_link_form.html'
    fields = ['name', 'url', 'delivery_company']
    success_url = '/admin/delivery-links/'
    pk_url_kwarg = 'id'

class DeleteDeliveryCompanyLink(generic.DeleteView):
    model = DeliveryCompanyLink
    template_name = 'delivery_link_confirm_delete.html'
    success_url = '/admin/delivery-links/'
    pk_url_kwarg = 'id'





class ListSocialMedia(generic.ListView):
    model = SocialMedia
    template_name = 'social_media_list.html'

class CreateSocialMedia(generic.CreateView):
    model = Branch
    template_name = 'create_social_media.html'
    fields = ['name', 'icon']
    success_url = '/dashboard/social-media/'

class DeleteSocialMedia(generic.DeleteView):
    model = SocialMedia
    template_name = 'delete_social_media.html'
    success_url = '/dashboard/social-media/'
    pk_url_kwarg = 'id'

class UpdateSocialMedia(generic.UpdateView):
    model = SocialMedia
    template_name = 'social_media_form.html'
    fields = ['name', 'icon']
    success_url = '/dashboard/social-media/'
    pk_url_kwarg = 'id'




class ListSocialMediaLinks(generic.ListView):
    pass

class CreateSocialMediaLink(generic.CreateView):
    pass

class DeleteSocialMediaLink(generic.DeleteView):
    pass

class UpdateSocialMediaLink(generic.UpdateView):
    pass



class ListBranches(generic.ListView):
    model = Branch
    template_name = 'branch_list.html'

class CreateBranch(generic.CreateView):
    model = Branch
    template_name = 'branch_form.html'
    fields = ['name', 'address', 'phone', 'email', 'organization']
    success_url = '/admin/branches/'

class DeleteBranch(generic.DeleteView):
    model = Branch
    template_name = 'branch_confirm_delete.html'
    success_url = '/admin/branches/'
    pk_url_kwarg = 'id'

class UpdateBranch(generic.UpdateView):
    model = Branch
    template_name = 'branch_form.html'
    fields = ['name', 'address', 'phone', 'email', 'organization']
    success_url = '/admin/branches/'
    pk_url_kwarg = 'id'







class ListClientOffers(generic.ListView):
    model = ClientOffer
    template_name = 'client_offer_list.html'

class CreateClientOffer(generic.CreateView):
    model = ClientOffer
    template_name = 'client_offer_form.html'
    fields = ['name', 'description', 'organization']
    success_url = '/admin/client-offers/'

class UpdateClientOffer(generic.UpdateView):
    model = ClientOffer
    template_name = 'client_offer_form.html'
    fields = ['name', 'description', 'organization']
    success_url = '/admin/client-offers/'
    pk_url_kwarg = 'id'

class DeleteClientOffer(generic.DeleteView):
    model = ClientOffer
    template_name = 'client_offer_confirm_delete.html'
    success_url = '/admin/client-offers/'
    pk_url_kwarg = 'id'




class ListServiceOffers(generic.ListView):
    model = ServiceOffer
    template_name = 'service_offer_list.html'

class CreateServiceOffer(generic.CreateView):
    model = ServiceOffer
    template_name = 'service_offer_form.html'
    fields = ['name', 'description', 'organization']
    success_url = '/admin/service-offers/'

class UpdateServiceOffer(generic.UpdateView):
    model = ServiceOffer
    template_name = 'service_offer_form.html'
    fields = ['name', 'description', 'organization']
    success_url = '/admin/service-offers/'
    pk_url_kwarg = 'id'

class DeleteServiceOffer(generic.DeleteView):
    model = ServiceOffer
    template_name = 'service_offer_confirm_delete.html'
    success_url = '/admin/service-offers/'
    pk_url_kwarg = 'id'
