from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import RequestFactory, SimpleTestCase

from inventory.views import inventory_create


class InventoryCreateAsyncNotificationTests(SimpleTestCase):
    def test_creation_dispatches_notification_emails_asynchronously(self):
        request = RequestFactory().post(
            '/crear-registro-administrativo/',
            {'title': 'Inventario de prueba'},
        )
        request.user = SimpleNamespace(id=7, groups=Mock())
        request.user.groups.filter.return_value.exists.return_value = True

        entity_provider = SimpleNamespace(id=11)
        provider = SimpleNamespace(entity_provider=entity_provider)
        inventory = Mock()
        form = Mock()
        form.is_valid.return_value = True
        form.save.return_value = inventory
        form.instance.id = 23
        recipient = User(id=7, email='provider@example.com')

        with patch('inventory.views.CreateInventoryForm', return_value=form), \
                patch('inventory.views.Provider.objects.get', return_value=provider), \
                patch('inventory.views.ProviderEntity.objects.get', return_value=entity_provider), \
                patch('inventory.views.Unit_Central.on_site.all', return_value=[]), \
                patch('inventory.views.Functionary.on_site.all', return_value=[]), \
                patch('inventory.views.User.objects.filter', return_value=[recipient]), \
                patch('inventory.views.get_current_site', return_value=SimpleNamespace(id=1)), \
                patch('inventory.views.create_notifications_and_send_emails_async') as dispatch, \
                patch('inventory.views.redirect', return_value='redirected'):
            response = inventory_create(request)

        self.assertEqual(response, 'redirected')
        dispatch.assert_called_once()
        notifications = dispatch.call_args.args[0]
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].sent_to, recipient)
        self.assertEqual(notifications[0].site_id, 1)
