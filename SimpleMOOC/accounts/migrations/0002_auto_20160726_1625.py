# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('key', models.CharField(max_length=100, verbose_name='Chave', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('confirmed', models.BooleanField(default=False, verbose_name='Confirmado')),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name_plural': 'Novas Senhas',
                'verbose_name': 'Nova Senha',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'O nome de usuário só pode conter letras, digitos ou o seguinte caracteres @/./+/-/_', 'invalid')], max_length=30, verbose_name='Nome de Usuário', unique=True),
        ),
        migrations.AddField(
            model_name='passwordreset',
            name='user',
            field=models.ForeignKey(verbose_name='Usuário', to=settings.AUTH_USER_MODEL),
        ),
    ]
