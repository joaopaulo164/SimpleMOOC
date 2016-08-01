# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20160729_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.TextField(verbose_name='Descrição', blank=True)),
                ('number', models.IntegerField(verbose_name='Número (ordem)', default=0)),
                ('release_date', models.DateField(null=True, verbose_name='Data de liberação', blank=True)),
                ('created_at', models.DateTimeField(verbose_name='Criado em', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('course', models.ForeignKey(related_name='lessons', to='courses.Course', verbose_name='Courso')),
            ],
            options={
                'verbose_name': 'Aula',
                'verbose_name_plural': 'Aulas',
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('embedded', models.TextField(verbose_name='Vídeo embedded', blank=True)),
                ('file', models.FileField(null=True, upload_to='lessons/materials', blank=True)),
                ('lesson', models.ForeignKey(related_name='materials', to='courses.Lesson', verbose_name='Aula')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materiais',
            },
        ),
        migrations.AlterField(
            model_name='announcement',
            name='course',
            field=models.ForeignKey(related_name='announcements', to='courses.Course', verbose_name='Curso'),
        ),
    ]
