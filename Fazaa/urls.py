from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

APIPatterns = [
    path('', include('app.base.urls')),
    path('auth/', include('app.users.urls')),
]

urlpatterns = [
    path("silk/", include("silk.urls", namespace="silk")),
    path('admin/', admin.site.urls),
    path('', include('app.admin_panel.urls')),
    path('api/' , include(APIPatterns)),
]

urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
