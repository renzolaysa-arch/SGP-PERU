from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase, override_settings

from notifications.models import Notification
from notifications.services import (
    create_notifications_and_send_emails_async,
)


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    EMAIL_HOST_USER='notificaciones@example.com',
)
class InventoryAsyncEmailTests(TestCase):
    @patch('notifications.services._email_executor.submit')
    def test_inventory_email_is_dispatched_outside_the_request(self, submit):
        site, _ = Site.objects.update_or_create(
            id=settings.SITE_ID,
            defaults={'domain': 'example.com', 'name': 'SGP'},
        )
        user = User.objects.create_user(
            username='provider@example.com',
            email='provider@example.com',
        )

        created = create_notifications_and_send_emails_async([
            Notification(
                name='Registro actualizado',
                sent_to=user,
                module_from='IN',
                message='Se editó el registro administrativo',
                name_link='Consultar registro administrativo',
                link='https://example.com/detalle-inventario/1',
                site=site,
            )
        ])

        self.assertEqual(len(created), 1)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

        submit.assert_called_once()
        email_sender, email_payloads = submit.call_args.args
        email_sender(email_payloads)

        self.assertEqual(len(mail.outbox), 1)
