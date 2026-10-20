from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.conf import settings
from inventory.models import Inventory
from users.models import Functionary, Unit_Central
from demand.models import Demands, Transfer, Transfers, Preparation, Preparations, Negotiation, Evaluation, Channels
from demand.progress import preparation_progress
from unittest.mock import patch
from django.http import HttpResponse


class PreparationProgressTests(TestCase):
    def setUp(self):
        Site.objects.get_or_create(pk=settings.SITE_ID, defaults={'domain': 'testserver', 'name': 'Peru'})
        self.user = User.objects.create_user('central@example.test')
        self.user.groups.add(Group.objects.create(name='Unidad Central'))
        Unit_Central.objects.create(user=self.user)
        functionary = Functionary.objects.create(user=User.objects.create_user('funcionario@example.test'))
        self.demand = Demands.objects.create(title='Solicitud', functionary=functionary, inventory=Inventory.objects.create(title='RRAA'), project=None)
        Negotiation.objects.create(demand=self.demand)
        self.transfer = Transfer.objects.create(demand=self.demand)
        self.preparation = Preparation.objects.create(demand=self.demand, demand_process='fi')
        channel = Channels.objects.create(title='Correo')
        self.deliveries = [Transfers.objects.create(transfer=self.transfer, channel=channel, number_deliveries='Entrega %s' % n, finalize=True) for n in range(1, 4)]
        self.rows = [Preparations.objects.create(preparation=self.preparation, transfer=d, finalize=True) for d in self.deliveries[:2]]
        self.client.force_login(self.user)

    def test_two_of_three_shows_partial_and_names_pending_delivery(self):
        progress = preparation_progress(self.preparation, self.transfer)
        self.assertEqual(progress['percent'], 66)
        self.assertEqual(progress['completed'], 2)
        self.assertEqual(progress['status'], 'pr')
        self.assertEqual(progress['pending_deliveries'], ['Entrega 3'])

    def test_legacy_duplicate_preparations_do_not_inflate_progress(self):
        Preparations.objects.create(preparation=self.preparation, transfer=self.deliveries[0], finalize=True)
        self.assertEqual(preparation_progress(self.preparation, self.transfer)['percent'], 66)

    def test_all_unique_deliveries_prepared_is_100(self):
        Preparations.objects.create(preparation=self.preparation, transfer=self.deliveries[2], finalize=True)
        self.assertEqual(preparation_progress(self.preparation, self.transfer)['status'], 'fi')
        self.assertEqual(preparation_progress(self.preparation, self.transfer)['percent'], 100)

    def test_repeated_start_does_not_create_another_preparation(self):
        url = '/solicitud/%s/preparacion/inicio/' % self.demand.pk
        data = {'transfer': self.deliveries[0].pk, 'date': '2026-10-20', 'hour': '12:00', 'coments': 'Reintento'}
        self.client.post(url, data)
        self.client.post(url, data)
        self.assertEqual(Preparations.objects.filter(preparation=self.preparation, transfer=self.deliveries[0]).count(), 1)

    def test_no_deliveries_does_not_divide_by_zero(self):
        self.transfer.transfers_set.all().delete()
        self.assertEqual(preparation_progress(self.preparation, self.transfer)['percent'], 0)

    def test_consulting_each_preparation_screen_does_not_change_saved_state(self):
        for step in ['inicio', 'proceso', 'revision', 'finalizado']:
            with patch('demand.views.render', return_value=HttpResponse('ok')):
                response = self.client.get('/solicitud/%s/preparacion/%s/' % (self.demand.pk, step))
            self.assertEqual(response.status_code, 200)
            self.preparation.refresh_from_db()
            self.assertEqual(self.preparation.demand_process, 'fi')

    def test_finishing_one_delivery_allows_evaluation_but_keeps_pending_work(self):
        row = Preparations.objects.create(preparation=self.preparation, transfer=self.deliveries[2])
        # Another delivery is deliberately still pending.
        self.rows[0].finalize = False
        self.rows[0].save()
        response = self.client.post('/solicitud/%s/preparacion/finalizado/?preparation=%s' % (self.demand.pk, row.pk),
                                    {'date_finalize': '2026-10-20', 'hour_finalize': '12:00', 'coments_finalize': 'Listo'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Evaluation.objects.filter(demand=self.demand).exists())
        self.assertEqual(preparation_progress(self.preparation, self.transfer)['percent'], 66)
