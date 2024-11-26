from django.views import generic
from django.views import View
from base.models import *
from users.models import *






class LoginView(View):
    pass

class LogoutView(View):
    pass

class DashboardView(View):
    pass




class ListClients(generic.ListView):
    queryset = Client
    template_name = 'organization_type_list.html'

class CreateClient(generic.CreateView):
    model = OrganizationType
    template_name = 'organization_type_form.html'
    fields = ['name']
    success_url = '/admin/organization-types/'

class UpdateClient(generic.UpdateView):
    model = OrganizationType
    template_name = 'organization_type_form.html'
    fields = ['name']
    success_url = '/admin/organization-types/'
    pk_url_kwarg = 'id'

class DeleteClient(generic.DeleteView):
    model = OrganizationType
    template_name = 'organization_type_confirm_delete.html'
    success_url = '/admin/organization-types/'
    pk_url_kwarg = 'id'

class GetClient(generic.DetailView):
    model = OrganizationType
    template_name = 'organization_type_confirm_delete.html'
    pk_url_kwarg = 'id'






class ListShareeks(generic.ListView):
    model = Shareek
    template_name = 'shareek_list.html'

class CreateShareek(generic.CreateView):
    model = Shareek
    template_name = 'shareek_form.html'
    fields = ['shareek', 'commercial_register_id', 'logo', 'name', 'description', 'organization_type', 'website', 'website_short_link']
    success_url = 'users/shareek/'

class UpdateShareek(generic.UpdateView):
    model = Shareek
    template_name = 'shareek_form.html'
    fields = ['shareek', 'commercial_register_id', 'logo', 'name', 'description', 'organization_type', 'website', 'website_short_link']
    success_url = 'users/shareek/'
    pk_url_kwarg = 'id'

class DeleteShareek(generic.DeleteView):
    model = Shareek
    template_name = 'shareek_confirm_delete.html'
    success_url = 'users/shareek/'
    pk_url_kwarg = 'id'

class GetShareek(generic.DetailView):
    model = Shareek
    template_name = 'shareek_detail.html'
    pk_url_kwarg = 'id'






class ListSubscriptions(generic.ListView):
    model = Subscription
    template_name = 'subscription_list.html'


class CreateSubscription(generic.CreateView):
    model = Subscription
    template_name = 'subscription_form.html'
    fields = ['shareek', 'commercial_register_id', 'logo', 'name', 'description', 'organization_type', 'website', 'website_short_link']
    success_url = '/admin/organizations/'


class UpdateSubscription(generic.UpdateView):
    model = Subscription
    template_name = 'subscription_form.html'
    fields = ['shareek', 'commercial_register_id', 'logo', 'name', 'description', 'organization_type', 'website', 'website_short_link']
    success_url = '/admin/organizations/'
    pk_url_kwarg = 'id'


class DeleteSubscription(generic.DeleteView):
    model = Subscription
    template_name = 'subscription_confirm_delete.html'
    success_url = '/admin/organizations/'
    pk_url_kwarg = 'id'


class GetSubscription(generic.DetailView):
    model = Subscription
    template_name = 'subscription_detail.html'
    pk_url_kwarg = 'id'






class ListAdmins(generic.ListView):
    model = CustomUser
    template_name = 'admin_list.html'

class CreateAdmin(generic.CreateView):
    model = Shareek
    template_name = 'admin_form.html'
    fields = ['shareek', 'commercial_register_id', 'logo', 'name', 'description', 'organization_type', 'website', 'website_short_link']
    success_url = 'users/shareek/'

class UpdateAdmin(generic.UpdateView):
    model = CustomUser
    template_name = 'admin_form.html'
    fields = ['shareek', 'commercial_register_id', 'logo', 'name', 'description', 'organization_type', 'website', 'website_short_link']
    success_url = 'users/shareek/'
    pk_url_kwarg = 'id'

class DeleteAdmin(generic.DeleteView):
    model = CustomUser
    template_name = 'admin_confirm_delete.html'
    success_url = 'users/shareek/'
    pk_url_kwarg = 'id'

class GetAdmin(generic.DetailView):
    model = Shareek
    template_name = 'shareek_detail.html'
    pk_url_kwarg = 'id'

