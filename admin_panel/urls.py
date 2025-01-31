from django.urls import path , include
from .views import user_views , organization_views , app_views



UsersPatterns=[
    path('clients' , user_views.ListClientsView.as_view() , name="clients"),
    path('clients/add/' , user_views.CreateClientView.as_view() , name="add-client"),
    path('clients/<int:id>/info/' , user_views.ClientInfoView.as_view() , name="client-info"),
    path('clients/action/' , user_views.BulkActionView.as_view() , name="bulk-action"),

    path('shareek' , user_views.ListShareeksView.as_view() , name="shareeks"),
    path('shareek/add/' , user_views.CreateShareekView.as_view() , name="add-shareek"),
    path('shareek/<int:id>/update/' , user_views.ShareekInfoView.as_view() , name="shareek-info"),
    path('shareek/action/' , user_views.BulkActionView.as_view() , name="bulk-action"),

    path('admins' , user_views.ListAdminsView.as_view() , name="admins"),
    path('admins/add/' , user_views.CreateAdminView.as_view() , name="add-admin"),
    path('admins/<int:id>/info/' , user_views.AdminInfoView.as_view() , name="admin-info"),
    path('admins/action/' , user_views.BulkActionView.as_view() , name="bulk-action"),

    path('change-password/<int:user_id>/' , user_views.ChangePasswordView.as_view() , name="change-password"),

    path('bulk-action/', user_views.BulkActionView.as_view(), name="bulk-action"),
]


OrganizationPatterns=[
    path('types' , organization_views.ListOrganizationType.as_view() , name="organization-types"),
    path('types/add' , organization_views.CreateOrganizationType.as_view() , name="add-organization-type"),
    path('types/<int:id>/update' , organization_views.UpdateOrganizationType.as_view() , name="organization-type-info"),
    path('types/delete' , organization_views.DeleteOrganizationType.as_view() ,name="delete-organization-type"),

    path('organizations' , organization_views.ListOrganizationsView.as_view() , name="organizations"),
    # path('organizations/add' , organization_views.CreateOrganizationView.as_view() , name="add-organization"),
    path('organizations/<int:id>/info' , organization_views.OrganizationInfoView.as_view() , name="organization-info"),
    # path('organizations/delete' , organization_views.DeleteOrganizationView.as_view() , name="delete-organization"),

    path('catalogs' , organization_views.ListCatalogsView.as_view() , name="catalogs"),
    path('catalogs/add/' , organization_views.CreateCatalogView.as_view() , name="add-catalog"),
    path('catalogs/<int:id>/info/' , organization_views.UpdateCatalogView.as_view() , name="catalog-info"),
    path('catalogs/delete/' , organization_views.DeleteCatalogView.as_view() , name="delete-catalog"),

    path('social-media' , organization_views.ListSocialMedia.as_view() , name="social-media"),
    path('social-media/add' , organization_views.CreateSocialMedia.as_view() , name="add-social-media"),
    path('social-media/<int:id>/info' , organization_views.UpdateSocialMedia.as_view() , name="social-media-info"),
    path('social-media/delete' , organization_views.DeleteSocialMedia.as_view() , name="delete-social-media"),

    path('delivery-companies' , organization_views.ListDeliveryCompanies.as_view() , name="delivery-companies"),
    path('delivery-companies/add/' , organization_views.CreateDeliveryCompany.as_view() , name="add-delivery-company"),
    path('delivery-companies/<int:id>/info/' , organization_views.UpdateDeliveryCompany.as_view() , name="delivery-company-info"),
    path('delivery-companies/delete/' , organization_views.DeleteDeliveryCompany.as_view() , name="delete-delivery-company"),

    path('client-offers' , organization_views.ListClientOffers.as_view() , name="client-offers"),
    path('client-offers/add/' , organization_views.CreateClientOffer.as_view() , name="add-client-offer"),
    path('client-offers/<int:id>/update/' , organization_views.UpdateClientOffer.as_view() , name="client-offer-info"),
    path('client-offers/delete/' , organization_views.DeleteClientOffer.as_view() , name="delete-client-offer"),

    path('service-offers' , organization_views.ListServiceOffers.as_view() , name="service-offers"),
    path('service-offers/add/' , organization_views.CreateServiceOffer.as_view() , name="add-service-offer"),
    path('service-offers/<int:id>/update/' , organization_views.UpdateServiceOffer.as_view() , name="service-offer-info"),
    path('service-offers/delete/' , organization_views.DeleteServiceOffer.as_view() , name="delete-service-offer"),

    path('delivery-links' , organization_views.ListDeliveryLinksView.as_view() , name="delivery-links"),
    path('delivery-links/add/' , organization_views.CreateDeliveryLinkView.as_view() , name="add-delivery-link"),
    path('delivery-links/<int:id>/info/' , organization_views.UpdateDeliveryLinkView.as_view() , name="delivery-link-info"),
    path('delivery-links/delete/' , organization_views.DeleteDeliveryLinkView.as_view() , name="delete-delivery-link"),

    path('social-links' , organization_views.ListSocialLinksView.as_view() , name="social-links"),
    path('social-links/add' , organization_views.CreateSocialLinkView.as_view() , name="add-social-link"),
    path('social-links/<int:id>/info' , organization_views.UpdateSocialLinkView.as_view() , name="social-link-info"),
    path('social-links/delete' , organization_views.DeleteSocialLinkView.as_view() , name="delete-social-link"),

    # path('organization/<int:id>/branches/' , organization_views.ListBranches.as_view() , name="branches"),
    # path('organization/<int:id>/branches/create/' , organization_views.CreateBranch.as_view() , name="create-branch"),
    # path('organization/<int:id>/branches/<int:id>/update/' , organization_views.UpdateBranch.as_view() , name="update-branch"),
    # path('organization/<int:id>/branches/<int:id>/delete/' , organization_views.DeleteBranch.as_view() , name="delete-branch"),

    path('contact-us' , app_views.ContactUsView.as_view() , name="contact-us"),
    path('contact-us/add' , app_views.CreateContactUsView.as_view() , name="add-contact-us"),
    path('contact-us/<int:id>/info' , app_views.UpdateContactUsView.as_view() , name="contact-us-info"),
    path('contact-us/delete' , app_views.DeleteContactUsView.as_view() , name="delete-contact-us"),

    path('subscriptions' , app_views.ListSubscriptionsView.as_view() , name="subscriptions"),
    path('subscriptions/add' , app_views.CreateSubscriptionView.as_view() , name="add-subscription"),
    path('subscriptions/<int:id>/info' , app_views.SubscriptionInfoView.as_view() , name="subscription-info"),
    path('subscriptions/delete' , app_views.DeleteSubscriptionView.as_view() , name="delete-subscription"),

    path('reports' , app_views.ListReportsView.as_view() , name="reports"),
    path('reports/<int:id>/info' , app_views.GetReportView.as_view() , name="report-info"),
    path('reports/delete' , app_views.DeleteReportView.as_view() , name="delete-report"),

    path('chats' , app_views.ListSupportChatsView.as_view() , name="chats"),
    path('<int:chat_id>/messages' , app_views.ListMessagesView.as_view() , name="messages"),

    path('common-questions' , app_views.CommonQuestionsView.as_view() , name="common-questions"),
    path('common-questions/add' , app_views.CreateQuestionView.as_view() , name="add-common-question"),
    path('common-questions/<int:id>/info' , app_views.UpdateQuestionView.as_view() , name="common-question-info"),
    path('common-questions/delete' , app_views.DeleteQuestionView.as_view() , name="delete-common-question"),

    path('notifications' , app_views.BaseNotificationsView.as_view() , name="notifications"),
    path('notifications/send/' , app_views.SendNotificationView.as_view() , name="send-notification"),
    path('notifications/delete/' , app_views.DeleteNotificationView.as_view() , name="delete-notification"),
]



DashboardPatterns = [
    path('' , user_views.DashboardView.as_view() , name="dashboard"),
    path('partial/' , user_views.DashboardPartialView.as_view() , name="dashboard-partial"),
    path('users/' , include(UsersPatterns)),
    path('organization/' , include(OrganizationPatterns)),
]


urlpatterns = [
    path('login/' , user_views.LoginView.as_view() , name="login"),
    path('logout/' , user_views.LogoutView.as_view() , name="logout"),
    path('dashboard/' , include(DashboardPatterns)),
    path('card/<slug:slug>/' , organization_views.CardUrlView.as_view() , name="card-url"),
    path('catalog/<slug:slug>/' , app_views.CatalogSlugUrlView.as_view()),
    path('social/<slug:slug>/' , app_views.SocialMediaSlugUrlView.as_view()),
    path('website/<slug:slug>/' , app_views.WebsiteSlugUrlView.as_view()),
    path('delivery/<slug:slug>/' , app_views.DeliverySlugUrlView.as_view()),  
    path('404/' , app_views.handler404.as_view() , name="404"),
    path('500/' , app_views.handler500.as_view() , name="500"),
]
