# coding=utf-8

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login # necessario para autenticar depois de cadastrado o usuário
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegisterForm, EditAccountForm

# Create your views here.

# @login_required => verifica se o usuário está logado, caso contrário redireciona para a página/view de login
@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)

def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = RegisterForm(request.POST) # Utilizando o Form customizado RegisterForm que é o UserCreationForm modificado
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username,
                password=form.cleaned_data['password1']) # não usar user.password porque a senha está criptografada
            login(request, user) # view login coloca o usuário na sessão
            # return redirect(settings.LOGIN_URL) # redireciona o usuário para tela de login
            return redirect('core:home') # redireciona o usuário para págino home
    else:
        # form = UserCreationForm()
        form = RegisterForm() # Utilizando o Form customizado RegisterForm que é o UserCreationForm modificado
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user) # Parametros: (POST do formulário, usuário à ser modificado, ou seja, usuário atualS)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user) # cria novamente usuário vazio
            context['success'] = True # variavel success para interagir com o template
    else:
        form = EditAccountForm(instance=request.user) # cria novamente usuário vazio
    context['form'] = form
    return render(request, template_name, context)
