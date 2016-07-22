from django.shortcuts import render, get_object_or_404
from .models import Course
from .forms import ContactCourse # importando o form

# Create your views here.

def index(request):
    courses = Course.objects.all() # Consulta todos os cursos do Banco
    template_name = 'courses/index.html' # Caminho dos template (dentro do respectivo APP)
    context = {
        'courses': courses # Contexto com vari�rias para que o Template possa consumir (renderizar)
    }
    return render(request, template_name ,context)

# def details(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     template_name = 'courses/details_old.html'
#     context = {
#         'course': course
#     }
#     return render(request, template_name, context)


def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    template_name = 'courses/details.html'
    if request.method == 'POST': # verifica se a requisi��o foi um POST
        form = ContactCourse(request.POST) # o POST � um dicion�rio com todos os campos submetidos pelo usu�rio
    else:
        form = ContactCourse()
    context = {
        'course': course,
        'form': form
    }
    return render(request, template_name, context)