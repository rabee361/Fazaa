from django.urls import path , include
from . import views


ShareekPatterns = [
    # path('organization' , CreateOrganizationView.as_view() , name="create-organization"),
    # path('organization/<int:id>' , UpdateOrganizationView.as_view() , name="update-organization"),
    # path('organization/<int:id>' , DeleteOrganizationView.as_view() , name="delete-organization"),
    # path('organization/<int:id>' , GetOrganizationView.as_view() , name="get-organization"),
    path('organization/<int:id>/social-media/' , views.SocialMediaView.as_view() , name="social-media"),
    path('organization/social-media/update/' , views.UpdateSocialMediaLinkView.as_view() , name="update-social-media-link"),
    path('organization/<int:id>/delivery-link/' , views.DeliveryLinkView.as_view() , name="delivery-link"),
    path('organization/delivery-link/update/' , views.UpdateDeliveryLinkView.as_view() , name="update-delivery-link"),

    path('organization/<int:id>/reels/' , views.OrganizationReelsView.as_view() , name="organization-reels"),
    path('organization/reels/create/' , views.CreateOrganizationReelsView.as_view() , name="create-organization-reels"),
    path('organization/reels/<int:id>/delete/' , views.DeleteOrganizationReelsView.as_view() , name="delete-organization-reels"),

    path('organization/<int:id>/gallery/' , views.OrganizationGalleryView.as_view() , name="organization-gallery"),
    path('organization/gallery/create/' , views.CreateOrganizationGalleryView.as_view() , name="create-organization-gallery"),
    path('organization/gallery/<int:id>/delete/' , views.DeleteOrganizationGalleryView.as_view() , name="delete-organization-gallery"),

    path('organization/<int:id>/catalog/' , views.OrganizationCatalogView().as_view() , name="organization-catalog"),
    path('organization/catalog/create/' , views.CreateOrganizationCatalogView.as_view() , name="create-organization-catalog"),
    path('organization/catalog/<int:id>/delete/' , views.DeleteOrganizationCatalogView.as_view() , name="delete-organization-catalog"),

    path('organization/<int:id>/client-offers/' , views.ListClientOffers.as_view() , name="client-offers"),
    path('organization/client-offer/create' , views.CreateClientOffer.as_view() , name="create-client-offer"),
    path('organization/client-offers/<int:id>/delete/' , views.DeleteClientOffer.as_view() , name="delete-client-offer"),
    path('organization/client-offers/<int:id>/update/' , views.UpdateClientOffer.as_view() , name="update-client-offer"),

    path('organization/<int:id>/shareek-offers/' , views.ListShareekOffers.as_view() , name="shareek-offers"),
    path('organization/shareek-offer/create' , views.CreateShareekOffer.as_view() , name="create-shareek-offer"),
    path('organization/shareek-offers/<int:id>/delete/' , views.DeleteShareekOffer.as_view() , name="delete-shareek-offer"),
    path('organization/shareek-offers/<int:id>/update/' , views.UpdateShareekOffer.as_view() , name="update-shareek-offer"),

    path('organization/catalog/create/' , views.CreateCatalogView().as_view , name="create-catalog"),
    path('organization/catalog/<int:id>/' , views.CatalogView().as_view , name="catalog"),
]


ClientPatterns = [
    # path('organizations/' , ListOrganizationView.as_view() , name="list-organization"),
]


urlpatterns = [
    path('shareek/' , include(ShareekPatterns)),
    path('client/' , include(ClientPatterns)),
]
