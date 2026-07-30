from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core import mail
from django.conf import settings


def notify_email(subject,
                 body,
                 to,
                 name_link,
                 link,
                 country
                 ):
    subject = subject
    html_message = render_to_string(
        'notifications/message.html', {'body': body, 'name_link': name_link, 'link': link, 'country': country, 'url': settings.SITE_URL})
    plain_message = strip_tags(html_message)
    from_email = 'Alertas y Notificaciones ' + settings.EMAIL_HOST_USER
    to = to

    try:
        mail.send_mail(subject, plain_message, from_email,
                       [to], html_message=html_message)
    except:
        print("Error al enviar correo")
