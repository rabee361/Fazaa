from django.urls import path , include
from .views import user_views , organization_views , app_views



# UsersPatterns=[
#     path('clients/' , user_views.ListClients.as_view() , name="clients"),
#     path('clients/create/' , user_views.CreateClient.as_view() , name="create-client"),
#     path('clients/<int:id>/update/' , user_views.UpdateClient.as_view() , name="update-client"),
#     path('clients/<int:id>/delete/' , user_views.DeleteClient.as_view() , name="delete-client"),
#     path('clients/<int:id>/' , user_views.GetClient.as_view() , name="get-client"),

#     path('shareek/' , user_views.ListShareeks.as_view() , name="shareeks"),
#     path('shareek/create/' , user_views.CreateShareek.as_view() , name="create-shareek"),
#     path('shareek/<int:id>/update/' , user_views.UpdateShareek.as_view() , name="update-shareek"),
#     path('shareek/<int:id>/delete/' , user_views.DeleteShareek.as_view() , name="delete-shareek"),
#     path('shareek/<int:id>/' , user_views.GetShareek.as_view() , name="get-shareek"),

#     path('admins/' , user_views.ListAdmins.as_view() , name="admins"),
#     path('admins/create/' , user_views.CreateAdmin.as_view() , name="create-admin"),
#     path('admins/<int:id>/update/' , user_views.UpdateAdmin.as_view() , name="update-admin"),
#     path('admins/<int:id>/delete/' , user_views.DeleteAdmin.as_view() , name="delete-admin"),
#     path('admins/<int:id>/' , user_views.GetAdmin.as_view() , name="get-admin"),

#     path('subscriptions/' , user_views.ListSubscriptions.as_view() , name="subscriptions"),
#     path('subscriptions/create/' , user_views.CreateSubscription.as_view() , name="create-subscription"),
#     path('subscriptions/<int:id>/update/' , user_views.UpdateSubscription.as_view() , name="update-subscription"),
#     path('subscriptions/<int:id>/delete/' , user_views.DeleteSubscription.as_view() , name="delete-subscription"),
#     path('subscriptions/<int:id>/' , user_views.GetSubscription.as_view() , name="get-subscription"),
# ]


OrganizationPatterns=[
    path('types/' , organization_views.ListOrganizationType.as_view() , name="organization-types"),
    path('types/create/' , organization_views.CreateOrganizationType.as_view() , name="create-organization-type"),
    path('types/<int:id>/update/' , organization_views.UpdateOrganizationType.as_view() , name="update-organization-type"),
    path('types/<int:id>/delete/' , organization_views.DeleteOrganizationType.as_view() ,name="delete-organization-type"),

    # path('social-media/' , organization_views.ListSocialMedia.as_view() , name="social-media"),
    # path('social-media/create/' , organization_views.CreateSocialMedia.as_view() , name="create-social-media"),
    # path('social-media/<int:id>/update/' , organization_views.UpdateSocialMedia.as_view() , name="update-social-media"),
    # path('social-media/<int:id>/delete/' , organization_views.DeleteSocialMedia.as_view() , name="delete-social-media"),

    # path('organization/<int:id>/social-links/' , organization_views.ListSocialMediaLinks.as_view() , name="social-links"),
    # path('organization/<int:id>/social-links/create/' , organization_views.CreateSocialMediaLink.as_view() , name="create-social-link"),
    # path('organization/<int:id>/social-links/<int:link_id>/update/' , organization_views.UpdateSocialMediaLink.as_view() , name="update-social-link"),
    # path('organization/<int:id>/social-links/<int:link_id>/delete/' , organization_views.DeleteSocialMediaLink.as_view() , name="delete-social-link"),

    # path('delivery-companies/' , organization_views.ListDeliveryCompanies.as_view() , name="delivery-companies"),
    # path('delivery-companies/create/' , organization_views.CreateDeliveryCompany.as_view() , name="create-delivery-company"),
    # path('delivery-companies/<int:id>/update/' , organization_views.UpdateDeliveryCompany.as_view() , name="update-delivery-company"),
    # path('delivery-companies/<int:id>/delete/' , organization_views.DeleteDeliveryCompany.as_view() , name="delete-delivery-company"),

    # path('organization/<int:id>/delivery-links/' , organization_views.ListDeliveryLinks.as_view() , name="delivery-links"),
    # path('organization/<int:id>/delivery-links/create/' , organization_views.CreateDeliveryCompanyLink.as_view() , name="create-delivery-link"),
    # path('organization/<int:id>/delivery-links/<int:id>/update/' , organization_views.UpdateDeliveryCompanyLink.as_view() , name="update-delivery-link"),
    # path('organization/<int:id>/delivery-links/<int:id>/delete/' , organization_views.DeleteDeliveryCompanyLink.as_view() , name="delete-delivery-link"),

    # path('organization/<int:id>/branches/' , organization_views.ListBranches.as_view() , name="branches"),
    # path('organization/<int:id>/branches/create/' , organization_views.CreateBranch.as_view() , name="create-branch"),
    # path('organization/<int:id>/branches/<int:id>/update/' , organization_views.UpdateBranch.as_view() , name="update-branch"),
    # path('organization/<int:id>/branches/<int:id>/delete/' , organization_views.DeleteBranch.as_view() , name="delete-branch"),

    # path('reports/' , app_views.ListReportsView.as_view() , name="reports"),
    # path('reports/<int:id>' , app_views.GetReportView.as_view() , name="get-report"),
    # path('reports/<int:id>/delete' , app_views.DeleteReportView.as_view() , name="delete-report"),

    # path('common-questions/' , app_views.CommonQuestionsView.as_view() , name="common-questions"),
    # path('common-questions/create' , app_views.CreateQuestionView.as_view() , name="create-common-question"),
    # path('common-questions/<int:id>/delete' , app_views.DeleteQuestionView.as_view() , name="delete-common-question"),
    # path('common-questions/<int:id>/update' , app_views.UpdateQuestionView.as_view() , name="update-common-question"),

    # path('notifications/' , app_views.NotificationsView.as_view() , name="notifications"),
    # path('notification/send/' , )


]



urlpatterns = [
    path('auth/login/' , user_views.LoginView.as_view() , name="login"),
    path('auth/logout/' , user_views.LogoutView.as_view() , name="logout"),
    # path('users/',include(UsersPatterns)),
    path('organization/',include(OrganizationPatterns)),
]
