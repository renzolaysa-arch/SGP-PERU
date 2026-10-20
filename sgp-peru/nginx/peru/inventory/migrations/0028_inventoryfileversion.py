from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def preserve_current_files(apps, schema_editor):
    Inventory = apps.get_model('inventory', 'Inventory')
    Version = apps.get_model('inventory', 'InventoryFileVersion')
    database = schema_editor.connection.alias
    for item in Inventory.objects.using(database).exclude(file_example_sample_data='').exclude(file_example_sample_data__isnull=True).iterator():
        Version.objects.using(database).get_or_create(
            inventory_id=item.pk, file=item.file_example_sample_data.name,
            defaults={'original_name': item.file_example_sample_data.name.rsplit('/', 1)[-1]},
        )


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0027_alter_inventory_document_choice_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='InventoryFileVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to='uploads/sample-data/versions')),
                ('original_name', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(blank=True, null=True)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_versions', to='inventory.inventory')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-id'], 'verbose_name': 'Versión de archivo de RRAA', 'verbose_name_plural': 'Versiones de archivos de RRAA'},
        ),
        migrations.AddConstraint(model_name='inventoryfileversion', constraint=models.UniqueConstraint(fields=('inventory', 'file'), name='unique_inventory_file_version')),
        migrations.RunPython(preserve_current_files, migrations.RunPython.noop),
    ]
