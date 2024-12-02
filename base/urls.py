from django.urls import path , include
from .views import shareek , client


ShareekPatterns = [
    path('org-types' , shareek.OrganizationTypes.as_view() , name="org-types"),
    # path('organization/<int:id>' , UpdateOrganizationView.as_view() , name="update-organization"),
    # path('organization/<int:id>' , DeleteOrganizationView.as_view() , name="delete-organization"),
    # path('organization/<int:id>' , GetOrganizationView.as_view() , name="get-organization"),

    path('organization/<int:id>/social-media/' , shareek.SocialMediaView.as_view() , name="social-media"),
    path('organization/social-media/update/' , shareek.UpdateSocialMediaLinkView.as_view() , name="update-social-media-link"),
    path('organization/<int:id>/delivery-link/' , shareek.DeliveryLinkView.as_view() , name="delivery-link"),
    path('organization/delivery-link/update/' , shareek.UpdateDeliveryLinkView.as_view() , name="update-delivery-link"),

    path('organization/<int:id>/reels/' , shareek.OrganizationReelsView.as_view() , name="organization-reels"),
    path('organization/reels/create/' , shareek.CreateOrganizationReelsView.as_view() , name="create-organization-reels"),
    path('organization/reels/<int:id>/delete/' , shareek.DeleteOrganizationReelsView.as_view() , name="delete-organization-reels"),

    path('organization/<int:id>/gallery/' , shareek.OrganizationGalleryView.as_view() , name="organization-gallery"),
    path('organization/gallery/create/' , shareek.CreateOrganizationGalleryView.as_view() , name="create-organization-gallery"),
    path('organization/gallery/<int:id>/delete/' , shareek.DeleteOrganizationGalleryView.as_view() , name="delete-organization-gallery"),

    path('organization/<int:id>/catalog/' , shareek.OrganizationCatalogView().as_view() , name="organization-catalog"),
    path('organization/catalog/create/' , shareek.CreateOrganizationCatalogView.as_view() , name="create-organization-catalog"),
    path('organization/catalog/<int:id>/delete/' , shareek.DeleteOrganizationCatalogView.as_view() , name="delete-organization-catalog"),

    path('organization/<int:id>/client-offers/' , shareek.ListClientOffers.as_view() , name="client-offers"),
    path('organization/client-offer/create/' , shareek.CreateClientOffer.as_view() , name="create-client-offer"),
    path('organization/client-offers/<int:id>/delete/' , shareek.DeleteClientOffer.as_view() , name="delete-client-offer"),
    path('organization/client-offers/<int:id>/update/' , shareek.UpdateClientOffer.as_view() , name="update-client-offer"),

    path('organization/<int:id>/service-offers/' , shareek.ListServiceOffers.as_view() , name="service-offers"),
    path('organization/service-offers/create/' , shareek.CreateServiceOffer.as_view() , name="create-service-offer"),
    path('organization/service-offers/<int:id>/delete/' , shareek.DeleteServiceOffer.as_view() , name="delete-service-offer"),
    path('organization/service-offers/<int:id>/update/' , shareek.UpdateServiceOffer.as_view() , name="update-service-offer"),

    path('templates/' , shareek.ListTemplatesView.as_view() , name="templates")
]


ClientPatterns = [
    # path('organizations/' , ListOrganizationView.as_view() , name="list-organization"),
]


urlpatterns = [
    path('shareek/' , include(ShareekPatterns)),
    path('client/' , include(ClientPatterns)),
]
