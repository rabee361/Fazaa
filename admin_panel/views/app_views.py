from django.forms import BaseModelForm
from django.views import View , generic
from users.models import *
from base.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect , render
from utils.views import CustomListBaseView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
from django.db.models import Max
from utils.notifications import send_users_notification
from admin_panel.forms import NotificationForm
from django.core.paginator import Paginator

login_required_m =  method_decorator(login_required(login_url='login'), name="dispatch")


class SocialMediaSlugUrlView(View):
    def get(self,request,slug):
        try:
            social = SocialMediaUrl.objects.get(short_url=slug)
            assert social.active and social.url
            social.visits += 1
            social.save()
            return redirect(social.url) 
        except Exception as e:
            return render(request, '404.html', status=400)

class WebsiteSlugUrlView(View):
    def get(self,request,slug):
        try:
            organization = Organization.objects.get(website_short_url=slug)
            assert organization.website_short_url
            # organization.visits += 1
            # organization.save()
            return redirect(organization.website)
        except Exception as e:
            return render(request, '404.html', status=400)


class DeliverySlugUrlView(View):
    def get(self,request,slug):
        try:
            delivery = DeliveryCompanyUrl.objects.get(short_url=slug)
            assert delivery.active and delivery.url
            delivery.visits += 1
            delivery.save()
            return redirect(delivery.url)
        except Exception as e:
            return render(request, '404.html', status=400)


class CatalogSlugUrlView(View):
    def get(self,request,slug):
        try:
            catalog = Catalog.objects.get(short_url=slug)
            assert catalog.short_url
            catalog.visits += 1
            catalog.save()
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


class ListSupportChatsView(generic.ListView):
    model = SupportChat
    context_object_name = 'chats'
    template_name = 'admin_panel/app/chats.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user').annotate(last_message=Max('message__createdAt'))
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/chats_partial.html'
        if q:
            return queryset.filter(user__full_name__icontains=q)
        else:
            return queryset


class ListMessagesView(View):
    def get(self, request, chat_id):
        page = int(request.GET.get('page', 1))
        messages_per_page = 10  # Adjust this number as needed
        
        # Get the chat object
        chat = SupportChat.objects.select_related('user').get(id=chat_id)
        
        # Get all messages for this chat, ordered by newest first
        all_messages = Message.objects.filter(chat_id=chat_id).order_by('-createdAt')
        
        # Create paginator
        paginator = Paginator(all_messages, messages_per_page)
        messages = paginator.get_page(page)
        
        # Check if there are more messages
        has_next = messages.has_next()
        
        context = {
            'messages': messages,
            'has_next': has_next,
            'next_page': page + 1 if has_next else None,
            'chat_id': chat_id,
            'chat': chat,
            'is_htmx': request.htmx
        }
        
        return render(request, 'admin_panel/partials/messages_partial.html', context)


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
class SendNotificationView(View):
    def get(self, request): 
        form = NotificationForm()
        return render(request, 'admin_panel/notifications/send_notification.html', {'form': form})
    
    def post(self, request):
        form = NotificationForm(request.POST)
        if form.is_valid():
            recipient_type = form.cleaned_data['recipient_type']
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            recipient_type = form.cleaned_data['recipient_type']

            if recipient_type == 'all':
                send_users_notification(title,body,recipient_type)
            elif recipient_type == 'clients':
                send_users_notification(title,body,recipient_type)
            elif recipient_type == 'shareeks':
                send_users_notification(title,body,recipient_type)
            form.save()
            return HttpResponseRedirect(reverse('notifications'))
        
        return render(request, 'admin_panel/notifications/send_notification.html', {'form': form})


@login_required_m
class NotificationBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
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
class AboutUsView(CustomListBaseView):
    model = AboutUs
    context_object_name = 'about_us'
    context_fields = ['id','name','icon']
    template_name = 'admin_panel/app/about_us/about_us.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'admin_panel/partials/about_us_partial.html'
        if q:
            return queryset.filter(name__icontains=q)
        else:
            return queryset

@login_required_m
class CreateAboutUsView(generic.CreateView):
    model = AboutUs
    template_name = 'admin_panel/app/about_us/about_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/about-us'

@login_required_m
class UpdateAboutUsView(generic.UpdateView):
    model = AboutUs
    context_object_name = 'about_us'
    template_name = 'admin_panel/app/about_us/about_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/about-us'
    pk_url_kwarg = 'id'

@login_required_m
class AboutUsBulkActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            AboutUs.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('about-us'))







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

