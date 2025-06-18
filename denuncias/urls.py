from django.contrib import admin
from django.urls import path, include
from denuncias.ocorrencias.views import enviar_denuncia, dashboard, user_logout # Importe suas views
from django.conf import settings # Para servir arquivos de mídia em desenvolvimento
from django.conf.urls.static import static # Para servir arquivos de mídia em desenvolvimento

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('denuncias.usuarios.urls')),
    path('', include('denuncias.home.urls')),
    path('denunciar/', include('denuncias.ocorrencias.urls', namespace='ocorrencias')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)