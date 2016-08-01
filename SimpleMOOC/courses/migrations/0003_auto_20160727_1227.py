# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_auto_20160720_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Pendente'), (1, 'Aprovado'), (2, 'Cancelado')], default=0, verbose_name='Situação')),
                ('created_at', models.DateTimeField(verbose_name='Criado em', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('course', models.ForeignKey(verbose_name='Curso', related_name='enrollments', to='courses.Course')),
                ('user', models.ForeignKey(verbose_name='Usuário', related_name='enrollments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Inscrições',
                'verbose_name': 'Inscrição',
            },
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('user', 'course')]),
        ),
    ]
