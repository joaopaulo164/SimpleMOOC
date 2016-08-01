# coding=utf-8

# Documentação de ferramentas para testes disponibilizada pelo Django (Asserts):
# https://docs.djangoproject.com/pt-br/1.9/topics/testing/tools/

from django.test import TestCase
from django.core import mail
from django.test.client import Client # cliente (broswer para teste do Django)
from django.core.urlresolvers import reverse

# Run you tests:
# (env) computar@user: SimpleMOOC $ python manage.py test

# Create your tests here.


# Classe de teste unitário
class HomeViewTest(TestCase):

    # Teste da view Home
    def test_home_status_code(self):

        # instanciando o cliente
        client = Client()

        # cliente.get () retorna um HttpResponse igual ao da view
        response = client.get('/')
        self.assertEqual(response.status_code, 200)


    # Teste da view Home utilizando reverse do urlresolvers
    def test_home_status_code2(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)


    # Teste da view Home - Testa o template utilizado (incluindo os herdados)
    def test_home_template_used(self):
        client = Client()
        response = client.get(reverse('core:home'))

        # Testa se o template foi usado na view/função
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')

        # Testa se o template não foi usado
        self.assertTemplateNotUsed(response, 'wrong_template.html')
