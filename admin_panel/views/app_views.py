from django.views import View, generic
from users.models import *
from base.models import *
from django.shortcuts import redirect , render
from utils.views import CustomListBaseView
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django.db.models import Max
from utils.notifications import send_users_notification
from admin_panel.forms import NotificationForm
from django.core.paginator import Paginator
from utils.views import BaseView


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


class OrganizationUrlInfoView(View):
    def get(self,request,slug):
        try:
            organization = Organization.objects.get(org_short_url=slug)
            social_urls = SocialMediaUrl.objects.filter(organization=organization)
            offers = ClientOffer.objects.filter(organization=organization)
            catalogs = Catalog.objects.filter(organization=organization)
            gallery = ImageGallery.objects.filter(organization=organization)[:3]
            delivery_companies = DeliveryCompanyUrl.objects.filter(organization=organization)
            context = {
                'organization': organization,
                'social_urls': social_urls,
                'website_url': request.build_absolute_uri(organization.get_absolute_website_url()),
                'card_url': request.build_absolute_uri(organization.get_absolute_card_url()),
                'offers': offers,
                'catalogs': catalogs,
                'gallery': gallery,
                'delivery_companies': delivery_companies
            }
            return render(request, 'admin_panel/profile.html', context=context)
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


class BranchSlugUrlView(View):
    def get(self,request,slug):
        try:
            branch = Branch.objects.get(short_url=slug)
            assert branch.short_url
            branch.visits += 1
            branch.save()
            base_url = "https://www.google.com/maps"
            if branch.location:
                return redirect(f"{base_url}?q={branch.location.x},{branch.location.y}")
            else:
                return redirect(branch.organization.website)
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

class ClientOfferUrlView(View):
    def get(self,request,slug):
        try:
            offer = ClientOffer.objects.get(short_url=slug)
            organization = Organization.objects.get(id=offer.organization.id)
            offers = ClientOffer.objects.filter(organization=organization)
            socials = SocialMediaUrl.objects.filter(organization=organization)
            context = {
                'offer': offer,
                'organization':organization,
                'website_url': request.build_absolute_uri(organization.get_absolute_website_url()),
                'card_url': request.build_absolute_uri(organization.get_absolute_card_url()),
                'offers':offers,
                'socials':socials
            }
            return render(request, 'admin_panel/client_offer.html', context=context)
        except Exception as e:
            return render(request, '404.html', status=400)
        

class ServiceOfferUrlView(View):
    def get(self,request,slug):
        try:
            offer = ServiceOffer.objects.get(short_url=slug)
            context = {
                'offer': offer
            }
            return render(request, 'admin_panel/service_offer.html', context=context)
        except Exception as e:
            return render(request, '404.html', status=400)
        
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


class GetReportView(BaseView, generic.UpdateView):
    model = Report
    context_object_name = 'report'
    template_name = 'admin_panel/app/reports/report_form.html'
    pk_url_kwarg = 'id'
    fields = ['client','organization','content']
    success_url = '/dashboard/organization/reports'


class DeleteReportView(BaseView):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        if selected_ids:
            Report.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('reports'))


class ListSupportChatsView(BaseView, generic.ListView):
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


class ListMessagesView(BaseView):
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
        

class CreateQuestionView(BaseView, generic.CreateView):
    model = CommonQuestion
    fields = ['question','answer']
    template_name = 'admin_panel/app/common_questions/common_question_form.html'
    success_url = '/dashboard/organization/common-questions'


class UpdateQuestionView(BaseView, generic.UpdateView):
    model = CommonQuestion
    fields = ['question','answer']
    template_name = 'admin_panel/app/common_questions/common_question_form.html'
    success_url = '/dashboard/organization/common-questions'
    pk_url_kwarg = 'id'


class CommonQuestionBulkActionView(BaseView):
    def post(self, request):    
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            CommonQuestion.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('common-questions'))



class BaseNotificationsView(CustomListBaseView):
    model = Notification
    context_object_name = 'notifications'
    context_fields = ['id','title','createdAt']
    template_name = 'admin_panel/notifications/notifications.html'



class SendNotificationView(BaseView):
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



class NotificationBulkActionView(BaseView):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            Notification.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('notifications'))



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


class CreateContactUsView(BaseView, generic.CreateView):
    model = ContactUs
    template_name = 'admin_panel/app/contact_us/contact_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/contact-us'


class UpdateContactUsView(BaseView, generic.UpdateView):
    model = ContactUs
    context_object_name = 'contact_us'
    template_name = 'admin_panel/app/contact_us/contact_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/contact-us'
    pk_url_kwarg = 'id'

    def get_context_data(self):
        context = super().get_context_data()
        context['icon'] = self.object.icon
        return context


class ContactUsBulkActionView(BaseView):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            ContactUs.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('contact-us'))




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


class CreateAboutUsView(BaseView, generic.CreateView):
    model = AboutUs
    template_name = 'admin_panel/app/about_us/about_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/about-us'


class UpdateAboutUsView(BaseView, generic.UpdateView):
    model = AboutUs
    context_object_name = 'about_us'
    template_name = 'admin_panel/app/about_us/about_us_form.html'
    fields = ['name','link','icon']
    success_url = '/dashboard/organization/about-us'
    pk_url_kwarg = 'id'


class AboutUsBulkActionView(BaseView):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            AboutUs.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('about-us'))








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



class CreateSubscriptionView(BaseView, generic.CreateView):
    model = Subscription
    fields = ['name','days','price']
    template_name = 'admin_panel/app/subscription_form.html'
    success_url = '/dashboard/organization/subscriptions'


class SubscriptionInfoView(BaseView, generic.UpdateView):
    model = Subscription
    fields = ['name','days','price']
    template_name = 'admin_panel/app/subscription_form.html'
    success_url = '/dashboard/organization/subscriptions'
    pk_url_kwarg = 'id'


class SubscriptionBulkActionView(BaseView):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids', '[]'))
        action = request.POST.get('action')
        if action == 'delete':
            Subscription.objects.filter(id__in=selected_ids).delete()
        return HttpResponseRedirect(reverse('subscriptions'))



class TermsView(CustomListBaseView):
    model = TermsPrivacy
    context_object_name = 'terms'
    context_fields = ['id','title','content']
    template_name = 'admin_panel/app/terms/terms.html'
    

class UpdateTermView(BaseView, generic.UpdateView):
    model = TermsPrivacy
    fields = ['title','content']
    template_name = 'admin_panel/app/terms/term_form.html'
    success_url = '/dashboard/organization/terms'
    pk_url_kwarg = 'id'
 

class handler404(BaseView):
    def get(self, request):
        return render(request, '404.html')

class handler500(BaseView):
    def get(self, request):
        return render(request, '500.html')

