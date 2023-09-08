from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.AdminSite.site_header = 'Monitor de Pragas'
admin.AdminSite.site_title = 'Painel do Administrador'
admin.AdminSite.index_title ='Painel do Administrador'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)