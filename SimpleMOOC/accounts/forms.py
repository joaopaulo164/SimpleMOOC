# coding=utf-8

__author__ = 'john'

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Customizando o UserCreationForm
class RegisterForm(UserCreationForm):

    email = forms.EmailField(label='E-mail')

    # função para verificar se o e-mail já foi cadastrado
    def clean_email(self):
        email = self.cleaned_data['email'] # retorna o e-mail passado pelo Form
        if User.objects.filter(email=email).exists(): # Queryset que verifica se o email já foi cadastrado no banco, exists() True ou False
            raise forms.ValidationError('Já existe usuário com este e-mail') # Lançando uma exeção
        return email

    # Reescrevendo o metodo save() do UserCreationForm
    def save(self, commit=True):
        # chama o save() do UserCreationForm (que também chama o save() do Model User)
        user = super(RegisterForm, self).save(commit=False) # commit = False para não salvar e será retornado um usuário
        user.email = self.cleaned_data['email'] # adiciona o campo email, vindo do Form, no usuário
        if commit:
            user.save()
        return user
