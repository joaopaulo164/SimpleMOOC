__author__ = 'john'

# importanto as bibliotecas
from django.template import Library

# registra as TAGS
register = Library()

from SimpleMOOC.courses.models import Enrollment


# Insere um HTML com informações (contexto) sobre os meus courses cadastrados
# a TAG my_courses possui HTML próprio (courses/templatetags/my_courses.html)
# a TAG my_courses é menos flexível, pois eu forço um HTML fixo que será renderizado, utilização no dashboard.htm (accounts/templates)
@register.inclusion_tag('courses/templatetags/my_courses.html') # tag que será renderizada
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user) # retorna as inscrições do usuário
    context = {}
    context['enrollments'] = enrollments
    return context


# Atualiza o contexto com os meus courses cadastrados
# a TAG load_my_courses, apenas atualiza o contexto e não possui HTML próprio
# a TAG load_my_courses é mais flexível por não possuir HTML, utilização no dashboard.htm (accounts/templates)
@register.assignment_tag
def load_my_courses(user):
    return Enrollment.objects.filter(user=user) # retorna as inscrições do usuário