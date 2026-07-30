from inventory.models import InventoryTheme, InventoryThematic, InventoryStatus, TypeFormatSampleData, TransferMediumSampleData, TagsSampleData, VariablesSampleData, Inventory, CommentInventory, QualityTest
from tests.flow.relations_inventory import ThemeInventory,  ThematicInventory, StatusInventory, TypeFormatSample, TransferMediumSample, TagsSample, VariablesSample 
import pytest

from faker import Faker
import random

fake = Faker()
fake.add_provider(ThemeInventory)
fake.add_provider(ThematicInventory)
fake.add_provider(StatusInventory)
fake.add_provider(TypeFormatSample)
fake.add_provider(TransferMediumSample)
fake.add_provider(TagsSample)
fake.add_provider(VariablesSample)

@pytest.fixture
def theme_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name_theme_inventory", fake.theme_inventory())
        # same for other fields
        return InventoryTheme.on_site.create(**kwargs)
    return factory

@pytest.fixture
def thematic_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name_thematic_inventory", fake.thematic_inventory())
        # same for other fields
        return InventoryThematic.on_site.create(**kwargs)
    return factory

@pytest.fixture
def status_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name", fake.status_inventory())
        # same for other fields
        return InventoryStatus.on_site.create(**kwargs)
    return factory

@pytest.fixture
def type_format(db):
    def factory(**kwargs):
        kwargs.setdefault("type_format", fake.type_format())
        # same for other fields
        return TypeFormatSampleData.on_site.create(**kwargs)
    return factory

@pytest.fixture
def transfer_medium(db):
    def factory(**kwargs):
        kwargs.setdefault("transfer_medium", fake.transfer_medium())
        # same for other fields
        return TransferMediumSampleData.on_site.create(**kwargs)
    return factory

@pytest.fixture
def tags_sample(db):
    def factory(**kwargs):
        kwargs.setdefault("tags_sample_data", fake.tags_sample())
        # same for other fields
        return TagsSampleData.on_site.create(**kwargs)
    return factory

@pytest.fixture
def variable_sample(db):
    def factory(**kwargs):
        kwargs.setdefault("variables_sample_data", fake.variable_sample())
        # same for other fields
        return VariablesSampleData.on_site.create(**kwargs)
    return factory

@pytest.fixture
def inventory_factory(theme_factory, thematic_factory, status_factory, type_format, transfer_medium, tags_sample, variable_sample):
    def factory(**kwargs):
        type_file = type_format()
        tags = tags_sample()
        variables= variable_sample()

        kwargs.setdefault("title", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("objective", fake.paragraph(5))
        kwargs.setdefault("inventory_theme_asociate", theme_factory())
        kwargs.setdefault("inventory_thematic_asociate", thematic_factory())
        kwargs.setdefault("use_laws_decrees", random.choice(['C.P', 'L', 'D.N']))
        kwargs.setdefault("document_choice", random.choice(['M.D', 'D.D', 'D.S']))
        kwargs.setdefault("nomenclature_choice", random.choice(['Si', 'No']))
        kwargs.setdefault("method_collections_choice", random.choice(['F.F', 'F.E', 'D.C']))
        kwargs.setdefault("frequency_choice", random.choice(['F.F', 'F.E', 'D.C']))       
        kwargs.setdefault("processing_choice", random.choice(['E', 'A', 'R']))
        kwargs.setdefault("record_choice", random.choice(['S', 'N']))
        kwargs.setdefault("dependence_name", fake.bs())
        kwargs.setdefault("director_name", fake.first_name()) 
        kwargs.setdefault("security_choice", random.choice(['Backups', 'Aislamiento del servidor', 'Utilización de perfiles']))
        kwargs.setdefault("information_stored_choice", random.choice(['Si', 'No']))
        kwargs.setdefault("information_choice", random.choice(['Anual', 'Semestral', 'Bimensual', 'Trimestral']))
        kwargs.setdefault("type_format_data_asociate", type_file)
        kwargs.setdefault("file_example_sample_data", fake.file_name(extension=type_file))
        kwargs.setdefault("transfer_medium_data_asociate", transfer_medium())

        inventory = Inventory.on_site.create(**kwargs)
        inventory.tag_sample_data_asociate.add(tags)
        inventory.variables_sample_data_asociate.add(variables)
        return inventory
    return factory


@pytest.mark.django_db
def test_inventory_factory(db, inventory_factory):
    inventory = inventory_factory()
    assert inventory.id == 1

