from django.urls import path
from .views import shareek , client , common


urlpatterns = [
    path('shareek/organization/types' , shareek.OrganizationTypes.as_view()),
    path('shareek/organization/<int:id>/delete' , shareek.DeleteOrganizationView.as_view()),
    path('shareek/organization/<int:id>/update/' , shareek.UpdateOrganizationView.as_view()),
    path('shareek/organizations' , shareek.OrganizationsListView.as_view()),
    path('shareek/organization/<int:id>/info/' , shareek.OrganizationInfoView.as_view()),   
    path('shareek/organization/<int:pk>/' , shareek.GetOrganizationView.as_view()),
    path('shareek/organization/<int:pk>/logo/update/' , shareek.UpdateOrganizationLogoView.as_view()),
    path('shareek/organization/<int:pk>/offers/available/' , shareek.AvailableOffersView.as_view()),

    path('shareek/organization/<int:pk>/social-url/' , shareek.SocialMediaUrlView.as_view()),
    path('shareek/organization/social-urls/<int:pk>/update/' , shareek.UpdateSocialMediaUrlView.as_view()),
    path('v2/shareek/organization/social-urls/update/' , shareek.UpdateBulkSocialMediaUrlView.as_view()),

    path('shareek/organization/<int:pk>/delivery-url/' , shareek.DeliveryUrlView.as_view()),
    path('shareek/organization/delivery-url/<int:pk>/update/' , shareek.UpdateDeliveryUrlView.as_view()),
    # path('v2/shareek/organization/social-urls/update/' , shareek.UpdateBulkDeliveryMediaUrlView.as_view()),

    path('shareek/organization/<int:id>/reels/' , shareek.ReelsView.as_view()),
    path('shareek/organization/reels/create/' , shareek.CreateReelsView.as_view()),
    path('shareek/organization/reels/<int:id>/delete/' , shareek.DeleteReelsView.as_view()),

    path('shareek/organization/<int:id>/gallery/' , shareek.GalleryView.as_view()),
    path('shareek/organization/gallery/create/' , shareek.CreateGalleryView.as_view()),
    path('shareek/organization/gallery/<int:id>/delete/' , shareek.DeleteGalleryView.as_view()),

    path('shareek/organization/<int:id>/catalogs/' , shareek.CatalogView().as_view()),
    path('shareek/organization/catalogs/create/' , shareek.CreateCatalogView.as_view()),
    path('shareek/organization/catalog/<int:id>/delete/' , shareek.DeleteCatalogView.as_view()),

    path('shareek/organization/<int:id>/client-offers/' , shareek.ClientOfferView.as_view()),
    path('shareek/organization/client-offers/create/' , shareek.CreateClientOffer.as_view()),
    path('shareek/organization/client-offers/<int:id>/delete/' , shareek.DeleteClientOffer.as_view()),
    path('shareek/organization/client-offers/<int:id>/update/' , shareek.UpdateClientOffer.as_view()),

    path('shareek/organization/<int:id>/service-offers/' , shareek.ServiceOfferView.as_view()),
    path('shareek/organization/service-offers/create/' , shareek.CreateServiceOffer.as_view()),
    path('shareek/organization/service-offers/<int:id>/delete/' , shareek.DeleteServiceOffer.as_view()),
    path('shareek/organization/service-offers/<int:id>/update/' , shareek.UpdateServiceOffer.as_view()),

    path('shareek/templates/' , shareek.TemplatesView.as_view()),

    path('terms-privacy' , common.TermsPrivacyView.as_view()),
    path('contact-us' , common.ContactUsView.as_view()),
    path('common-questions' , common.CommonQuestionsView.as_view()),

    path('reports/create/' , client.CreateReportView.as_view()),
    path('reports/<int:user_id>' , client.ReportListView.as_view()),
    path('reports/organizations' , client.ReportOrganizationsView.as_view())
]


