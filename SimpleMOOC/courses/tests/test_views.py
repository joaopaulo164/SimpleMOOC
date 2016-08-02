# coding=utf-8

# Os arquivos de teste filhos devem ser importados no arquivo __init__.py da pasta tests para serem carregados

# Documentação de ferramentas para testes disponibilizada pelo Django (Asserts):
# https://docs.djangoproject.com/pt-br/1.9/topics/testing/tools/

from django.test import TestCase
from django.core import mail
from django.test.client import Client # cliente (broswer para teste do Django)
from django.core.urlresolvers import reverse
from django.conf import settings

from SimpleMOOC.courses.models import Course

# Run you tests:
# (env) computar@user: SimpleMOOC $ python manage.py test


# Create your tests here.


# Classe de teste unitário
class HomeViewTest(TestCase):

    # Teste da view Home -1
    def test_home_status_code(self):

        # instanciando o cliente
        client = Client()

        # cliente.get () retorna um HttpResponse igual ao da view
        response = client.get('/')
        self.assertEqual(response.status_code, 200)


    # Teste da view Home utilizando reverse do urlresolvers - 2
    def test_home_status_code2(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)


    # Teste da view Home - Testa o template utilizado (incluindo os herdados) - 3
    def test_home_template_used(self):
        client = Client()
        response = client.get(reverse('core:home'))

        # Testa se o template foi usado na view/função
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')

        # Testa se o template não foi usado
        self.assertTemplateNotUsed(response, 'wrong_template.html')


class ContactCourseTestCase(TestCase):


    # Executa ações antes que qualquer teste seja executado
    @classmethod
    def setUpClass(cls):
        pass


    # Executa ações depois que todos os testes foram executados
    @classmethod
    def tearDownClass(cls):
        pass


    # Para cada TestCase e um método de teste for executado "test_contact_form_erro()",
    # será chamado um setUp antes e um tearDown depois do teste


    # Cria um curso - antes da execução de um método de teste (sempre que um teste for chamado)
    def setUp(self):
        self.course = Course.objects.create(name='Django', slug='django')


    # Apaga um curso - depois da execução de um método de teste (sempre que um teste terminar)
    def tearDown(self):
        self.course.delete()


    # cria um formulário de teste
    # submete um formulário com erro (assertFormError) - 4
    def test_contact_form_erro(self):

        # os campos email e message estão em branco para dar erro
        data = {'name': 'Fulando de tal', 'email': '', 'message': ''}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug]) # a função details precisa do argumento slug
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')


    # submete um formulário correto - 5
    # verifica se o e-mail foi enviado com sucesso "self.assertEqual(len(mail.outbox), 1)"
    # verifica se o destinatário da mensagem está correto "self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])"
    def test_contact_form_success(self):

        # os campos email e message estão em branco para dar erro
        data = {'name': 'Fulando de tal', 'email': 'admin@admin.com', 'message': 'Oi'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug]) # a função details precisa do argumento slug
        response = client.post(path, data)

        # verifica se o e-mail foi enviado com sucesso
        self.assertEqual(len(mail.outbox), 1)

        # verifica se o destinatário da mensagem está correto
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])