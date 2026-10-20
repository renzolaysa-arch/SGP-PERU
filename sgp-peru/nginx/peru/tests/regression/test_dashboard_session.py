from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.conf import settings
from users.models import Functionary


class DashboardSessionTests(TestCase):
    def setUp(self):
        Site.objects.get_or_create(pk=settings.SITE_ID, defaults={'domain': 'testserver', 'name': 'Peru'})
        self.user = User.objects.create_user('funcionario@example.test', password='Test1234')
        self.user.groups.add(Group.objects.create(name='Funcionario'))
        Functionary.objects.create(user=self.user)

    def test_expired_ajax_request_returns_401_instead_of_profile_lookup_error(self):
        response = self.client.get('/usuario/notificaciones-funcionario/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['error'], 'session_expired')
        self.assertEqual(response.json()['login_url'], '/usuario/ingresar/')

    def test_normal_unauthenticated_navigation_redirects_to_login(self):
        response = self.client.get('/usuario/tablero-actividades/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/usuario/ingresar/')

    def test_wrong_role_has_distinct_ajax_response(self):
        self.client.force_login(self.user)
        response = self.client.get('/usuario/dashboard/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], 'permission_denied')

    def test_authorized_notifications_are_not_cached(self):
        self.client.force_login(self.user)
        response = self.client.get('/usuario/notificaciones-funcionario/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn('no-store', response['Cache-Control'])

    def test_logout_is_idempotent_and_invalidates_the_other_tab(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get('/usuario/logout')['Location'], '/')
        self.assertEqual(self.client.get('/usuario/logout')['Location'], '/')
        response = self.client.get('/usuario/notificaciones-funcionario/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 401)
