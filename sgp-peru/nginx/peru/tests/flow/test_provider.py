
from providers.models import ProviderEntity, ProviderStatus, ProviderTopic, ProviderCategory, ProviderType, ProviderDocuments, ProviderSector, Stage
from tests.flow.relations_entity_provider import StatusEntity, TypeEntity, DomainEntity, SectorEntity
import pytest
import re
from faker import Faker
import random

fake = Faker()
fake.add_provider(SectorEntity)
fake.add_provider(TypeEntity)
fake.add_provider(DomainEntity)
fake.add_provider(StatusEntity)


@pytest.fixture
def sector_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name", fake.type_sector())
        # same for other fields
        return ProviderSector.objects.create(**kwargs)
    return factory

@pytest.fixture
def type_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name", fake.type_entity())
        # same for other fields
        return ProviderType.objects.create(**kwargs)
    return factory

@pytest.fixture
def status_prov_factory(db):
    def factory(**kwargs):
        kwargs.setdefault("name", fake.status())
        # same for other fields
        return ProviderStatus.objects.create(**kwargs)
    return factory

@pytest.fixture
def entity_factory(db, sector_factory, type_factory, status_prov_factory):  # see how i injected `category_factory`
    def factory(**kwargs):
        kwargs.setdefault("name", fake.first_name())
        kwargs.setdefault("identification_number", random.randint(1000,1050))
        kwargs.setdefault("description", fake.last_name())
        kwargs.setdefault("sector", sector_factory())
        kwargs.setdefault("type", type_factory())
        kwargs.setdefault("image", fake.file_extension(category='image'))
        kwargs.setdefault("domain", fake.domain())
        kwargs.setdefault("status", status_prov_factory()) 
        # same for other fields
        return ProviderEntity.on_site.create(**kwargs)
    return factory

@pytest.mark.django_db
def test_entity_creation(db, entity_factory):
    product = entity_factory()
    assert product.id == 1


@pytest.mark.django_db
def test_entity_creation_fail(db):
    def factory(**kwargs):
        with pytest.raises(Exception):
            kwargs.setdefault("name", fake.first_name())
            return ProviderEntity.on_site.create(**kwargs)
    return factory


