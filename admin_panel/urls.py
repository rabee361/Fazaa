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

    path('<int:user_id>/change-password/' , user_views.ChangePasswordView.as_view() , name="change-password"),

    path('chats' , app_views.ListSupportChatsView.as_view() , name="chats"),
    path('<int:chat_id>/messages' , app_views.ListMessagesView.as_view() , name="messages"),
]


OrganizationPatterns=[
    path('types' , organization_views.ListOrganizationType.as_view() , name="organization-types"),
    path('types/add' , organization_views.CreateOrganizationType.as_view() , name="add-organization-type"),
    path('types/<int:id>/update' , organization_views.UpdateOrganizationType.as_view() , name="organization-type-info"),
    path('types/action' , organization_views.OrganizationTypesBulkActionView.as_view() ,name="organization-types-action"),

    path('organizations' , organization_views.ListOrganizationsView.as_view() , name="organizations"),
    path('organizations/<int:id>/info' , organization_views.OrganizationInfoView.as_view() , name="organization-info"),

    path('catalogs' , organization_views.ListCatalogsView.as_view() , name="catalogs"),
    path('catalogs/add/' , organization_views.CreateCatalogView.as_view() , name="add-catalog"),
    path('catalogs/<int:id>/info/' , organization_views.UpdateCatalogView.as_view() , name="catalog-info"),
    path('catalogs/action/' , organization_views.CatalogBulkActionView.as_view() , name="catalog-bulk-action"),

    path('images-gallery' , organization_views.ListImagesGalleryView.as_view() , name="images-gallery"),
    path('images-gallery/add/' , organization_views.CreateImageGalleryView.as_view() , name="add-image"),
    path('images-gallery/<int:id>/info/' , organization_views.UpdateImageGalleryView.as_view() , name="image-info"),
    path('images-gallery/action/' , organization_views.ImageGalleryBulkActionView.as_view() , name="image-gallery-bulk-action"),

    path('reels-gallery' , organization_views.ListReelsGalleryView.as_view() , name="reels-gallery"),
    path('reels-gallery/add/' , organization_views.CreateReelGalleryView.as_view() , name="add-reel"),
    path('reels-gallery/<int:id>/info/' , organization_views.UpdateReelGalleryView.as_view() , name="reel-info"),
    path('reels-gallery/action/' , organization_views.ReelGalleryBulkActionView.as_view() , name="reel-gallery-bulk-action"),

    path('social-media' , organization_views.ListSocialMedia.as_view() , name="social-media"),
    path('social-media/add' , organization_views.CreateSocialMedia.as_view() , name="add-social-media"),
    path('social-media/<int:id>/info' , organization_views.UpdateSocialMedia.as_view() , name="social-media-info"),
    path('social-media/action' , organization_views.SocialMediaActionView.as_view() , name="social-media-action"),

    path('delivery-companies' , organization_views.ListDeliveryCompanies.as_view() , name="delivery-companies"),
    path('delivery-companies/add/' , organization_views.CreateDeliveryCompany.as_view() , name="add-delivery-company"),
    path('delivery-companies/<int:id>/info/' , organization_views.UpdateDeliveryCompany.as_view() , name="delivery-company-info"),
    path('delivery-companies/action' , organization_views.DeliveryCompanyActionView.as_view() , name="delivery-company-action"),

    path('client-offers' , organization_views.ListClientOffers.as_view() , name="client-offers"),
    path('client-offers/add/' , organization_views.CreateClientOffer.as_view() , name="add-client-offer"),
    path('client-offers/<int:id>/update/' , organization_views.UpdateClientOffer.as_view() , name="client-offer-info"),
    path('client-offers/action/' , organization_views.ClientOfferBulkActionView.as_view() , name="client-offer-action"),

    path('service-offers' , organization_views.ListServiceOffers.as_view() , name="service-offers"),
    path('service-offers/add/' , organization_views.CreateServiceOffer.as_view() , name="add-service-offer"),
    path('service-offers/<int:id>/update/' , organization_views.UpdateServiceOffer.as_view() , name="service-offer-info"),
    path('service-offers/action/' , organization_views.ServiceOfferBulkActionView.as_view() , name="service-offer-action"),

    path('offer-templates' , organization_views.ListOfferTemplates.as_view() , name="offer-templates"),
    path('offer-templates/add/' , organization_views.CreateOfferTemplate.as_view() , name="add-offer-template"),
    path('offer-templates/<int:id>/info/' , organization_views.UpdateOfferTemplate.as_view() , name="offer-template-info"),
    path('offer-templates/delete/' , organization_views.DeleteOfferTemplate.as_view() , name="delete-offer-template"),

    path('delivery-links' , organization_views.ListDeliveryLinksView.as_view() , name="delivery-links"),
    path('delivery-links/add/' , organization_views.CreateDeliveryLinkView.as_view() , name="add-delivery-link"),
    path('delivery-links/<int:id>/info/' , organization_views.UpdateDeliveryLinkView.as_view() , name="delivery-link-info"),
    path('delivery-links/action/' , organization_views.DeliveryLinkBulkActionView.as_view() , name="delivery-bulk-action"),

    path('social-links' , organization_views.ListSocialLinksView.as_view() , name="social-links"),
    path('social-links/add' , organization_views.CreateSocialLinkView.as_view() , name="add-social-link"),
    path('social-links/<int:id>/info' , organization_views.UpdateSocialLinkView.as_view() , name="social-link-info"),
    path('social-links/action/' , organization_views.SocialUrlBulkActionView.as_view() , name="social-bulk-action"),

    path('branches' , organization_views.ListBranches.as_view() , name="branches"),
    path('branches/add/' , organization_views.CreateBranch.as_view() , name="add-branch"),
    path('branches/<int:id>/info/' , organization_views.UpdateBranch.as_view() , name="branch-info"),
    path('branches/action/' , organization_views.BranchActionView.as_view() , name="branch-action"),

    path('contact-us' , app_views.ContactUsView.as_view() , name="contact-us"),
    path('contact-us/add' , app_views.CreateContactUsView.as_view() , name="add-contact-us"),
    path('contact-us/<int:id>/info' , app_views.UpdateContactUsView.as_view() , name="contact-us-info"),
    path('contact-us/action/' , app_views.ContactUsBulkActionView.as_view() , name="contact-us-action"),

    path('about-us' , app_views.AboutUsView.as_view() , name="about-us"),
    path('about-us/add' , app_views.CreateAboutUsView.as_view() , name="add-about-us"),
    path('about-us/<int:id>/info' , app_views.UpdateAboutUsView.as_view() , name="about-us-info"),
    path('about-us/action/' , app_views.AboutUsBulkActionView.as_view() , name="about-us-action"),

    path('subscriptions' , app_views.ListSubscriptionsView.as_view() , name="subscriptions"),
    path('subscriptions/add' , app_views.CreateSubscriptionView.as_view() , name="add-subscription"),
    path('subscriptions/<int:id>/info' , app_views.SubscriptionInfoView.as_view() , name="subscription-info"),
    path('subscriptions/action/' , app_views.SubscriptionBulkActionView.as_view() , name="subscription-action"),

    path('reports' , app_views.ListReportsView.as_view() , name="reports"),
    path('reports/<int:id>/info' , app_views.GetReportView.as_view() , name="report-info"),
    path('reports/delete' , app_views.DeleteReportView.as_view() , name="delete-report"),

    path('terms/' , app_views.TermsView.as_view() , name="terms"),
    path('terms/<int:id>/info' , app_views.UpdateTermView.as_view() , name="term-info"),

    path('common-questions' , app_views.CommonQuestionsView.as_view() , name="common-questions"),
    path('common-questions/add' , app_views.CreateQuestionView.as_view() , name="add-common-question"),
    path('common-questions/<int:id>/info' , app_views.UpdateQuestionView.as_view() , name="common-question-info"),
    path('common-questions/action/' , app_views.CommonQuestionBulkActionView.as_view() , name="common-question-action"),

    path('notifications' , app_views.BaseNotificationsView.as_view() , name="notifications"),
    path('notifications/send/' , app_views.SendNotificationView.as_view() , name="send-notification"),
    path('notifications/action/' , app_views.NotificationBulkActionView.as_view() , name="notification-action"),
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
    # path('deep-link/<slug:slug>/' , app_views.OrganizationDeepLinkView.as_view()),
    path('delivery/<slug:slug>/' , app_views.DeliverySlugUrlView.as_view()),  
    path('branch/<slug:slug>/' , app_views.BranchSlugUrlView.as_view()),  
    path('404/' , app_views.handler404.as_view() , name="404"),
    path('500/' , app_views.handler500.as_view() , name="500"),
]
