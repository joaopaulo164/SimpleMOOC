from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Course, Enrollment

# Criando decorator enrollment_required (inscrição é obrigatória)
# (view_func) => recebe a função da view do Django
def enrollment_required(view_func):

    # antes de executar a view recebida executa a função auxiliar def _wrapper() (nossa view de fato)
    def _wrapper(request, *args, **kwargs):
        slug = kwargs['slug'] # procura nos kwargs o parametro slug
        course = get_object_or_404(Course, slug=slug) # busca o curso pelo slug
        has_permission = request.user.is_staff # verifica se o usuário é admin (staff)
        # se não tiver permissão (staff)
        if not has_permission:
            try:
                # verifica se existe inscrição para o usuário atual e o curso
                enrollment = Enrollment.objects.get(
                    user=request.user, course=course
                )
            except Enrollment.DoesNotExist:
                # se não existir permissão (inscrição) set mensagem de erro
                message = 'Desculpe, mas você não tem permissão para acessar esta página'
            else:
                # se existir permissão, verifica se foi aprovado
                if enrollment.is_approved():
                    # se aprovado dá permissão
                    has_permission = True
                else:
                    # se não aprovado set mensagem de erro
                    message = 'A sua inscrição no curso ainda está pendente'
        # se não tiver permissão retorna mensagem de erro e redireciona para o dashboard
        if not has_permission:
            messages.error(request, message)
            return redirect('accounts:dashboard')
        # se tiver permissão retorna o curso para requisião
        request.course = course
        # executa a view de fato
        return view_func(request, *args, **kwargs)
    return _wrapper
