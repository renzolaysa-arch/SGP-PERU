import logging
from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.core import mail

from notifications.functions import notify_email
from notifications.models import Notification


logger = logging.getLogger(__name__)

_email_executor = ThreadPoolExecutor(
    max_workers=2,
    thread_name_prefix='notification-email',
)


def _send_notification_emails(email_payloads, subject='Alertas y Notificaciones'):
    try:
        with mail.get_connection(
            timeout=getattr(settings, 'EMAIL_TIMEOUT', 10),
        ) as connection:
            for payload in email_payloads:
                notify_email(
                    subject,
                    payload['message'],
                    payload['email'],
                    payload['name_link'],
                    payload['link'],
                    settings.COUNTRY,
                    connection=connection,
                    fail_silently=True,
                )
    except Exception:
        logger.exception('No se pudo abrir la conexion con el servidor de correo')


def send_email_async(subject, body, to, name_link=None, link=None):
    """Envia un correo suelto en segundo plano, sin hacer esperar a quien lo dispara."""
    payload = {'message': body, 'email': to, 'name_link': name_link, 'link': link}
    try:
        _email_executor.submit(_send_notification_emails, [payload], subject)
    except RuntimeError:
        logger.exception('No se pudo programar el envio del correo "%s"', subject)


def create_notifications_and_send_emails_async(notifications):
    """Create internal notifications and dispatch best-effort emails."""
    notifications = list(notifications)
    if not notifications:
        return []

    email_payloads = [
        {
            'message': notification.message,
            'email': notification.sent_to.email,
            'name_link': notification.name_link,
            'link': notification.link,
        }
        for notification in notifications
        if not notification.hidden
    ]

    created_notifications = Notification.objects.bulk_create(notifications)

    if email_payloads:
        try:
            _email_executor.submit(
                _send_notification_emails,
                email_payloads,
            )
        except RuntimeError:
            pass

    return created_notifications
