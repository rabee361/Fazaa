from django.views import generic
from django.views import View
from base.models import *
from users.models import *
from django.shortcuts import redirect , render
from django.contrib.auth import authenticate , login , logout
from utils.views import CustomListBaseView
from admin_panel.forms import *
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.db.models import Count, Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from utils.views import BaseView


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
                request.session.set_expiry(60*60*4)  # 4 hours
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


class DashboardView(BaseView):
    def get(self, request):
        return render(request, 'admin_panel/dashboard.html',context={})


class DashboardPartialView(BaseView):
    def get(self, request):
        user_counts = User.objects.aggregate(
            admins=Count('id', filter=Q(user_type='ADMIN')),
            clients=Count('id', filter=Q(user_type='CLIENT')), 
            shareeks=Count('id', filter=Q(user_type='SHAREEK'))
        )
        admins = user_counts['admins']
        clients = user_counts['clients']
        shareeks = user_counts['shareeks']
        organizations = Organization.objects.count()
        organization_types = OrganizationType.objects.count()
        delivery_companies = DeliveryCompany.objects.count()
        delivery_companies_urls = DeliveryCompanyUrl.objects.count()
        social_media = SocialMedia.objects.count()
        social_media_urls = SocialMediaUrl.objects.count()
        common_questions = CommonQuestion.objects.count()
        context = {
            'admins':admins,
            'clients':clients,
            'shareeks':shareeks,
            'organizations':organizations,
            'delivery_companies':delivery_companies,
            'delivery_companies_urls':delivery_companies_urls,
            'social_media_urls':social_media_urls,
            'social_media':social_media,
            'organization_types':organization_types,
            'common_questions':common_questions,
        }
        return render(request, 'admin_panel/partials/dashboard_partial.html',context=context)




class ListClientsView(CustomListBaseView):
    model = User
    context_object_name = 'clients'
    context_fields = ['id','full_name','phonenumber','is_active']
    template_name = 'admin_panel/users/clients/clients_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/clients_partial.html'
        if q:
            return super().get_queryset().filter(Q(full_name__icontains=q) | Q(phonenumber__icontains=q), user_type='CLIENT', is_deleted=False)
        else:
            return super().get_queryset().filter(user_type='CLIENT', is_deleted=False)


class CreateClientView(BaseView, generic.CreateView):
    model = User
    form_class = ClientForm
    template_name = 'admin_panel/users/clients/client_form.html'
    success_url = '/dashboard/users/clients'


class ClientInfoView(BaseView):
    def get(self, request, id):
        client = get_object_or_404(User, id=id, user_type='CLIENT', is_deleted=False)
        form = UpdateClientForm(instance=client)
        return render(request, 'admin_panel/users/clients/update_client.html', {'form': form , 'client': client, 'image': client.image})

    def post(self, request, id):
        client = get_object_or_404(User, id=id, user_type='CLIENT', is_deleted=False)
        form = UpdateClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients')
        return render(request, 'admin_panel/users/clients/update_client.html', {'form': form , 'client': client, 'image': client.image})



class DeleteClientView(BaseView):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            User.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('clients'))





class ListShareeksView(CustomListBaseView, generic.ListView):
    model = User
    context_object_name = 'shareeks'
    context_fields = ['id','full_name','phonenumber','is_active']
    template_name = 'admin_panel/users/shareeks/shareeks_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/shareeks_partial.html'
        if q:
            return super().get_queryset().filter(Q(full_name__istartswith=q) | Q(phonenumber__istartswith=q), user_type='SHAREEK', is_deleted=False)
        else:
            return super().get_queryset().filter(user_type='SHAREEK', is_deleted=False)


class CreateShareekView(BaseView, generic.CreateView):
    model = Shareek
    form_class = ShareekForm
    template_name = 'admin_panel/users/shareeks/shareek_form.html'
    success_url = '/dashboard/users/shareek'


class ShareekInfoView(BaseView):
    def get(self, request, id):
        shareek = get_object_or_404(User, id=id, user_type='SHAREEK', is_deleted=False)
        form = UpdateShareekForm(instance=shareek)
        return render(request, 'admin_panel/users/shareeks/update_shareek.html', {'form': form, 'shareek': shareek, 'image': shareek.image})

    def post(self, request, id):
        shareek = get_object_or_404(User, id=id, user_type='SHAREEK', is_deleted=False)
        form = UpdateShareekForm(request.POST, request.FILES, instance=shareek)
        if form.is_valid():
            form.save()
            return redirect('shareeks')
        return render(request, 'admin_panel/users/shareeks/update_shareek.html', {'form': form , 'shareek': shareek, 'image': shareek.image})



class DeleteShareekView(BaseView):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            User.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('shareeks'))



class ListAdminsView(CustomListBaseView, generic.ListView):
    model = User
    context_object_name = 'admins'
    context_fields = ['id','full_name','phonenumber','is_active']
    template_name = 'admin_panel/users/admins/admins_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/admins_partial.html'
        if q:
            return super().get_queryset().filter(Q(full_name__istartswith=q) | Q(phonenumber__istartswith=q), user_type='ADMIN', is_deleted=False)
        else:
            return super().get_queryset().filter(user_type='ADMIN', is_deleted=False)


class CreateAdminView(BaseView):
    def get(self,request):
        form = AdminForm()
        return render (request, 'admin_panel/users/admins/admin_form.html',{'form':form})
    
    def post(self,request):
        form = AdminForm(request.POST,request.FILES)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.user_type = 'ADMIN'
            user.set_password(password)
            user.save()
            return redirect('admins')
        return render(request,'admin_panel/users/admins/admin_form.html',{'form':form})


class BulkActionView(BaseView):
    def post(self, request):
        try:
            selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
            action = request.POST.get('action', '')
            
            if not selected_ids:
                messages.error(request, 'الرجاء اختيار عنصر واحد على الأقل')
                return self.get_redirect_url(request)
                
            users = User.objects.filter(id__in=selected_ids)
            if not users.exists():
                messages.error(request, 'لم يتم العثور على المستخدمين المحددين')
                return self.get_redirect_url(request)

            if action == 'delete':
                # Get all support chats for users being deleted
                for user in users:
                    Message.objects.filter(sender=user).delete()
                users.update(is_deleted=True)
            elif action == 'deactivate':
                users.update(is_active=False)
            elif action == 'activate':
                users.update(is_active=True)
            else:
                messages.error(request, 'إجراء غير صالح')
                
        except json.JSONDecodeError:
            messages.error(request, 'حدث خطأ أثناء معالجة الطلب')
        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
            
        return self.get_redirect_url(request)

    def get_redirect_url(self, request):
        # Get the referer URL to determine which list we came from
        referer = request.META.get('HTTP_REFERER', '')
        if 'clients' in referer:
            return redirect('clients')
        elif 'shareek' in referer:
            return redirect('shareeks')
        else:
            return redirect('admins')


class AdminInfoView(BaseView):
    def get(self, request, id):
        admin = get_object_or_404(User, id=id, user_type='ADMIN', is_deleted=False)
        form = UpdateAdminForm(instance=admin)
        return render(request, 'admin_panel/users/admins/update_admin.html', {'form': form , 'admin': admin, 'image': admin.image})

    def post(self, request, id):
        admin = get_object_or_404(User, id=id, user_type='ADMIN', is_deleted=False)
        form = UpdateAdminForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('admins')
        return render(request, 'admin_panel/users/admins/update_admin.html', {'form': form , 'admin': admin, 'image': admin.image})




class ChangePasswordView(BaseView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id, is_deleted=False)
        form = ChangePasswordForm()
        return render(request, 'admin_panel/users/change_password.html', {
            'form': form,
            'user': user
        })
        
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id, is_deleted=False)
        form = ChangePasswordForm(data=request.POST)

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            return redirect('dashboard')
        return render(request, 'admin_panel/users/change_password.html', {
            'form': form,
            'user': user
        })

