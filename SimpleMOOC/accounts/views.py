# coding=utf-8

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm, SetPasswordForm)

# (authenticate, login) necessario para autenticar depois de cadastrado o usuário
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings

from SimpleMOOC.core.utils import generate_hash_key
from SimpleMOOC.courses.models import Enrollment

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

# Create your views here.

User = get_user_model() # Pega o usuário customizado

# @login_required => verifica se o usuário está logado, caso contrário redireciona para a página/view de login
@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context = {}

    # Removido para fazer uma Custom TAG (templatetags em courses) my_courses é o nome da TAG
    # Desta maneira conseguimos deixar disponível a função/tag my_courses disponível para o projeto inteiro
    # context['enrollments'] = Enrollment.objects.filter(user=request.user) # Passando as inscrições para o contexto da view dashboard

    return render(request, template_name, context)

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


def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}
    # Se request.Post estiver vazio (False) será preenchido com None, ou seja, PasswordResetForm(), pois ele não validará o formulário
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        #
        # Removendo a lógica da View para o forms.py, método save() da classe PasswordResetForm
        #
        # user = User.objects.get(email=form.cleaned_data['email'])
        # key = generate_hash_key(user.username)
        # reset = PasswordReset(key=key, user=user)
        # reset.save()
        #
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None) # Formulário sem a solicitação de senha antiga.
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user) # Parametros: (POST do formulário, usuário à ser modificado, ou seja, usuário atualS)
        if form.is_valid():
            form.save()

            # removido ao refatorar e utilizar o módulo MESSAGES do Django #
            # Não precisa mais limpar o formulário, pois damos o return redirect('accounts:dashboard') abaixo
            #form = EditAccountForm(instance=request.user) # cria novamente usuário vazio

            # removido para refatorar e utilizar o módulo MESSAGES do Django
            #context['success'] = True # variavel success para interagir com o template

            # Refatoração => Usando o módulo MESSAGES do Django para exibir mensagens
            # Utilização no arquivo base.html (app:core/templates)
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso!')
            return redirect('accounts:dashboard')
    else:
        form = EditAccountForm(instance=request.user) # cria novamente usuário vazio
    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user) # PasswordChangeForm => Form do Django para alerar senha
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)
