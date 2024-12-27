from django.urls import path , include
from .views import shareek , client


urlpatterns = [
    path('org-types' , shareek.OrganizationTypes.as_view()),
    # path('organization/<int:id>' , shareek.UpdateOrganizationView.as_view()),
    path('organization/<int:id>' , shareek.DeleteOrganizationView.as_view()),
    path('organization/<int:pk>' , shareek.GetOrganizationView.as_view()),

    path('<int:id>/social-media/' , shareek.SocialMediaUrlView.as_view()),
    path('social-media/update/' , shareek.UpdateSocialMediaUrlView.as_view()),

    path('<int:id>/delivery-url/' , shareek.DeliveryUrlView.as_view()),
    path('delivery-url/update/' , shareek.UpdateDeliveryUrlView.as_view()),

    path('<int:id>/reels/' , shareek.ReelsView.as_view()),
    path('reels/create/' , shareek.CreateReelsView.as_view()),
    path('<int:id>/reels/delete/' , shareek.DeleteReelsView.as_view()),

    path('<int:id>/gallery/' , shareek.GalleryView.as_view()),
    path('gallery/create/' , shareek.CreateGalleryView.as_view()),
    path('<int:id>/gallery/delete/' , shareek.DeleteGalleryView.as_view()),

    path('<int:id>/catalog/' , shareek.CatalogView().as_view()),
    path('catalog/create/' , shareek.CreateCatalogView.as_view()),
    path('<int:id>/catalog/delete/' , shareek.DeleteCatalogView.as_view()),

    path('<int:id>/client-offers/' , shareek.ClientOfferView.as_view()),
    path('client-offer/create' , shareek.CreateClientOffer.as_view()),
    path('<int:id>/client-offers/delete/' , shareek.DeleteClientOffer.as_view()),
    path('<int:id>/client-offers/update/' , shareek.UpdateClientOffer.as_view()),

    path('<int:id>/service-offers/' , shareek.ServiceOfferView.as_view()),
    path('service-offer/create' , shareek.CreateServiceOffer.as_view()),
    path('service-offers/<int:id>/delete/' , shareek.DeleteServiceOffer.as_view()),
    path('service-offers/<int:id>/update/' , shareek.UpdateServiceOffer.as_view()),

    path('templates/' , shareek.TemplatesView.as_view()),
]


