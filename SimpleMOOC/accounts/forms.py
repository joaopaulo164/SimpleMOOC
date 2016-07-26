# coding=utf-8

__author__ = 'john'

from django import forms
from django.contrib.auth.forms import UserCreationForm

# Utilizando o usuário Customizado
# Utilização dos forms do Django com o usuário customizado
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms

from django.contrib.auth import get_user_model

User = get_user_model() # usando o usuário do sistema (user customizado)


# No momento não exite a necessidade de usar ModelForm porque só teremos e-mail
class PasswordResetForm(forms.Form):

    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email'] # pega data do formulário
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Nenhum usuário foi encontrado com este e-mail!')




# Refatoração no RegisterForm porque ele não é mais compatível com o UserCreationForm (Olhar código comentado no final do arquivo)
class RegisterForm(forms.ModelForm):

    # email = forms.EmailField(label='E-mail') # não é mais necessário, pois está declarado na classe Meta => fields = ['username', 'email']
    # função para verificar se o e-mail já foi cadastrado (único) não é mais necessária, pois no usuário customizado ele já é único

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'A confirmação de senha mão está correta')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1']) # criptografa a senha vinda do formulário antes de salvar no banco
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name']


# Utilizando o usuário padrão do Django
#
# # from django.contrib.auth.models import User
#
# # Customizando o UserCreationForm
# class RegisterForm(UserCreationForm):
#
#     email = forms.EmailField(label='E-mail')
#
#     # função para verificar se o e-mail já foi cadastrado (único)
#     def clean_email(self):
#         email = self.cleaned_data['email'] # retorna o e-mail passado pelo Form
#         if User.objects.filter(email=email).exists(): # Queryset que verifica se o email já foi cadastrado no banco, exists() True ou False
#             raise forms.ValidationError('Já existe usuário com este e-mail') # Lançando uma exeção
#         return email
#
#     # Reescrevendo o metodo save() do UserCreationForm
#     def save(self, commit=True):
#         # chama o save() do UserCreationForm (que também chama o save() do Model User)
#         user = super(RegisterForm, self).save(commit=False) # commit = False para não salvar e será retornado um usuário
#         user.email = self.cleaned_data['email'] # adiciona o campo email, vindo do Form, no usuário
#         if commit:
#             user.save()
#         return user
#
#
# class EditAccountForm(forms.ModelForm): # forms.ModelForm => utiliza todos os campos do Modelo para gerar o Form
#
#     # função para verificar se o e-mail já foi cadastrado
#     def clean_email(self):
#
#         # retorna o e-mail passado pelo Form
#         email = self.cleaned_data['email']
#
#         # Verifica se o email já foi cadastrado no banco
#         # exclude() exclui da Queryset o registro com PK igual da instância atual (pk=self.instance.pk)
#         queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)
#
#         # exists() True ou False
#         if queryset.exists():
#             raise forms.ValidationError('Já existe usuário com este e-mail') # Lançando uma exeção
#         return email
#
#     class Meta: # Obrigatório
#         model = User # Diz para o ModelForm qual o Model (User) utilizar
#         fields = ['username', 'email', 'first_name', 'last_name'] # campos que serão alterados
#