# denuncias/usuarios/views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm # Importa o formulário de autenticação padrão do Django
from .forms import UsuarioCreationForm # Importa o seu formulário de cadastro personalizado
from .models import Usuario # Mantido para referência, mas não usado diretamente nas views de form aqui

# Função de cadastro
def cadastro_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST) # Instancia o formulário com os dados da requisição
        if form.is_valid():
            user = form.save() # Se o formulário for válido, salva o usuário (a senha já é hashada e validada)
            login(request, user) # Faz o login do usuário recém-cadastrado
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('ocorrencias:dashboard') # Redireciona para o dashboard após o login
        else:
            # Se o formulário não for válido, ele conterá os erros
            # E as mensagens de erro serão exibidas no template (que você já atualizou)
            messages.error(request, 'Ocorreu um erro no cadastro. Por favor, verifique os dados.')
            # A view renderizará o template com o formulário contendo os erros
    else:
        form = UsuarioCreationForm() # Cria uma instância vazia do formulário para requisições GET

    # Passa o formulário (com ou sem dados/erros) para o template
    return render(request, 'app/cadastro.html', {'form': form})

# Função de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST) # Instancia o formulário de autenticação
        if form.is_valid():
            # O AuthenticationForm já fez o authenticate para nós
            user = form.get_user() # Pega o usuário autenticado do formulário
            login(request, user) # Faz o login do usuário
            messages.success(request, 'Login realizado com sucesso!')
            
            # Lógica para redirecionar usuários staff para o dashboard de admin
            if user.is_staff:
                return redirect('ocorrencias:admin_dashboard')
            else:
                return redirect('ocorrencias:dashboard')
        else:
            # Se o formulário não for válido (CPF ou senha incorretos), ele conterá os erros
            # E as mensagens de erro serão exibidas no template (que você já atualizou)
            messages.error(request, 'CPF ou senha inválidos.')
            # A view renderizará o template com o formulário contendo os erros
    else:
        form = AuthenticationForm() # Cria uma instância vazia do formulário para requisições GET

    # Passa o formulário (com ou sem dados/erros) para o template
    return render(request, 'app/login.html', {'form': form})

# Função de logout
def logout_view(request):
    logout(request)
    messages.info(request, 'Você foi desconectado.') # Mensagem informativa no logout
    return redirect('home') # Redireciona para a sua página inicial (ou outra que desejar)