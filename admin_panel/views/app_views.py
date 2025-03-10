from django.views import View , generic
from users.models import *
from base.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect , render
from utils.views import CustomListBaseView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django.db.models import Max

login_required_m =  method_decorator(login_required, name="dispatch")


class SocialMediaSlugUrlView(View):
    def get(self,request,slug):
        try:
            social = SocialMediaUrl.objects.get(short_url=slug)
            assert social.active and social.url
            return redirect(social.url) 
        except Exception as e:
            return render(request, '404.html', status=400)

class WebsiteSlugUrlView(View):
    def get(self,request,slug):
        try:
            organization = Organization.objects.get(website_short_url=slug)
            assert organization.website_short_url
            return redirect(organization.website)
        except Exception as e:
            return render(request, '404.html', status=400)


class DeliverySlugUrlView(View):
    def get(self,request,slug):
        try:
            delivery = DeliveryCompanyUrl.objects.get(short_url=slug)
            assert delivery.active and delivery.url
            return redirect(delivery.url)
        except Exception as e:
            return render(request, '404.html', status=400)


class CatalogSlugUrlView(View):
    def get(self,request,slug):
        try:
            catalog = Catalog.objects.get(short_url=slug)
            assert catalog.short_url
            return redirect(catalog.file.url)
        except Exception as e:
            return render(request, '404.html', status=400)


@login_required_m
class ListReportsView(CustomListBaseView):
    model = Report
    context_object_name = 'reports'
    context_fields = ['id','organization','client','createdAt']
    template_name = 'admin_panel/app/reports/reports.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(organization__name__icontains=search_query)
        return queryset

@login_required_m
class GetReportView(generic.UpdateView):
    model = Report
    context_object_name = 'report'
    template_name = 'admin_panel/app/reports/report_form.html'
    pk_url_kwarg = 'id'
    fields = ['client','organization','content']
    success_url = '/dashboard/organization/reports'

@login_required_m
class DeleteReportView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            Report.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('reports'))


class ListSupportChatsView(View):
    def get(self, request):
        chats = SupportChat.objects.select_related('user').annotate(last_message=Max('message__createdAt')).all()
        context = {
            'chats': chats,
        }
        return render(request, 'admin_panel/app/chats.html' , context=context)


class ListMessagesView(View):
    def get(self,request,chat_id):
        messages = Message.objects.filter(chat_id=chat_id)
        return 

@login_required_m
class CommonQuestionsView(CustomListBaseView):
    model = CommonQuestion
    context_object_name = 'common_questions'   
    context_fields = ['id','question']
    template_name = 'admin_panel/app/common_questions/common_questions.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/common_questions_partial.html'
        if q:
            return queryset.filter(question__icontains=q)
        else:
            return queryset
        
@login_required_m
class CreateQuestionView(generic.CreateView):
    model = CommonQuestion
    fields = ['question','answer']
    template_name = 'admin_panel/app/common_questions/common_question_form.html'
    success_url = '/dashboard/organization/common-questions'

@login_required_m
class UpdateQuestionView(generic.UpdateView):
    model = CommonQuestion
    fields = ['question','answer']
    template_name = 'admin_panel/app/common_questions/common_question_form.html'
    success_url = '/dashboard/organization/common-questions'
    pk_url_kwarg = 'id'

@login_required_m
class CommonQuestionBulkActionView(View):
    def post(self, request):    
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            CommonQuestion.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('common-questions'))


@login_required_m
class BaseNotificationsView(CustomListBaseView):
    model = Notification
    context_object_name = 'notifications'
    context_fields = ['id','title','createdAt']
    template_name = 'admin_panel/notifications/notifications.html'


@login_required_m
class SendNotificationView(generic.CreateView):
    model = Notification
    template_name = 'admin_panel/notifications/send_notification.html'
    fields = ['title','body']
    success_url = '/dashboard/organization/notifications'


@login_required_m
class DeleteNotificationView(View):
    def post(self, request):
            selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
            if selected_ids:
                Notification.objects.filter(id__in=selected_ids).delete()
            return HttpResponseRedirect(reverse('notifications'))


@login_required_m
class ContactUsView(CustomListBaseView):
    model = ContactUs
    context_object_name = 'contact_us'
    context_fields = ['id','name','icon']
    template_name = 'admin_panel/app/contact_us/contact_us.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/contact_us_partial.html'
        if q:
            return queryset.filter(name__icontains=q)
        else:
            return queryset

@login_required_m
class CreateContactUsView(generic.CreateView):
    model = ContactUs
    template_name = 'admin_panel/app/contact_us/contact_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/contact-us'

@login_required_m
class UpdateContactUsView(generic.UpdateView):
    model = ContactUs
    context_object_name = 'contact_us'
    template_name = 'admin_panel/app/contact_us/contact_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/contact-us'
    pk_url_kwarg = 'id'

@login_required_m
class ContactUsBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            ContactUs.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('contact-us'))


@login_required_m
class ListSubscriptionsView(CustomListBaseView):
    model = Subscription
    context_fields = ['id','name','days','price']
    context_object_name = 'subscriptions'
    template_name = 'admin_panel/app/subscriptions.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/subscriptions_partial.html'
        if q:
            return queryset.filter(name__icontains=q)
        else:
            return queryset

@login_required_m
class CreateSubscriptionView(generic.CreateView):
    model = Subscription
    fields = ['name','days','price']
    template_name = 'admin_panel/app/subscription_form.html'
    success_url = '/dashboard/organization/subscriptions'

@login_required_m
class SubscriptionInfoView(generic.UpdateView):
    model = Subscription
    fields = ['name','days','price']
    template_name = 'admin_panel/app/subscription_form.html'
    success_url = '/dashboard/organization/subscriptions'
    pk_url_kwarg = 'id'

@login_required_m
class SubscriptionBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            Subscription.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('subscriptions'))


class handler404(View):
    def get(self, request):
        return render(request, '404.html')

class handler500(View):
    def get(self, request):
        return render(request, '500.html')

