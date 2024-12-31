from dataclasses import Field
from django.views import generic
from django.views import View
from app.base.models import *
from app.users.models import *
from django.shortcuts import redirect , render
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.views import CustomListBaseView
from app.admin_panel.forms import *
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count, Q

login_required_m =  method_decorator(login_required(login_url='login') , name="dispatch")


class LoginView(View):
    def get(self, request):
        return render(request, 'admin_panel/login.html', context={})

    def post(self, request): 
        phonenumber = request.POST.get('phonenumber', None)
        password = request.POST.get('password', None)
        remember_me = request.POST.get('remember_me', False)
        
        context = {
            'phonenumber': phonenumber,
            'has_error': False,
            'phone_error': False,
            'password_error': False
        }
        
        if not phonenumber or not password:
            context['has_error'] = True
            if not phonenumber:
                context['phone_error'] = True
            if not password:
                context['password_error'] = True
            return render(request, 'admin_panel/login.html', context=context)
            
        user = authenticate(request, phonenumber=phonenumber, password=password)
        if user:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(60*60*4)  # 30 days
            else:
                request.session.set_expiry(0)  # Expire when browser closes
            request.session.modified = True
            return redirect('dashboard')
        else:
            context['has_error'] = True
            context['phone_error'] = True
            context['password_error'] = True
            return render(request, 'admin_panel/login.html', context=context)


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')

@login_required_m
class DashboardView(View):
    def get(self, request):
        
        user_counts = CustomUser.objects.aggregate(
            admins=Count('id', filter=Q(user_type='ADMIN')),
            clients=Count('id', filter=Q(user_type='CLIENT')), 
            shareeks=Count('id', filter=Q(user_type='SHAREEK'))
        )
        admins = user_counts['admins']
        clients = user_counts['clients']
        shareeks = user_counts['shareeks']
        organizations = Organization.objects.count()
        delivery_companies = DeliveryCompany.objects.count()
        delivery_companies_urls = DeliveryCompanyUrl.objects.count()
        social_media = SocialMedia.objects.count()
        social_media_urls = SocialMediaUrl.objects.count()
        context = {
            'admins':admins,
            'clients':clients,
            'shareeks':shareeks,
            'organizations':organizations,
            'delivery_companies':delivery_companies,
            'delivery_companies_urls':delivery_companies_urls,
            'social_media_urls':social_media_urls,
            'social_media':social_media,
        }
        return render(request, 'admin_panel/dashboard.html',context=context)


class ListClientsView(CustomListBaseView):
    model = CustomUser
    context_object_name = 'clients'
    context_fields = ['id','full_name','phonenumber','is_active']
    template_name = 'admin_panel/users/clients/clients_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user_type='CLIENT')


class CreateClientView(generic.CreateView):
    model = CustomUser
    template_name = 'admin_panel/users/clients/client_form.html'
    fields = ['full_name','phonenumber','email','get_notifications','image']
    success_url = '/dashboard/users/clients'

class ClientInfoView(generic.UpdateView):
    model = CustomUser
    template_name = 'admin_panel/users/clients/client_form.html'
    fields = ['full_name','phonenumber','email','get_notifications','image']
    success_url = '/dashboard/users/clients'
    pk_url_kwarg = 'id'


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteClientView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            OrganizationType.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
        return HttpResponseRedirect(reverse('organization-types'))





class ListShareeksView(CustomListBaseView,generic.ListView):
    model = CustomUser
    context_object_name = 'shareeks'
    context_fields = ['id','full_name','phonenumber','is_active']
    template_name = 'admin_panel/users/shareeks/shareeks_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user_type='SHAREEK')


class CreateShareekView(View):
    def get(self,request):
        form = ShareekForm()
        return render(request, 'admin_panel/users/shareeks/shareek_form.html', {'form': form})
    # def post(self, request):
    #     form = ShareekForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         shareek = form.save()
    #         return redirect('users/shareek/')
    #     else:
    #         return render(request, 'admin_panel/users/shareeks/add_shareek.html', {'form': form})
    # model = Shareek
    # form_class = ShareekForm
    # template_name = 'admin_panel/users/shareeks/add_shareek.html'
    # success_url = 'users/shareek/'

class UpdateShareekView(generic.UpdateView):
    model = Shareek
    template_name = 'admin_panel/users/shareeks/shareek_form.html'
    fields = ['shareek', 'commercial_register_id', 'logo', 'name', 'description', 'organization_type', 'website', 'website_short_link']
    success_url = '/dashboard/users/shareeks/'
    pk_url_kwarg = 'id'


class DeleteShareekView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            Shareek.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
        return HttpResponseRedirect(reverse('shareeks'))




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
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            OrganizationType.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
        return HttpResponseRedirect(reverse('organization-types'))





class ListAdminsView(CustomListBaseView,generic.ListView):
    model = CustomUser
    context_object_name = 'admins'
    context_fields = ['id','full_name','phonenumber','is_active']
    template_name = 'admin_panel/users/admins/admins_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user_type='ADMIN')

class CreateAdminView(generic.CreateView):
    model = CustomUser
    template_name = 'admin_panel/users/admins/admin_form.html'
    fields = ['full_name', 'phonenumber', 'email', 'password']
    success_url = '/dashboard/users/admins/'

class UpdateAdminView(generic.UpdateView):
    model = CustomUser
    template_name = 'admin_panel/users/admins/admin_form.html'
    fields = ['full_name','phonenumber','email','get_notifications','image']
    success_url = '/dashboard/users/admins/'
    pk_url_kwarg = 'id'

class DeleteAdminView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            CustomUser.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
        return HttpResponseRedirect(reverse('admins'))

