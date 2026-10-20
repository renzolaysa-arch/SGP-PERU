import smtplib
from unittest.mock import patch

from django.core import mail
from django.test import SimpleTestCase, override_settings

from notifications.functions import notify_email


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    EMAIL_HOST_USER='notificaciones@ejemplo.gob.pe',
    SITE_URL='https://sgp.ejemplo.gob.pe/',
)
class NotifyEmailTests(SimpleTestCase):
    def send(self, country='pe', link='https://sgp.ejemplo.gob.pe/usuario/activate-token/abc'):
        notify_email('Activa tu cuenta', 'Para activar su cuenta es necesario hacer clic',
                     'persona@entidad.gob.pe', 'Activa tu cuenta', link, country)
        return mail.outbox[-1]

    def test_sender_uses_name_and_angle_brackets(self):
        message = self.send()

        self.assertEqual(message.message()['From'],
                         'Alertas y Notificaciones <notificaciones@ejemplo.gob.pe>')

    def test_plain_text_includes_the_link(self):
        message = self.send()

        self.assertIn('https://sgp.ejemplo.gob.pe/usuario/activate-token/abc', message.body)
        self.assertNotIn('@import', message.body)

    def test_footer_depends_on_country(self):
        peru = self.send(country='pe').alternatives[0][0]
        colombia = self.send(country='co').alternatives[0][0]

        self.assertIn('INEI | Instituto Nacional de Estadística e Informática', peru)
        self.assertNotIn('DANE | Departamento', peru)
        self.assertIn('DANE | Departamento administrativo nacional de estadística', colombia)

    def test_smtp_failure_is_logged_instead_of_hidden(self):
        with patch('notifications.functions.mail.send_mail', side_effect=smtplib.SMTPException('rechazado')), \
                self.assertLogs('notifications.functions', level='ERROR') as logs:
            sent = notify_email('Asunto', 'Cuerpo', 'persona@entidad.gob.pe', None, None, 'pe')

        self.assertEqual(sent, 0)
        self.assertIn('Asunto', logs.output[0])

    def test_smtp_failure_raises_when_not_silent(self):
        with patch('notifications.functions.mail.send_mail', side_effect=smtplib.SMTPException('rechazado')):
            with self.assertRaises(smtplib.SMTPException):
                notify_email('Asunto', 'Cuerpo', 'persona@entidad.gob.pe', None, None, 'pe', fail_silently=False)
