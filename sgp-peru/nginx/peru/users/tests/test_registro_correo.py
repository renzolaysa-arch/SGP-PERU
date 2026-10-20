from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings

from notifications.models import Notification
from providers.models import ProviderEntity, ProviderSector, ProviderStatus, ProviderType
from users.models import Provider, Unit_Central


SIGNUP_URL = '/usuario/crear/'


@override_settings(SITE_URL='https://sgp.ejemplo.gob.pe/')
@patch('captcha.fields.ReCaptchaField.validate', lambda self, value: None)
class ProviderSignupEmailTests(TestCase):
    def setUp(self):
        Site.objects.get_or_create(id=settings.SITE_ID, defaults={'domain': 'testserver', 'name': 'Prueba'})
        Group.objects.create(name='Proveedor')
        head = User.objects.create_user('unidad@ejemplo.gob.pe', 'unidad@ejemplo.gob.pe', 'Clave2026segura')
        Unit_Central.objects.create(user=head)
        self.entity = ProviderEntity.objects.create(
            name='Entidad de prueba', identification_number=1, description='Prueba',
            sector=ProviderSector.objects.create(name='Sector'),
            type=ProviderType.objects.create(name='Tipo'),
            status=ProviderStatus.objects.create(name='Activo'),
            domain='entidad.gob.pe',
        )

    def signup(self, email):
        data = {
            'name': 'Ana', 'last_name': 'Pérez', 'document_type': 'CC', 'identification_number': '12345678',
            'email': email, 'password': 'Clave2026segura', 'password_confirm': 'Clave2026segura',
            'g-recaptcha-response': 'x',
        }
        with patch('users.views.notify_email', return_value=1) as send_email, \
                patch('notifications.services._email_executor.submit') as submit:
            response = self.client.post(SIGNUP_URL, data)
        return response, send_email, submit

    def test_entity_domain_sends_activation_link(self):
        response, send_email, submit = self.signup('Ana@Entidad.gob.pe')

        provider = Provider.objects.get(user__username='Ana@Entidad.gob.pe')
        self.assertFalse(provider.user.is_active)
        self.assertEqual(provider.entity_provider, self.entity)
        self.assertTrue(provider.valid_data)
        self.assertTrue(provider.hash)
        send_email.assert_called_once()
        subject, _, to, _, link = send_email.call_args.args[:5]
        self.assertEqual(subject, 'Activa tu cuenta')
        self.assertEqual(to, 'Ana@entidad.gob.pe')
        self.assertEqual(link, 'https://sgp.ejemplo.gob.pe/usuario/activate-token/' + provider.hash + '/')
        self.assertEqual(response['Location'], '/usuario/crear/')
        self.assertEqual(Notification.objects.filter(module_from='PRV').count(), 1)
        submit.assert_called_once()

    def test_other_domain_waits_for_central_unit(self):
        response, send_email, _ = self.signup('ana@otro-dominio.org')

        provider = Provider.objects.get(user__username='ana@otro-dominio.org')
        self.assertIsNone(provider.entity_provider)
        self.assertFalse(provider.valid_data)
        self.assertEqual(provider.hash, '')
        self.assertEqual(send_email.call_args.args[0], 'Nuevo proveedor')
        self.assertEqual(response['Location'], '/usuario/crear/')

    def test_invalid_email_shows_form_errors(self):
        response, send_email, _ = self.signup('ana@minsa')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='ana@minsa').exists())
        send_email.assert_not_called()

    def test_duplicate_email_ignores_case(self):
        self.signup('ana@otro-dominio.org')
        response, send_email, _ = self.signup('ANA@otro-dominio.org')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username__iexact='ana@otro-dominio.org').count(), 1)
        send_email.assert_not_called()

    def test_activation_link_can_be_opened_twice(self):
        self.signup('ana@entidad.gob.pe')
        provider = Provider.objects.get(user__username='ana@entidad.gob.pe')
        link = '/usuario/activate-token/%s/' % provider.hash

        first = self.client.get(link)
        second = self.client.get(link)

        provider.refresh_from_db()
        self.assertTrue(provider.user.is_active)
        self.assertEqual(provider.hash, '')
        self.assertEqual(first['Location'], '/usuario/ingresar')
        self.assertEqual(second['Location'], '/usuario/ingresar')

    def test_resend_token_requires_central_unit(self):
        self.signup('ana@entidad.gob.pe')
        provider = Provider.objects.get(user__username='ana@entidad.gob.pe')

        with patch('users.views.notify_email', return_value=1) as send_email:
            response = self.client.get('/usuario/envio-token/%s/' % provider.id)

        self.assertEqual(response['Location'], '/usuario/ingresar/')
        send_email.assert_not_called()

    def test_smtp_failure_preserves_account_and_reports_error(self):
        from smtplib import SMTPException
        with patch('users.views.notify_email', side_effect=SMTPException('SMTP rejected')), \
                patch('notifications.services._email_executor.submit'):
            response = self.client.post(SIGNUP_URL, {
                'name': 'Ana', 'last_name': 'Pérez', 'document_type': 'CC', 'identification_number': '12345678',
                'email': 'ana@entidad.gob.pe', 'password': 'Clave2026segura', 'password_confirm': 'Clave2026segura',
                'g-recaptcha-response': 'x',
            }, follow=True)
        self.assertEqual(User.objects.filter(username='ana@entidad.gob.pe').count(), 1)
        self.assertContains(response, 'no se pudo enviar el correo')
        self.assertContains(response, 'Reenviar correo de registro')

    def test_resend_is_real_and_limited_to_registration_session(self):
        self.signup('ana@entidad.gob.pe')
        with patch('users.views.notify_email', return_value=1) as send:
            self.client.post('/usuario/reenviar-registro/')
            send.assert_not_called()
            session = self.client.session
            session['registration_last_send'] = 0
            session.save()
            self.client.post('/usuario/reenviar-registro/')
            send.assert_called_once()
        self.assertEqual(User.objects.filter(username='ana@entidad.gob.pe').count(), 1)

    def test_other_browser_cannot_resend_by_posting_provider_id(self):
        from django.test import Client
        self.signup('ana@entidad.gob.pe')
        provider = Provider.objects.get(user__username='ana@entidad.gob.pe')
        with patch('users.views.notify_email') as send:
            Client().post('/usuario/reenviar-registro/', {'provider_id': provider.pk})
            send.assert_not_called()

    def test_resend_requires_post(self):
        self.assertEqual(self.client.get('/usuario/reenviar-registro/').status_code, 405)
