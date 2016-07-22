from django.template.loader import render_to_string
from django.template.defaultfilters import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# função generica para envio e e-mail
def send_mail_template(subject, template_name, context, recipient_list,
                       from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):

    message_html = render_to_string(template_name, context) # renderiza em formato texto

    message_txt = strip_tags(message_html) # remove as tags o html

    # EmailMultiAlternatives é utilizado para enviar uma alternativa em html
    email = EmailMultiAlternatives(subject=subject, body=message_txt, from_email=from_email, to=recipient_list)

    email.attach_alternative(message_html, "text/html")
    email.send(fail_silently=fail_silently)