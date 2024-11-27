from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# # Register your models here.




class CustomUserAdmin(UserAdmin):
    list_display = ['id','fullName','phonenumber','get_notifications']

    fieldsets = (
        (None, 
                {'fields':('phonenumber','email', 'password',)}
            ),
            ('User Information',
                {'fields':('fullName', 'image','user_type','get_notifications')}
            ),
            ('Registration', 
                {'fields':('last_login',)}
            )
    )


class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'phonenumber', 'code_type', 'code','createdAt','expiresAt','is_used']
    search_fields = ['phonenumber']


class ShareekAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user__fullName','user__phonenumber','job']
    search_fields = ['user__fullName']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user__fullName','user__phonenumber']
    search_fields = ['user__fullName']


class SupportChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_filter = ['user']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'content', 'createdAt']
    list_filter = ['chat', 'createdAt']
    search_fields = ['content']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'createdAt']
    list_filter = ['createdAt']
    search_fields = ['title', 'content']



class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'cost', 'duration']
    list_filter = ['duration']



class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__phonenumber', 'organization', 'content', 'createdAt']
    list_filter = ['user__phonenumber', 'organization', 'createdAt']
    search_fields = ['content']



admin.site.register(CustomUser)
admin.site.register(Client, ClientAdmin)
admin.site.register(Shareek, ShareekAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(OTPCode, OTPCodeAdmin)
admin.site.register(SupportChat, SupportChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Notification, NotificationAdmin)