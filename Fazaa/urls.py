from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

APIPatterns = [
    path('', include('base.urls')),
    path('auth/', include('users.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('dashboard/', include('admin_panel.urls')),
    path('api/' , include(APIPatterns)),

]+ static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
