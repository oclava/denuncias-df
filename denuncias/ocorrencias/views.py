from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import DenunciaForm, AdminDenunciaAssignmentForm
from .models import Denuncia, CategoriaDenuncia, Orgao 
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Avg

import geopandas
from shapely.geometry import Point
import folium
import os
from django.conf import settings 


def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@login_required
def enviar_denuncia(request):
    if request.method == 'POST':
        form = DenunciaForm(request.POST, request.FILES)
        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.usuario = request.user
            denuncia.save()
            messages.success(request, 'Denúncia enviada com sucesso! Agradecemos sua colaboração.')
            return redirect('ocorrencias:dashboard')
        else:
            print("Erros do formulário:", form.errors) # mostra os erros no terminal
            messages.error(request, 'Ocorreu um erro ao enviar a denúncia. Por favor, verifique os campos.')
    else:
        form = DenunciaForm()
    
    context = {
        'form': form
    }
    return render(request, 'app/enviar_denuncia.html', context)

@login_required
def dashboard(request):
    # filtra as denuncias
    minhas_denuncias = Denuncia.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    context = {
        'minhas_denuncias': minhas_denuncias
    }
    return render(request, 'app/user-dashboard.html', context) # context renderiza as denuncias do usuario no front

@login_required
def detalhes_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk, usuario=request.user)
    
    context = {
        'denuncia': denuncia
    }

    return render(request, 'app/detalhes_denuncia.html', context)


def user_logout(request):
    logout(request)
    return redirect('home') 

# dashboard do administrador 
@login_required
@user_passes_test(is_staff_user) # apenas usuários staff possam acessar
def admin_dashboard(request):
    # mostra todas as denuncias
    todas_denuncias = Denuncia.objects.all()

    if request.user.is_superuser:
        pass 
    else:
        user_orgaos_ids = request.user.orgaos_responsavel.values_list('id', flat=True) # filtra para os responsaveis dos orgaos

        if not user_orgaos_ids:
            todas_denuncias = Denuncia.objects.none() # se remover buga
            messages.warning(request, "Seu usuário não está associado a nenhum órgão responsável. Você não pode ver nenhuma denúncia.")
        else:
            todas_denuncias = todas_denuncias.filter(orgaos_designados__id__in=user_orgaos_ids).distinct()

    context = {
        'todas_denuncias': todas_denuncias.order_by('-data_criacao'), 
        'active_tab': 'admin_dashboard', # para navegação no template
    }
    return render(request, 'app/admin_dashboard.html', context)

# detalhes da denuncia
@login_required
@user_passes_test(is_staff_user)
def admin_detalhes_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)

    if not request.user.is_superuser:
        user_orgaos_ids = request.user.orgaos_responsavel.values_list('id', flat=True)
        if not denuncia.orgaos_designados.filter(id__in=user_orgaos_ids).exists():
            messages.error(request, "Você não tem permissão para acessar esta denúncia.")
            return redirect('ocorrencias:admin_dashboard') 

    if request.method == 'POST':
        form = AdminDenunciaAssignmentForm(request.POST, instance=denuncia)
        if form.is_valid():
            form.save()
            messages.success(request, "Denúncia atualizada com sucesso!")
            return redirect('ocorrencias:admin_detalhes_denuncia', pk=denuncia.pk)
    else:
        form = AdminDenunciaAssignmentForm(instance=denuncia)

    context = {
        'denuncia': denuncia,
        'form': form,
    }
    return render(request, 'app/admin_detalhes_denuncia.html', context)


@login_required
@user_passes_test(is_staff_user)
def mapa_denuncias(request):

    todas_denuncias = Denuncia.objects.all()

    if not request.user.is_superuser:
        user_orgaos_ids = request.user.orgaos_responsavel.values_list('id', flat=True)
        if not user_orgaos_ids:
            todas_denuncias = Denuncia.objects.none()
            messages.warning(request, "Seu usuário não está associado a nenhum órgão responsável. Você não pode ver nenhuma denúncia no mapa.")
        else:
            todas_denuncias = todas_denuncias.filter(orgaos_designados__id__in=user_orgaos_ids).distinct()
    
    # filtros
    status_filter = request.GET.get('status', '')
    categoria_filter = request.GET.get('categoria', '')
    orgao_filter = request.GET.get('orgao', '')

    if status_filter:
        todas_denuncias = todas_denuncias.filter(status=status_filter)
    if categoria_filter:
        todas_denuncias = todas_denuncias.filter(categoria__id=categoria_filter)
    if orgao_filter:
        todas_denuncias = todas_denuncias.filter(orgaos_designados__id=orgao_filter)

    # filtra somente os que tem longitude e latitude
    denuncias_com_localizacao = todas_denuncias.filter(latitude__isnull=False, longitude__isnull=False).order_by('-data_criacao')

    #geopandas
    den_data = []
    for den in denuncias_com_localizacao:
        if den.latitude is not None and den.longitude is not None:
            den_data.append({
                'id': den.id,
                'titulo': den.titulo,
                'descricao': den.descricao,
                'status': den.get_status_display(), 
                'categoria': den.categoria.nome,
                'localizacao_txt': den.localizacao,
                'latitude': float(den.latitude),
                'longitude': float(den.longitude)
            })
            print(f"Den_data final: {den_data}")


    if den_data:
        # tudo isso pra centralizar o mapa
        avg_lat = sum([d['latitude'] for d in den_data]) / len(den_data)
        avg_lon = sum([d['longitude'] for d in den_data]) / len(den_data)
        map_center = [avg_lat, avg_lon]
        zoom_level = 12 
    else:
        # centraliza em bsb
        map_center = [-15.7801, -47.9292] 
        zoom_level = 10

    m = folium.Map(location=map_center, zoom_start=zoom_level)

    # cores do pinos no mapa
    status_colors = {
        'Aberta': 'blue',
        'Em análise': 'orange',
        'Encaminhada': 'purple',
        'Concluída': 'green',   
        'Rejeitada': 'red',    
        'default': 'gray'       
    }

    # coloca os pinos no mapa
    for data in den_data:
        admin_detail_url = f"/admin/detalhes/{data['id']}"
        # ordem que aparece se clicar na denuncia
        popup_content = f"<b>{data['titulo']}</b><br>" \
                        f"Status: {data['status']}<br>" \
                        f"Categoria: {data['categoria']}<br>" \
                        f"Descrição: {data['descricao']}<br>" \
                        f"Endereço: {data['localizacao_txt'] or 'Não informado'}<br>" \
                        f"<a href='{admin_detail_url}' target='_blank'>Ver Detalhes</a>"
        
        marker_color = status_colors.get(data['status'], status_colors['default'])
        
        folium.Marker(
            location=[data['latitude'], data['longitude']],
            popup=popup_content,
            tooltip=data['titulo'],
            icon=folium.Icon(color=marker_color, icon='info-sign')
        ).add_to(m)
    
    # renderiza em html
    map_html = m._repr_html_()

    # filtros base
    status_choices = Denuncia.STATUS_CHOICES
    categorias = CategoriaDenuncia.objects.all().order_by('nome') 
    orgaos = Orgao.objects.all().order_by('nome') 

    context = {
        'map_html': map_html, 
        'status_choices': status_choices,
        'categorias': categorias,
        'orgaos': orgaos,
        'selected_status': status_filter,
        'selected_categoria': categoria_filter,
        'selected_orgao': orgao_filter,
        'active_tab': 'mapa_denuncias', 
    }
    return render(request, 'app/admin_mapa_denuncias.html', context)