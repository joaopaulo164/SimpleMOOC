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

urlpatterns = patterns('SimpleMOOC.courses.views',
    # caminho para view index da app courses
    url(r'^$', 'index', name='index'),

    # caminho para view details da app courses - (?P<pk>\d+) express�o regular = valor decimal (1 ou mais digitos) nomeado como pk
    #url(r'^(?P<pk>\d+)/$', 'details', name='details'),

    # caminho para view details da app courses - (?P<slug>[\w_-]+) express�o regular = caracteres que do slug ("alfa-numerico"_-). Ex: pytho-para-zumbis
    url(r'^(?P<slug>[\w_-]+)/$', 'details', name='details'),

    # caminho para a view enrollment
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', 'enrollment', name='enrollment'),
    url(r'^(?P<slug>[\w_-]+)/anuncios/$', 'announcements', name='announcements'),
)