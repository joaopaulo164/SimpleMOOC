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

from model_mommy import mommy

# Run you tests:
# (env) computar@user: SimpleMOOC $ python manage.py test


# Create your tests here.


# Teste - 6
class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.courses_django = mommy.make('courses.Course', name='Python na Web com Django', _quantity=5)
        self.courses_dev = mommy.make('courses.Course', name='Python para Devs', _quantity=10)
        self.client = Client()

        # for course in self.courses_django:
        #     print(course)
        # for course in self.courses_dev:
        #     print(course)


    def tearDown(self):
        Course.objects.all().delete()


    def test_course_search(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search), 5)
        search = Course.objects.search('devs')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('python')
        self.assertEqual(len(search), 15)


# Teste - 7
class CourseManagerTestCase2(TestCase):

    def setUp(self):
        self.courses = []
        names = ['Python para iniciantes', 'Python pra Web', 'Python com Django', 'Java para iniciantes', 'Java pra Web']
        for name in names:
            course = mommy.make('courses.Course', name=name)
            self.courses.append(course)
        self.client = Client()


    def tearDown(self):
        Course.objects.all().delete()


    def test_course_search(self):
        search = Course.objects.search('python')
        self.assertEqual(len(search), 3)
        search = Course.objects.search('java')
        self.assertEqual(len(search), 2)
        search = Course.objects.search('django')
        self.assertEqual(len(search), 1)
