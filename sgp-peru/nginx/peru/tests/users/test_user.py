#from django.test import TestCase
from users.models import User, Provider, Unit_Central, Functionary
import pytest
from faker import Faker

fake = Faker()

@pytest.fixture
def user_global_creation():
    email = fake.email()
    return User(            
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            password="Ariadna00$",
            username=email,
            email=email
        )

@pytest.mark.django_db
def test_common_user_creation(user_global_creation):
    user_global_creation.is_staff=False
    user_global_creation.is_active=True
    user_global_creation.save()
    assert user_global_creation.is_staff ==False
    assert user_global_creation.is_active ==True


@pytest.mark.django_db
def test_superuser_creation(user_global_creation):
    user_global_creation.is_staff=True
    user_global_creation.is_active=True
    user_global_creation.is_superuser=True
    user_global_creation.save()
    assert user_global_creation.is_superuser == True
    assert user_global_creation.username == user_global_creation.email

@pytest.mark.django_db
def test_provider_creation():  
    email = fake.email()  
    provider = Provider.objects.create(
            document_type="CC",
            identification_number="1059785463",
            user = User.objects.create_user(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                password="Ariadna00$",
                username=email,
                email=email,
                is_staff=False,
                is_active=True,
                ),
            valid_data=True,
            hash=True
    )
    assert provider.id == 1
    assert provider.user.email == email

@pytest.mark.django_db
def test_functionary_creation():
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
    assert functionary.id ==1

@pytest.mark.django_db
def test_unit_creation():
    email = fake.email()
    functionary = Unit_Central.objects.create(
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
    assert functionary.id ==1

@pytest.mark.django_db
def test_user_creation_fail():
    with pytest.raises(Exception):
        User.objects.create_user(
            password="Ariadna00$",
            is_staff=False,
        )
        


