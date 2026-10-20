import logging
from email.utils import formataddr

from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core import mail
from django.conf import settings


logger = logging.getLogger(__name__)

SENDER_NAME = 'Alertas y Notificaciones'


def get_from_email():
    """Remitente con el formato Nombre <correo>; sin los < > el servidor recibe una direccion invalida."""
    return formataddr((SENDER_NAME, settings.EMAIL_HOST_USER))


def notify_email(subject,
                 body,
                 to,
                 name_link,
                 link,
                 country,
                 connection=None,
                 fail_silently=True,
                 ):
    html_message = render_to_string(
        'notifications/message.html', {'body': body, 'name_link': name_link, 'link': link, 'country': country, 'url': settings.SITE_URL})
    # Texto plano propio: strip_tags del HTML perdia el enlace y dejaba el CSS
    plain_message = strip_tags(body)
    if link:
        plain_message += '\n\n' + (name_link or 'Enlace') + ': ' + link

    try:
        return mail.send_mail(
            subject,
            plain_message,
            get_from_email(),
            [to],
            html_message=html_message,
            connection=connection,
            fail_silently=False,
        )
    except Exception:
        if not fail_silently:
            raise
        logger.exception('No se pudo enviar el correo "%s" a %s', subject, to)
        return 0
