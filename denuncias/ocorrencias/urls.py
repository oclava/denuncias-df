from django.urls import path
from . import views

app_name = 'denuncias.ocorrencias' 

urlpatterns = [
    path('enviar/', views.enviar_denuncia, name='enviar_denuncia'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detalhes/<int:pk>/', views.detalhes_denuncia, name='detalhes_denuncia'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/detalhes/<int:pk>/', views.admin_detalhes_denuncia, name='admin_detalhes_denuncia')
]