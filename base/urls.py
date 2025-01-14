from django.urls import path , include
from .views import shareek , client , common


urlpatterns = [
    path('org-types' , shareek.OrganizationTypes.as_view()),
    # path('organization/<int:id>' , shareek.UpdateOrganizationView.as_view()),
    path('organization/<int:id>/delete' , shareek.DeleteOrganizationView.as_view()),
    path('organizations' , shareek.OrganizatinosListView.as_view()),
    path('organization/<int:pk>' , shareek.GetOrganizationView.as_view()),

    # path('social-media/' , shareek.SocialMediaView.as_view()),
    path('organization/<int:pk>/social-url/' , shareek.SocialMediaUrlView.as_view()),
    path('organization/<int:pk>/social-urls/update/' , shareek.UpdateSocialMediaUrlView.as_view()),

    # path('delivery-companies/' , shareek.DeliveryCompanyView.as_view()),
    path('organization/<int:pk>/delivery-url/' , shareek.DeliveryUrlView.as_view()),
    path('organization/<int:pk>/delivery-url/update/' , shareek.UpdateDeliveryUrlView.as_view()),

    path('organization/<int:id>/reels/' , shareek.ReelsView.as_view()),
    path('reels/create/' , shareek.CreateReelsView.as_view()),
    path('reels/<int:id>/delete/' , shareek.DeleteReelsView.as_view()),

    path('organization/<int:id>/gallery/' , shareek.GalleryView.as_view()),
    path('gallery/create/' , shareek.CreateGalleryView.as_view()),
    path('gallery/<int:id>/delete/' , shareek.DeleteGalleryView.as_view()),

    path('organization/<int:id>/catalog/' , shareek.CatalogView().as_view()),
    path('catalog/create/' , shareek.CreateCatalogView.as_view()),
    path('catalog/<int:id>/delete/' , shareek.DeleteCatalogView.as_view()),

    path('organization/<int:id>/client-offers/' , shareek.ClientOfferView.as_view()),
    path('client-offer/create/' , shareek.CreateClientOffer.as_view()),
    path('client-offers/<int:id>/delete/' , shareek.DeleteClientOffer.as_view()),
    path('client-offers/<int:id>/update/' , shareek.UpdateClientOffer.as_view()),

    path('organization/<int:id>/service-offers/' , shareek.ServiceOfferView.as_view()),
    path('service-offer/create/' , shareek.CreateServiceOffer.as_view()),
    path('service-offers/<int:id>/delete/' , shareek.DeleteServiceOffer.as_view()),
    path('service-offers/<int:id>/update/' , shareek.UpdateServiceOffer.as_view()),

    path('templates/' , shareek.TemplatesView.as_view()),

    path('terms-privacy/' , common.TermsPrivacyView.as_view()),
    path('common-questions/' , common.CommonQuestionsView.as_view()),

    path('reports/create/' , client.CreateReportView.as_view()),
    path('reports/<int:user_id>' , client.ReportListView.as_view()),
]


