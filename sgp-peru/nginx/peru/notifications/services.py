from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.core import mail

from notifications.functions import notify_email
from notifications.models import Notification


_email_executor = ThreadPoolExecutor(
    max_workers=2,
    thread_name_prefix='notification-email',
)


def _send_notification_emails(email_payloads):
    try:
        with mail.get_connection(
            timeout=getattr(settings, 'EMAIL_TIMEOUT', 10),
        ) as connection:
            for payload in email_payloads:
                notify_email(
                    'Alertas y Notificaciones',
                    payload['message'],
                    payload['email'],
                    payload['name_link'],
                    payload['link'],
                    settings.COUNTRY,
                    connection=connection,
                    fail_silently=True,
                )
    except Exception:
        pass


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
