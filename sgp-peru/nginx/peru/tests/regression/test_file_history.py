import tempfile
from datetime import timedelta
from pathlib import Path
from django.conf import settings
from django.test import TestCase, override_settings
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.forms import modelform_factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from inventory.models import Inventory, InventoryFileVersion, TypeFormatSampleData
from inventory.file_versions import save_with_history
from users.models import Provider, Functionary, AccessUserRRA
from providers.models import ProviderEntity, ProviderSector, ProviderStatus, ProviderType


class FileHistoryTests(TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        settings_override = override_settings(MEDIA_ROOT=self.folder.name)
        settings_override.enable()
        self.addCleanup(settings_override.disable)
        Site.objects.get_or_create(pk=settings.SITE_ID, defaults={'domain': 'testserver', 'name': 'Peru'})
        self.user = User.objects.create_user('proveedor@example.test')
        self.user.groups.add(Group.objects.create(name='Proveedor'))
        self.entity = ProviderEntity.objects.create(name='Entidad', description='Prueba',
            sector=ProviderSector.objects.create(name='Sector'), type=ProviderType.objects.create(name='Ministerio'),
            status=ProviderStatus.objects.create(name='Activo'))
        Provider.objects.create(user=self.user, entity_provider=self.entity)
        self.format = TypeFormatSampleData.objects.create(type_format='.csv')
        self.form_class = modelform_factory(Inventory, fields=['title', 'type_format_data_asociate', 'file_example_sample_data'])

    def save(self, item=None, content=b'a,b\n1,2\n', title='RRAA'):
        files = {} if content is None else {'file_example_sample_data': SimpleUploadedFile('datos.csv', content, content_type='text/csv')}
        form = self.form_class({'title': title, 'type_format_data_asociate': self.format.pk}, files=files, instance=item)
        self.assertTrue(form.is_valid(), form.errors)
        return save_with_history(form, self.user, self.entity)

    def test_replacing_same_filename_preserves_both_contents_and_authorship(self):
        item = self.save()
        old = item.file_example_sample_data.name
        self.save(item, b'a,b\n3,4\n')
        self.assertNotEqual(old, item.file_example_sample_data.name)
        self.assertEqual(item.file_versions.count(), 2)
        self.assertEqual(Path(self.folder.name, old).read_bytes(), b'a,b\n1,2\n')
        self.assertEqual(Path(item.file_example_sample_data.path).read_bytes(), b'a,b\n3,4\n')
        self.assertTrue(all(v.uploaded_by == self.user and v.uploaded_at for v in item.file_versions.all()))

    def test_editing_metadata_creates_no_version(self):
        item = self.save()
        self.save(item, content=None, title='Título corregido')
        self.assertEqual(item.file_versions.count(), 1)

    def test_legacy_file_is_preserved_without_inventing_date_or_author(self):
        item = Inventory.objects.create(title='Anterior', entity_provider=self.entity, type_format_data_asociate=self.format,
                                        file_example_sample_data=SimpleUploadedFile('anterior.csv', b'a\n1\n'))
        old = item.file_example_sample_data.name
        self.save(item)
        legacy = item.file_versions.get(file=old)
        self.assertIsNone(legacy.uploaded_at)
        self.assertIsNone(legacy.uploaded_by)
        self.assertEqual(item.file_versions.count(), 2)

    def test_data_migration_preserves_existing_reference_idempotently(self):
        from importlib import import_module
        from types import SimpleNamespace
        from django.apps import apps
        from django.db import connection
        item = Inventory.objects.create(title='Anterior', file_example_sample_data='uploads/sample-data/existente.csv')
        migrate = import_module('inventory.migrations.0028_inventoryfileversion').preserve_current_files
        migrate(apps, SimpleNamespace(connection=connection))
        migrate(apps, SimpleNamespace(connection=connection))
        version = InventoryFileVersion.objects.get(inventory=item)
        self.assertEqual(version.file.name, 'uploads/sample-data/existente.csv')
        self.assertIsNone(version.uploaded_at)
        self.assertIsNone(version.uploaded_by)

    def test_owner_can_list_and_download_previous_version(self):
        item = self.save()
        self.save(item, b'a\n3\n')
        self.client.force_login(self.user)
        response = self.client.get('/historial-archivos/%s/' % item.pk)
        self.assertContains(response, 'Vigente')
        self.assertContains(response, 'Anterior')
        version = item.file_versions.last()
        response = self.client.get('/historial-archivos/%s/%s/descargar/' % (item.pk, version.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b''.join(response.streaming_content), b'a,b\n1,2\n')

    def test_other_provider_cannot_read_history_or_edit_record(self):
        item = self.save()
        other = User.objects.create_user('otro@example.test')
        other.groups.add(Group.objects.get(name='Proveedor'))
        Provider.objects.create(user=other)
        self.client.force_login(other)
        self.assertEqual(self.client.get('/historial-archivos/%s/' % item.pk).status_code, 403)
        self.assertEqual(self.client.get('/editar-inventario/%s' % item.pk).status_code, 403)
        version = item.file_versions.first()
        self.assertEqual(self.client.get('/historial-archivos/%s/%s/descargar/' % (item.pk, version.pk)).status_code, 403)

    def test_expired_functionary_access_does_not_allow_history(self):
        item = self.save()
        user = User.objects.create_user('funcionario@example.test')
        functionary = Functionary.objects.create(user=user)
        AccessUserRRA.objects.create(user=functionary, inventory=item, date_limit=timezone.localdate()-timedelta(days=1))
        self.client.force_login(user)
        self.assertEqual(self.client.get('/historial-archivos/%s/' % item.pk).status_code, 403)
