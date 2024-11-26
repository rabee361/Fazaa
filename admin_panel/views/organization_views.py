from django.views import generic
from utils import permissions
from base.models import *


class ListOrganizationType(generic.ListView):
    queryset = OrganizationType.objects.all()
    template_name = 'organization_type_list.html'


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





class ListDeliveryCompanies(generic.ListView):
    queryset = DeliveryCompany.objects.all()
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
    queryset = DeliveryCompanyLink.objects.all()
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
    queryset = SocialMedia.objects.all()
    template_name = 'branch_list.html'

class CreateSocialMedia(generic.CreateView):
    model = Branch
    template_name = 'branch_form.html'
    fields = ['name', 'address', 'phone', 'email', 'organization']
    success_url = '/admin/branches/'

class DeleteSocialMedia(generic.DeleteView):
    model = SocialMedia
    template_name = 'branch_confirBranchm_delete.html'
    success_url = '/admin/branches/'
    pk_url_kwarg = 'id'

class UpdateSocialMedia(generic.UpdateView):
    model = SocialMedia
    template_name = 'social_media_form.html'
    fields = ['name', 'address', 'phone', 'email', 'organization']
    success_url = '/admin/branches/'
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
    queryset = Branch.objects.all()
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


