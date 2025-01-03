from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# # Register your models here.




class CustomUserAdmin(UserAdmin):
    list_display = ['id','full_name','phonenumber','get_notifications']

    fieldsets = (
        (None, 
                {'fields':('phonenumber','email', 'password',)}
            ),
            ('User Information',
                {'fields':('full_name', 'image','user_type','get_notifications')}
            ),
            ('Registration', 
                {'fields':('last_login',)}
            )
    )


class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'phonenumber', 'code_type', 'code','createdAt','expiresAt','is_used']
    search_fields = ['phonenumber']


class ShareekAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user__full_name','user__phonenumber','job']
    search_fields = ['user__full_name']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user__full_name','user__phonenumber']
    search_fields = ['user__full_name']


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






admin.site.register(CustomUser)
admin.site.register(Client, ClientAdmin)
admin.site.register(Shareek, ShareekAdmin)
admin.site.register(OTPCode, OTPCodeAdmin)
admin.site.register(SupportChat, SupportChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Notification, NotificationAdmin)