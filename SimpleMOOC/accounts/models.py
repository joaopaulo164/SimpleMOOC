# coding=utf-8

import re # módulo Regex do python

from django.db import models
from django.core import validators # para criar validações dos campos do modelo
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)

# Create your models here.

# Custom User (Customização do usuário)

# AbstractBaseUser => lógica básica (senha, último login e des/criptografar senha e etc)
# PermissionsMixin => segurança, permissão e grupos
# UserManager => Manager base (User.objects)

class User(AbstractBaseUser, PermissionsMixin):

    # validação do campo por Regex
    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
        'O nome de usuário só pode conter letras, digitos ou o seguinte caracteres @/./+/-/_', 'invalid')]
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True) # Necessário para Admin do Django (usuário padrão)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False) # Necessário para Admin do Django (acessar a área administrativa)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True) # Necessário para Admin do Django

    objects = UserManager() # manager para classe (com funções uteis já estabelecidas)

    # Campos necessários para compatibilidade do Django
    USERNAME_FIELD = 'username' # campo único para referência do login (poderia ser email)
    REQUIRED_FIELDS = ['email'] # necessário para criação de super usuários

    # representação STRING do objeto
    def __str__(self):
        return self.name or self.username

    # necessário para o bom funcionamento do Admin
    def get_short_name(self):
        return self.username

    # necessário para o bom funcionamento do Admin
    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'