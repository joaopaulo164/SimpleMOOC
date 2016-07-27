# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

# Create your models here.

# Customizando Course.objects
class CourseManager(models.Manager):
    # Função search() = Retorna cursos onde nome ou descrição forem iguais ao valor (string) passada como parametro
    # Ex: Curso.object.search('python')
    def search(self, query):
        return self.get_queryset().filter(models.Q(name__icontains=query) | models.Q(description__icontains=query)) # Q para utilizar | (ou)

class Course(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição Simples', blank=True)
    about = models.TextField('Sobre o curso', blank=True)
    start_date = models.DateField('Data de Início', null=True, blank=True)
    image = models.ImageField(upload_to='courses/images', verbose_name='Imagem', null=True, blank=True)   # upload_to = salva o caminho do arquivo (imagem)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)  # auto_now_add = preenche com a data de criação
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)   # auto_now = preenche com a data atual toda vez que for salvo (atualizado)

    # Course.objects customizado
    objects = CourseManager()

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        #reverse = resgatar\retornar a url
        return ('courses:details', (), {'slug': self.slug})

    # Customiza o nome da classe para exibição no ADMIN
    class Meta:
        verbose_name_plural = 'Cursos'
        verbose_name = 'Curso'
        # ordenar pela ordem crescent do nome
        ordering = ['name']
        # ordenar decrescente ['-name'] (colocar menos na frente do campo)


class Enrollment(models.Model):
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        related_name='enrollments'
    )  # enrollments => atributo que será criado no usuário para fazer a busca (relação) no modelo Enrollment

    course = models.ForeignKey(Course, verbose_name='Curso', related_name='enrollments')
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=1, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)


    def active(self):
        self.status = 1
        self.save()


    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'

        # unique_together => index de unicidade, ou seja, só pode existir uma inscrição para cada usuário e curso
        unique_together = (('user', 'course'),)
