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


class EditAccountForm(forms.ModelForm): # forms.ModelForm => utiliza todos os campos do Modelo para gerar o Form

    # função para verificar se o e-mail já foi cadastrado
    def clean_email(self):

        # retorna o e-mail passado pelo Form
        email = self.cleaned_data['email']

        # Verifica se o email já foi cadastrado no banco
        # exclude() exclui da Queryset o registro com PK igual da instância atual (pk=self.instance.pk)
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)

        # exists() True ou False
        if queryset.exists():
            raise forms.ValidationError('Já existe usuário com este e-mail') # Lançando uma exeção
        return email

    class Meta: # Obrigatório
        model = User # Diz para o ModelForm qual o Model (User) utilizar
        fields = ['username', 'email', 'first_name', 'last_name'] # campos que serão alterados