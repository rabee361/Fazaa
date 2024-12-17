from django.urls import path , include
from .views import shareek , client


ShareekPatterns = [
    path('org-types' , shareek.OrganizationTypes.as_view()),
    # path('organization/<int:id>' , UpdateOrganizationView.as_view()),
    # path('organization/<int:id>' , DeleteOrganizationView.as_view()),
    # path('organization/<int:id>' , GetOrganizationView.as_view()),
    path('organization/<int:id>/social-media/' , shareek.SocialMediaView.as_view()),
    path('organization/social-media/update/' , shareek.UpdateSocialMediaLinkView.as_view()),
    path('organization/<int:id>/delivery-link/' , shareek.DeliveryLinkView.as_view()),
    path('organization/delivery-link/update/' , shareek.UpdateDeliveryLinkView.as_view()),

    path('organization/<int:id>/reels/' , shareek.OrganizationReelsView.as_view()),
    path('organization/reels/create/' , shareek.CreateOrganizationReelsView.as_view()),
    path('organization/reels/<int:id>/delete/' , shareek.DeleteOrganizationReelsView.as_view()),

    path('organization/<int:id>/gallery/' , shareek.OrganizationGalleryView.as_view()),
    path('organization/gallery/create/' , shareek.CreateOrganizationGalleryView.as_view()),
    path('organization/gallery/<int:id>/delete/' , shareek.DeleteOrganizationGalleryView.as_view()),

    path('organization/<int:id>/catalog/' , shareek.OrganizationCatalogView().as_view()),
    path('organization/catalog/create/' , shareek.CreateOrganizationCatalogView.as_view()),
    path('organization/catalog/<int:id>/delete/' , shareek.DeleteOrganizationCatalogView.as_view()),

    path('organization/<int:id>/client-offers/' , shareek.ListClientOffers.as_view()),
    path('organization/client-offer/create' , shareek.CreateClientOffer.as_view()),
    path('organization/client-offers/<int:id>/delete/' , shareek.DeleteClientOffer.as_view()),
    path('organization/client-offers/<int:id>/update/' , shareek.UpdateClientOffer.as_view()),

    path('organization/<int:id>/service-offers/' , shareek.ListServiceOffers.as_view()),
    path('organization/service-offer/create' , shareek.CreateServiceOffer.as_view()),
    path('organization/service-offers/<int:id>/delete/' , shareek.DeleteServiceOffer.as_view()),
    path('organization/service-offers/<int:id>/update/' , shareek.UpdateServiceOffer.as_view()),
]


ClientPatterns = [
    # path('organizations/' , ListOrganizationView.as_view()),
]


urlpatterns = [
    path('shareek/' , include(ShareekPatterns)),
    path('client/' , include(ClientPatterns)),
]
