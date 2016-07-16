# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição', blank=True)
    start_date = models.DateField('Data de Início', null=True, blank=True)
    image = models.ImageField(upload_to='courses/images', verbose_name='Imagem')   # upload_to = salva o caminho do arquivo (imagem)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)  # auto_now_add = preenche com a data de criação
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)   # auto_now = preenche com a data atual toda vez que for salvo (atualizado)