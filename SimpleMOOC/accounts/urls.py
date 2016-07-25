# coding=utf-8
"""SimpleMOOC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
    url(r'^$', 'SimpleMOOC.accounts.views.dashboard', name='dashboard'),

    # utilizando uma view direta do Django para login
    # template_name => modifica para o nosso template a função de login
    url(r'^entrar/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),

    # utilizando uma view direta do Django para logout
    # next_page => vai para a pagina home do modulo core (Pagina principal)
    url(r'^sair/$', 'django.contrib.auth.views.logout', {'next_page': 'core:home'}, name='logout'),

    url(r'^cadastre-se/$', 'SimpleMOOC.accounts.views.register', name='register'),
    url(r'^editar/$', 'SimpleMOOC.accounts.views.edit', name='edit'),
    url(r'^editar-senha/$', 'SimpleMOOC.accounts.views.edit_password', name='edit_password'),
)