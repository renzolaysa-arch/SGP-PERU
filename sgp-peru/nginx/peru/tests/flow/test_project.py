from projects.models import TagsProject, CategoryProject, RelatedStatistical, ThemeProject, StateProject, Project
from users.models import Functionary, User
import pytest
from tests.flow.test_inventory import *
from tests.flow.test_provider import *


from faker import Faker
import random

fake = Faker()


@pytest.fixture()
def tags_project(db):
    def factory(**kwargs):
        kwargs.setdefault("name_tag_project", fake.company())
        kwargs.setdefault("type_color_choice", random.choice(['red', 'blue', 'orange', 'gray']))
        # same for other fields
        return TagsProject.on_site.create(**kwargs)
    return factory

@pytest.fixture
def category_project(db):
    def factory(**kwargs):
        kwargs.setdefault("name_category_project", fake.company())
        # same for other fields
        return CategoryProject.on_site.create(**kwargs)
    return factory

@pytest.fixture
def related_project(db):
    def factory(**kwargs):
        kwargs.setdefault("name", fake.company())
        # same for other fields
        return RelatedStatistical.on_site.create(**kwargs)
    return factory

@pytest.fixture
def theme_project(db):
    def factory(**kwargs):
        kwargs.setdefault("name_theme_project", fake.company())
        # same for other fields
        return ThemeProject.on_site.create(**kwargs)
    return factory

@pytest.fixture
def state_project(db):
    def factory(**kwargs):
        kwargs.setdefault("state_project", fake.company())
        # same for other fields
        return StateProject.on_site.create(**kwargs)
    return factory

@pytest.fixture
def functionary_project(db):
    def factory(**kwargs):
        email = fake.email()
        functionary = Functionary.objects.create(
                user = User.objects.create_user(
                    first_name = fake.first_name(),
                    last_name = fake.last_name(),
                    password="Ariadna00$",
                    username=email,
                    email=email,
                    is_staff=False,
                    is_active=True,
                    ),
            )
        return functionary
    return factory

@pytest.fixture
def project_factory(db, tags_project, entity_factory, category_project, related_project, theme_project, state_project, functionary_project, inventory_factory):
    def factory(**kwargs):
        tags= tags_project()
        print("tags", tags.name_tag_project)
        provider = entity_factory()
        inventory = inventory_factory()
        
        #print("tag", tags.id)
        kwargs.setdefault("name", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("objetive_project", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("category_project", category_project())
        kwargs.setdefault("area_in_charge", fake.paragraph(nb_sentences=1))
        kwargs.setdefault("functionary_project", functionary_project())
        kwargs.setdefault("related_statistical_research", fake.company())
        kwargs.setdefault("related_statistical", related_project())
        kwargs.setdefault("theme_project", theme_project())
        kwargs.setdefault("state_project", state_project())

        # same for other fields
        project = Project.on_site.create(**kwargs)
        project.tag_project.add(tags)
        project.provider_any_project.add(provider)
        project.rraa_asociate.add(inventory)
        return project
    return factory

@pytest.mark.django_db
def test_project_factory(db, project_factory):
    project = project_factory()
    assert project.id == 1