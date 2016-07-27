__author__ = 'john'

# importanto as bibliotecas
from django.template import Library

# registra as TAGS
register = Library()

from SimpleMOOC.courses.models import Enrollment


# Insere um HTML com informa��es (contexto) sobre os meus courses cadastrados
# a TAG my_courses possui HTML pr�prio (courses/templatetags/my_courses.html)
# a TAG my_courses � menos flex�vel, pois eu for�o um HTML fixo que ser� renderizado, utiliza��o no dashboard.htm (accounts/templates)
@register.inclusion_tag('courses/templatetags/my_courses.html') # tag que ser� renderizada
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user) # retorna as inscri��es do usu�rio
    context = {}
    context['enrollments'] = enrollments
    return context


# Atualiza o contexto com os meus courses cadastrados
# a TAG load_my_courses, apenas atualiza o contexto e n�o possui HTML pr�prio
# a TAG load_my_courses � mais flex�vel por n�o possuir HTML, utiliza��o no dashboard.htm (accounts/templates)
@register.assignment_tag
def load_my_courses(user):
    return Enrollment.objects.filter(user=user) # retorna as inscri��es do usu�rio