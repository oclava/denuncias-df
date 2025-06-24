from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UsuarioCreationForm
from .models import Usuario

def cadastro_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('ocorrencias:dashboard') 
        else:
            messages.error(request, 'Ocorreu um erro no cadastro. Por favor, verifique os dados.')
    else:
        form = UsuarioCreationForm()
    return render(request, 'app/cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST) 
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            
            if user.is_staff:
                return redirect('ocorrencias:admin_dashboard')
            else:
                return redirect('ocorrencias:dashboard')
        else:
            messages.error(request, 'CPF ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você foi desconectado.') 
    return redirect('home')