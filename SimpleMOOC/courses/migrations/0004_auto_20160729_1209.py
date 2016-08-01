# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_auto_20160727_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('content', models.TextField(verbose_name='Conteúdo')),
                ('created_at', models.DateTimeField(verbose_name='Criado em', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('course', models.ForeignKey(to='courses.Course', verbose_name='Curso')),
            ],
            options={
                'verbose_name_plural': 'Anúncios',
                'ordering': ['-created_at'],
                'verbose_name': 'Anúncio',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('comment', models.TextField(verbose_name='Comentário')),
                ('created_at', models.DateTimeField(verbose_name='Criado em', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('announcement', models.ForeignKey(related_name='comments', to='courses.Announcement', verbose_name='Anúncio')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Usúario')),
            ],
            options={
                'verbose_name_plural': 'Comentários',
                'ordering': ['created_at'],
                'verbose_name': 'Comentário',
            },
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pendente'), (1, 'Aprovado'), (2, 'Cancelado')], default=1, verbose_name='Situação', blank=True),
        ),
    ]
