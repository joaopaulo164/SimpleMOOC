# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from SimpleMOOC.core.mail import send_mail_template

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


class Lesson(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (ordem)', default=0)
    release_date = models.DateField('Data de liberação', blank=True, null=True)

    course = models.ForeignKey(Course, verbose_name='Courso', related_name='lessons')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class Material(models.Model):

    name = models.CharField('Nome', max_length=200)
    embedded = models.TextField('Vídeo embedded', blank=True)
    file = models.FileField(upload_to='lessons/materials', blank=True, null=True)

    lesson = models.ForeignKey(Lesson, verbose_name='Aula', related_name='materials')

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'


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


    # Muda o status para 1 = aprovado
    def active(self):
        self.status = 1
        self.save()


    # Retorna status = 1, se estiver aprovado
    def is_approved(self):
        return self.status == 1


    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'

        # unique_together => index de unicidade, ou seja, só pode existir uma inscrição para cada usuário e curso
        unique_together = (('user', 'course'),)



class Announcement(models.Model):

    course = models.ForeignKey(
        Course,
        verbose_name='Curso',
        related_name='announcements'
    )
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at'] # -created_at => decrescente



class Comment(models.Model):

    announcement = models.ForeignKey(
        Announcement,
        verbose_name='Anúncio',
        related_name='comments' # uma instância de Announcement terá uma relação comments que trará os seus comentários
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usúario')
    comment = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)


    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']


# Notifica por e-mail os usuários sobre novos anúncios dos cursos que eles estiveram cadastrados por meio dos SIGNAL
# Signal é um gatinho, neste caso utilizamos o signal.post_save() (disparado pós salvamento/criação do objeto)
def post_save_announcement(instance, created, **kwargs):

    # instance é o anúncio atual
    # created é um parâmetro do método pos_save (não nenessáriamente um objeto salvo foi criado naquele momento)
    # **kwargs é um dicionário de argumentos (argumentos nomeados), mas não será necessário no momento

    if created: # Executa se foi criado
        subjetc = instance.title
        context = {
            'announcement': instance # Adiciona o anúncio atual no contexto
        }
        template_name = 'courses/announcement_mail.html' # template do e-mail

        # retorna as inscrições do curso referente ao anúncio atual (instance) e que com status aprovado (status = 1)
        enrollments = Enrollment.objects.filter(course=instance.course, status=1)

        # para cada inscrição envia um e-mail
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subjetc, template_name, context, recipient_list)

# Indica quando o gatilho será disparado e a função post_save_announcement() será executada
models.signals.post_save.connect(
        post_save_announcement, # função que será executada
        sender=Announcement, # sender é quem envia, só será executada quando o Announcement (Anúncio) for o sender
        dispatch_uid='post_save_announcement' # evitar cadastrar a função mais de uma vez no SIGNAL (torna único)
)


