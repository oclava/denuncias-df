from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import DenunciaForm, AdminDenunciaAssignmentForm
from .models import Denuncia
from django.contrib import messages
from django.contrib.auth import logout 

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
            messages.error(request, 'Ocorreu um erro ao enviar a denúncia. Por favor, verifique os campos.')
    else:
        form = DenunciaForm()
    
    return render(request, 'app/enviar_denuncia.html', {'form': form})

@login_required
def dashboard(request):
    # pega todas as denúncias criadas pelo usuário logado
    minhas_denuncias = Denuncia.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    context = {
        'minhas_denuncias': minhas_denuncias
    }
    # Retorna o template renderizado com o contexto das denúncias
    return render(request, 'app/user-dashboard.html', context)

@login_required
def detalhes_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk, usuario=request.user)
    
    context = {
        'denuncia': denuncia
    }

    return render(request, 'app/detalhes_denuncia.html', context)


def user_logout(request):
    logout(request)
    return redirect('login') 

# Dashboard do administrador 
@login_required
@user_passes_test(is_staff_user) # apenas usuários staff possam acessar
def admin_dashboard(request):
    # mostra todas as denuncias
    todas_denuncias = Denuncia.objects.all()

    # Se o usuário for um superusuário, ele vê todas as denúncias
    if request.user.is_superuser:
        pass # 'todas_denuncias' já contém tudo
    else:
        # Para usuários staff que NÃO são superusuários:
        # Pega os IDs de todos os órgãos pelos quais este usuário é responsável
        user_orgaos_ids = request.user.orgaos_responsavel.values_list('id', flat=True)

        if not user_orgaos_ids:
            # Se o usuário staff não tem nenhum órgão associado, ele não vê nenhuma denúncia
            todas_denuncias = Denuncia.objects.none() # Retorna um QuerySet vazio
            messages.warning(request, "Seu usuário não está associado a nenhum órgão responsável. Você não pode ver nenhuma denúncia.")
        else:
            # Filtra as denúncias que têm pelo menos um dos órgãos do usuário designados
            # Usa '__in' para verificar se os orgaos_designados da denúncia contêm QUALQUER um dos orgaos_responsavel do usuário
            todas_denuncias = todas_denuncias.filter(orgaos_designados__id__in=user_orgaos_ids).distinct()
            # '.distinct()' é importante para evitar que a mesma denúncia apareça várias vezes
            # se ela tiver múltiplos órgãos designados e o usuário for responsável por mais de um deles.

    context = {
        'todas_denuncias': todas_denuncias.order_by('-data_criacao'), # Ordena pela data de criação mais recente
        'active_tab': 'admin_dashboard', # Para navegação ativa no template
    }
    return render(request, 'app/admin_dashboard.html', context)


# A view admin_detalhes_denuncia também precisa ser atualizada para verificar a permissão
@login_required
@user_passes_test(is_staff_user)
def admin_detalhes_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)

    if not request.user.is_superuser:
        user_orgaos_ids = request.user.orgaos_responsavel.values_list('id', flat=True)
        # Verifica se algum dos órgãos designados para esta denúncia está entre os órgãos que o usuário gerencia
        if not denuncia.orgaos_designados.filter(id__in=user_orgaos_ids).exists():
            messages.error(request, "Você não tem permissão para acessar esta denúncia.")
            return redirect('ocorrencias:admin_dashboard') # Redireciona de volta para o dashboard

    # Lógica de processamento do formulário
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