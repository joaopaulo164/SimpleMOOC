# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages # modulo de exibição de mensagens do Django
from .models import Course, Enrollment
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
    context = {}
    if request.method == 'POST': # verifica se a requisiçãoo foi um POST
        form = ContactCourse(request.POST) # o POST é um dicionário com todos os campos submetidos pelo usuário
        if form.is_valid():
            context['is_valid'] = True
            #print(form.cleaned_data) # para acessar os dados do formulário => form.cleaned_data['name'] por exemplo
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['course'] = course
    context['form'] = form

    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    # pega o curso atual
    course = get_object_or_404(Course, slug=slug)
    # verifico se existe uma inscrição para o usuário, se não cria a inscrição
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    # Se enrollment.active default for == 0 é preciso ativar (descomentar o códig abaixo), no nosso caso já colocamos 1, ou seja, ativado
    if created:
        # enrollment.active()

        # utiliza o modulo padrão de mensagens do Django para enviar uma mensagem sobre ações do usuário.
        # sua utilização encontra-se no arquivo base.html (app:core/templates)
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')
    return redirect('accounts:dashboard')


