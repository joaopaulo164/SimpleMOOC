from django.shortcuts import render
from .models import Course

# Create your views here.

def index(request):
    courses = Course.objects.all() # Consulta todos os cursos do Banco
    template_name = 'courses/index.html' # Caminho dos template (dentro do respectivo APP)
    context = {
        'courses': courses # Contexto com variárias para que o Template possa consumir (renderizar)
    }
    return render(request, template_name ,context)