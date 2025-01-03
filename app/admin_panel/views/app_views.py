from django.views import View , generic
from app.users.models import *
from app.base.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect , render
from utils.views import CustomListBaseView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import json

login_required_m =  method_decorator(login_required, name="dispatch")




class SocialMediaSlugUrlView(View):
    def get(self,request,slug):
        social = SocialMediaUrl.objects.get(short_url=slug)
        return redirect(social.url)


class WebsiteSlugUrlView(View):
    def get(self,request,slug):
        organization = Organization.objects.get(website_short_url=slug)
        return redirect(organization.website)



class DeliverySlugUrlView(View):
    def get(self,request,slug):
        delivery = DeliveryCompanyUrl.objects.get(short_url=slug)
        return redirect(delivery.url)


class CatalogSlugUrlView(View):
    def get(self,request,slug):
        catalog = Catalog.objects.get(short_url=slug)
        return redirect(catalog.file.url)


class ListReportsView(CustomListBaseView):
    model = Report
    context_object_name = 'reports'
    context_fields = ['id','organization','client','createdAt']
    template_name = 'admin_panel/reports/reports.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q').select_related('organization')
        if search_query:
            queryset = queryset.filter(organization__name__icontains=search_query)
        return queryset


class GetReportView(generic.DeleteView):
    model = Report
    context_object_name = 'report'

class DeleteReportView(generic.DeleteView):
    model = Report
    context_object_name = 'report'



class CommonQuestionsView(CustomListBaseView):
    model = CommonQuestion
    context_object_name = 'common_questions'   
    context_fields = ['id','question','answer']
    template_name = 'admin_panel/app/common_questions/common_questions.html'


class CreateQuestionView(generic.CreateView):
    model = CommonQuestion
    fields = ['question','answer']
    template_name = 'admin_panel/app/common_questions/common_question_form.html'
    success_url = '/dashboard/organization/common-questions'

class UpdateQuestionView(generic.UpdateView):
    model = CommonQuestion
    fields = ['question','answer']
    template_name = 'admin_panel/app/common_questions/common_question_form.html'
    success_url = '/dashboard/organization/common-questions'
    pk_url_kwarg = 'id'

class DeleteQuestionView(View):
    def post(self, request):    
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            CommonQuestion.objects.filter(id__in=selected_ids).delete()
        messages.success(request, 'تم حذف العناصر المحددة بنجاح')
        return HttpResponseRedirect(reverse('common-questions'))



class BaseNotificationsView(CustomListBaseView):
    model = Notification
    context_object_name = 'notifications'
    context_fields = ['id','title','createdAt']
    template_name = 'admin_panel/notifications/notifications.html'



class SendNotificationView(generic.CreateView):
    model = Notification
    template_name = 'admin_panel/notifications/send_notification.html'
    fields = ['title','body']
    success_url = '/dashboard/organization/notifications'



class DeleteNotificationView(View):
    def post(self, request):
            selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
            if selected_ids:
                Notification.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
            return HttpResponseRedirect(reverse('notifications'))



class ContactUsView(CustomListBaseView):
    model = ContactUs
    context_object_name = 'contact_us'
    context_fields = ['id','name','link','icon']
    template_name = 'admin_panel/app/contact_us/contact_us.html'

class CreateContactUsView(generic.CreateView):
    model = ContactUs
    template_name = 'admin_panel/app/contact_us/contact_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/contact-us'

class UpdateContactUsView(generic.UpdateView):
    model = ContactUs
    context_object_name = 'contact_us'
    template_name = 'admin_panel/app/contact_us/contact_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/contact-us'
    pk_url_kwarg = 'id'

class DeleteContactUsView(View):
    def post(self, request):
            selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
            if selected_ids:
                ContactUs.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
            return HttpResponseRedirect(reverse('contact-us'))


class ListSubscriptionsView(CustomListBaseView):
    model = Subscription
    context_fields = ['id','name','days','price']
    context_object_name = 'subscriptions'
    template_name = 'admin_panel/app/subscriptions.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

class CreateSubscriptionView(generic.CreateView):
    model = Subscription
    fields = ['name','days','price']
    template_name = 'admin_panel/app/subscription_form.html'
    success_url = '/dashboard/organization/subscriptions'

class SubscriptionInfoView(generic.UpdateView):
    model = Subscription
    fields = ['name','days','price']
    template_name = 'admin_panel/app/subscription_form.html'
    success_url = '/dashboard/organization/subscriptions'
    pk_url_kwarg = 'id'

class DeleteSubscriptionView(View):
    def post(self, request):
            selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
            if selected_ids:
                Subscription.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'تم حذف العناصر المحددة بنجاح')
            return HttpResponseRedirect(reverse('subscriptions'))
