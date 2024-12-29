from django.urls import path , include
from .views import user_views , organization_views , app_views



UsersPatterns=[
    path('clients/' , user_views.ListClientsView.as_view() , name="clients"),
    path('clients/add/' , user_views.CreateClientView.as_view() , name="add-client"),
    path('clients/<int:id>/info/' , user_views.ClientInfoView.as_view() , name="client-info"),
    path('clients/delete/' , user_views.DeleteClientView.as_view() , name="delete-client"),

    path('shareek/' , user_views.ListShareeksView.as_view() , name="shareeks"),
    path('shareek/add/' , user_views.CreateShareekView.as_view() , name="add-shareek"),
    path('shareek/<int:id>/update/' , user_views.UpdateShareekView.as_view() , name="shareek-info"),
    path('shareek/delete/' , user_views.DeleteShareekView.as_view() , name="delete-shareek"),

    path('admins/' , user_views.ListAdminsView.as_view() , name="admins"),
    path('admins/add/' , user_views.CreateAdminView.as_view() , name="add-admin"),
    path('admins/<int:id>/info/' , user_views.UpdateAdminView.as_view() , name="admin-info"),
    path('admins/delete/' , user_views.DeleteAdminView.as_view() , name="delete-admin"),

#     path('subscriptions/' , user_views.ListSubscriptions.as_view() , name="subscriptions"),
#     path('subscriptions/create/' , user_views.CreateSubscription.as_view() , name="create-subscription"),
#     path('subscriptions/<int:id>/update/' , user_views.UpdateSubscription.as_view() , name="update-subscription"),
#     path('subscriptions/<int:id>/delete/' , user_views.DeleteSubscription.as_view() , name="delete-subscription"),
]


OrganizationPatterns=[
    path('types' , organization_views.ListOrganizationType.as_view() , name="organization-types"),
    path('types/add' , organization_views.CreateOrganizationType.as_view() , name="add-organization-type"),
    path('types/<int:id>/update' , organization_views.UpdateOrganizationType.as_view() , name="organization-type-info"),
    path('types/delete' , organization_views.DeleteOrganizationType.as_view() ,name="delete-organization-type"),

    path('catalogs' , organization_views.ListCatalogsView.as_view() , name="catalogs"),
    path('catalogs/add/' , organization_views.CreateCatalogView.as_view() , name="add-catalog"),
    path('catalogs/<int:id>/info/' , organization_views.UpdateCatalogView.as_view() , name="catalog-info"),
    path('catalogs/delete/' , organization_views.DeleteCatalogView.as_view() , name="delete-catalog"),

    path('social-media' , organization_views.ListSocialMedia.as_view() , name="social-media"),
    path('social-media/add' , organization_views.CreateSocialMedia.as_view() , name="add-social-media"),
    path('social-media/<int:id>/info' , organization_views.UpdateSocialMedia.as_view() , name="social-media-info"),
    path('social-media/<int:id>/delete' , organization_views.DeleteSocialMedia.as_view() , name="delete-social-media"),

    # path('organization/<int:id>/social-links/' , organization_views.ListSocialMediaLinks.as_view() , name="social-links"),
    # path('organization/<int:id>/social-links/create/' , organization_views.CreateSocialMediaLink.as_view() , name="create-social-link"),
    # path('organization/<int:id>/social-links/<int:link_id>/update/' , organization_views.UpdateSocialMediaLink.as_view() , name="update-social-link"),
    # path('organization/<int:id>/social-links/<int:link_id>/delete/' , organization_views.DeleteSocialMediaLink.as_view() , name="delete-social-link"),

    path('delivery-companies' , organization_views.ListDeliveryCompanies.as_view() , name="delivery-companies"),
    path('delivery-companies/create/' , organization_views.CreateDeliveryCompany.as_view() , name="create-delivery-company"),
    path('delivery-companies/<int:id>/info/' , organization_views.UpdateDeliveryCompany.as_view() , name="delivery-company-info"),
    path('delivery-companies/<int:id>/delete/' , organization_views.DeleteDeliveryCompany.as_view() , name="delete-delivery-company"),

    path('client-offers' , organization_views.ListClientOffers.as_view() , name="client-offers"),
    path('client-offers/add/' , organization_views.CreateClientOffer.as_view() , name="add-client-offer"),
    path('client-offers/<int:id>/update/' , organization_views.UpdateClientOffer.as_view() , name="client-offer-info"),
    path('client-offers/<int:id>/delete/' , organization_views.DeleteClientOffer.as_view() , name="delete-client-offer"),

    path('service-offers' , organization_views.ListServiceOffers.as_view() , name="service-offers"),
    path('service-offers/add/' , organization_views.CreateServiceOffer.as_view() , name="add-service-offer"),
    path('service-offers/<int:id>/update/' , organization_views.UpdateServiceOffer.as_view() , name="service-offer-info"),
    path('service-offers/<int:id>/delete/' , organization_views.DeleteServiceOffer.as_view() , name="delete-service-offer"),

    # path('organization/<int:id>/delivery-links/' , organization_views.ListDeliveryLinks.as_view() , name="delivery-links"),
    # path('organization/<int:id>/delivery-links/create/' , organization_views.CreateDeliveryCompanyLink.as_view() , name="create-delivery-link"),
    # path('organization/<int:id>/delivery-links/<int:id>/update/' , organization_views.UpdateDeliveryCompanyLink.as_view() , name="update-delivery-link"),
    # path('organization/<int:id>/delivery-links/<int:id>/delete/' , organization_views.DeleteDeliveryCompanyLink.as_view() , name="delete-delivery-link"),

    # path('organization/<int:id>/branches/' , organization_views.ListBranches.as_view() , name="branches"),
    # path('organization/<int:id>/branches/create/' , organization_views.CreateBranch.as_view() , name="create-branch"),
    # path('organization/<int:id>/branches/<int:id>/update/' , organization_views.UpdateBranch.as_view() , name="update-branch"),
    # path('organization/<int:id>/branches/<int:id>/delete/' , organization_views.DeleteBranch.as_view() , name="delete-branch"),

    path('about' , app_views.AboutUsView.as_view() , name="about-us"),
    path('about/update/' , app_views.UpdateAboutUsView.as_view() , name="update-about"),

    path('reports' , app_views.ListReportsView.as_view() , name="reports"),
    path('reports/<int:id>' , app_views.GetReportView.as_view() , name="get-report"),
    path('reports/<int:id>/delete' , app_views.DeleteReportView.as_view() , name="delete-report"),

    path('common-questions' , app_views.CommonQuestionsView.as_view() , name="common-questions"),
    path('common-questions/create' , app_views.CreateQuestionView.as_view() , name="create-common-question"),
    path('common-questions/<int:id>/delete' , app_views.DeleteQuestionView.as_view() , name="delete-common-question"),
    path('common-questions/<int:id>/update' , app_views.UpdateQuestionView.as_view() , name="update-common-question"),

    path('notifications' , app_views.BaseNotificationsView.as_view() , name="notifications"),
    path('notifications/send/' , app_views.SendNotificationView.as_view() , name="send-notification"),
    path('notifications/delete/' , app_views.DeleteNotificationView.as_view() , name="delete-notification"),
]



DashboardPatterns = [
    path('' , user_views.DashboardView.as_view() , name="dashboard"),
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
]
