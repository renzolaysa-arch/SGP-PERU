from django.test import TestCase
from django.conf import settings
from django.contrib.sites.models import Site
from providers.models import ProviderEntity, ProviderSector, ProviderStatus, ProviderType
from inventory.filters import InventoryFilter
from inventory.models import Inventory


class InventorySearchTests(TestCase):
    def setUp(self):
        Site.objects.get_or_create(pk=settings.SITE_ID, defaults={'domain': 'testserver', 'name': 'Peru'})
        entity = ProviderEntity.objects.create(
            name='Ministerio de Educación - MINEDU', description='Prueba',
            sector=ProviderSector.objects.create(name='Sector'),
            status=ProviderStatus.objects.create(name='Activo'),
            type=ProviderType.objects.create(name='Ministerio'),
        )
        self.item = Inventory.objects.create(title='Alumnos matriculados', entity_provider=entity)
        self.other = Inventory.objects.create(title='Estadísticas sanitarias')

    def search(self, text, queryset=None):
        return InventoryFilter({'title': text}, queryset=queryset if queryset is not None else Inventory.on_site.all()).qs

    def test_provider_name_is_searchable_without_title_match(self):
        self.assertEqual(list(self.search(' minedu ')), [self.item])

    def test_title_search_still_works(self):
        self.assertEqual(list(self.search('MATRICULADOS')), [self.item])

    def test_search_preserves_existing_queryset_restrictions(self):
        self.assertFalse(self.search('MINEDU', Inventory.objects.filter(pk=self.other.pk)).exists())

    def test_blank_query_preserves_results(self):
        self.assertEqual(self.search('   ').count(), 2)

    def test_no_match_is_empty(self):
        self.assertFalse(self.search('Proveedor inexistente').exists())
