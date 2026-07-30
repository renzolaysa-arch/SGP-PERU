from django.test import RequestFactory, TestCase
from django.test.client import Client
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User, Group
from users.models import Functionary, Provider
from datetime import datetime, timedelta
from demand.models import *
from projects.models import *
from inventory.models import *
from providers.models import *
import pytest
import random
fake = Faker()


class InventoryTest(TestCase):
    def setUp(self):
        # Funcionary
        email = "test_functionary@test.com"
        self.client = Client()
        self.functionary = Functionary.objects.create(
            user=User.objects.create_user(
                password="Ariadna00$",
                username=email,
                email=email,
                is_staff=False,
                is_active=True,
            ),
        )
        self.group = Group.objects.create(name='Funcionario')
        self.functionary.user.groups.add(self.group)

        # Project
        self.tags_project = TagsProject.on_site.create(name_tag_project=fake.company(
        ), type_color_choice=random.choice(['red', 'blue', 'orange', 'gray']))
        self.category_project = CategoryProject.on_site.create(
            name_category_project=fake.company())
        self.related_statistical = RelatedStatistical.on_site.create(
            name=fake.company())
        self.theme_project = ThemeProject.on_site.create(
            name_theme_project=fake.company())
        self.state_project = StateProject.on_site.create(
            state_project=fake.company())
        self.project = Project.on_site.create(
            name=fake.paragraph(nb_sentences=1),
            objetive_project=fake.paragraph(nb_sentences=1),
            category_project=self.category_project,
            area_in_charge=fake.paragraph(nb_sentences=1),
            functionary_project=self.functionary,
            related_statistical_research=fake.company(),
            related_statistical=self.related_statistical,
            theme_project=self.theme_project,
            state_project=self.state_project,
        )

        # Provider
        self.provider_sector = ProviderSector.objects.create(
            name=fake.company())
        self.provider_type = ProviderType.objects.create(name=fake.company())
        self.provider_status = ProviderStatus.objects.create(
            name=fake.company())
        self.provider_entity = ProviderEntity.on_site.create(
            name=fake.first_name(),
            identification_number=random.randint(1000, 1050),
            description=fake.last_name(),
            sector=self.provider_sector,
            type=self.provider_type,
            image=fake.file_extension(category='image'),
            domain=fake.company(),
            status=self.provider_status
        )

        # Provider
        email = "test_provider@test.com"
        self.client = Client()
        self.provider = Provider.objects.create(
            user=User.objects.create_user(
                password="Ariadna00$",
                username=email,
                email=email,
                is_staff=False,
                is_active=True,
            ),
            entity_provider=self.provider_entity,
            document_type='CC',
            identification_number="00000000",
            valid_data=True
        )
        self.group = Group.objects.create(name='Proveedor')
        self.provider.user.groups.add(self.group)

        # Inventory
        self.inventory_theme = InventoryTheme.on_site.create(
            name_theme_inventory=fake.company())
        self.inventory_thematic = InventoryThematic.on_site.create(
            name_thematic_inventory=fake.company())
        self.inventory_status = InventoryStatus.on_site.create(
            name=fake.company())
        self.type_format_sampledata = TypeFormatSampleData.on_site.create(
            type_format='pdf')
        self.transfer_medium_sampledata = TransferMediumSampleData.on_site.create(
            transfer_medium=fake.company())
        self.tags_sampledata = TagsSampleData.on_site.create(
            tags_sample_data=fake.company())
        self.variables_sampledata = VariablesSampleData.on_site.create(
            variables_sample_data=fake.company())
        self.inventory = Inventory.on_site.create(
            title=fake.paragraph(nb_sentences=1),
            objective=fake.paragraph(5),
            inventory_theme_asociate=self.inventory_theme,
            inventory_thematic_asociate=self.inventory_thematic,
            use_laws_decrees=random.choice(['C.P', 'L', 'D.N']),
            document_choice=random.choice(['M.D', 'D.D', 'D.S']),
            nomenclature_choice=random.choice(['Si', 'No']),
            method_collections_choice=random.choice(['F.F', 'F.E', 'D.C']),
            frequency_choice=random.choice(['F.F', 'F.E', 'D.C']),
            processing_choice=random.choice(['E', 'A', 'R']),
            record_choice=random.choice(['S', 'N']),
            dependence_name=fake.bs(),
            director_name=fake.first_name(),
            security_choice=random.choice(
                ['Backups', 'Aislamiento del servidor', 'Utilización de perfiles']),
            information_stored_choice=random.choice(['Si', 'No']),
            information_choice=random.choice(
                ['Anual', 'Semestral', 'Bimensual', 'Trimestral']),
            type_format_data_asociate=self.type_format_sampledata,
            file_example_sample_data=fake.file_name(
                extension=self.type_format_sampledata),
            transfer_medium_data_asociate=self.transfer_medium_sampledata,
            entity_provider=self.provider_entity
        )

        # Demand
        today = datetime.today()
        end_date = today + timedelta(days=30)
        self.demands_categories = DemandsCategories.on_site.create(
            name='Category')
        self.demands_status = DemandsStatus.on_site.create(name='Activo')
        self.demands_theme = DemandsTheme.on_site.create(name=fake.job())
        self.key_words = KeyWords.on_site.create(name=fake.job())
        self.topic = Topic.on_site.create(name=fake.job())
        self.demand = Demands.on_site.create(
            functionary=self.functionary,
            inventory=self.inventory,
            project=self.project,
            title=fake.job(),
            description=fake.paragraph(nb_sentences=1),
            use=random.choice(
                ['Realizar validación', 'Conformar un registro base', 'Estadística experimental']),
            use_other=fake.company(),
            time=random.choice(['1 mes', '2 meses', '3 meses', '11 meses']),
            product=fake.paragraph(nb_sentences=1),
            status=self.demands_status,
            category=self.demands_categories,
            theme=self.demands_theme,
            provider_entity=self.provider_entity,
            topic=self.topic,
            finish_date=fake.date_between_dates(today, end_date),
            file_demand=fake.file_name(extension='.pdf'),
            process='re',
            type='ex',
        )
        self.note = Note.on_site.create(
            demand=self.demand,
            commentary=fake.paragraph(nb_sentences=1),
            functionary=self.functionary,
        )

        # Reception
        date_demand_validation = datetime.today()
        date_verification_completeness = date_demand_validation + \
            timedelta(days=15)
        date_tentative_presentation = date_demand_validation + \
            timedelta(days=20)
        date_demand_presentation = date_demand_validation + timedelta(days=30)
        date_demand_finalized = date_demand_validation + timedelta(days=40)
        self.reception = Reception.on_site.create(
            demand=self.demand,
            date_demand_validation=date_demand_validation,
            date_verification_completeness=date_verification_completeness,
            date_demand_notification=date_verification_completeness,
            date_tentative_presentation=date_tentative_presentation,
            date_demand_presentation=date_demand_presentation,
            status_demand_validation=self.demands_status,
            status_demand_notification=self.demands_status,
            demand_subprocess=random.choice(
                ['demand-validation', 'verification-completeness', 'demand-notification', 'technical-committee-presentation']),
            demand_assessment=random.choice(['1', '2', '3', '4']),
            comment_revision=fake.paragraph(nb_sentences=1),
            punctual_need=random.choice(['Si', 'No']),
            full_justification=random.choice(['Si', 'No']),
            approval_instance=random.choice(['Si', 'No']),
            date_demand_finalized=date_demand_finalized,
            comment_finalized=fake.paragraph(nb_sentences=1),
        )

    @pytest.mark.django_db
    def test_list_inventory(self):
        self.client.login(username="test_functionary@test.com",
                          password='Ariadna00$')
        url = reverse("inventory:inventory_list")
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)
        print(response.context['filter'])
        print(response.context['list_custom'])
        print(response.context['inventory_page_obj'])
        print(response.context['inventory_total'])
        print(response.context['inventory_page'])
        print(response.context['form_order_by'])

    @pytest.mark.django_db
    def test_detail_inventory(self):
        self.client.login(username="test_functionary@test.com",
                          password='Ariadna00$')
        url = reverse("inventory:detail_inventory", kwargs={'id_inventory': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)
        print(response.context['inventory'])
        print(response.context['comments'])
        print(response.context['owner'])

    @pytest.mark.django_db
    def test_detail_inventory_not_found(self):
        self.client.login(username="test_functionary@test.com",
                          password='Ariadna00$')
        url = reverse("inventory:detail_inventory",
                      kwargs={'id_inventory': 10})
        response = self.client.get(url)
        assert response.status_code == 404
        print("url", url, " :", response)

    @pytest.mark.django_db
    def test_create_comment_inventory(self):
        print("Comentarios creados:", CommentInventory.on_site.all().count())
        print("Notificaciones creadas:", Notification.on_site.all().count())
        self.client.login(username="test_functionary@test.com",
                          password='Ariadna00$')
        url = reverse("inventory:detail_inventory", kwargs={'id_inventory': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)
        assert "form" in response.context
        response = self.client.post(reverse("inventory:detail_inventory", kwargs={'id_inventory': 1}), data={
            "comment_text": fake.paragraph(nb_sentences=1),
            "form_id": "comment_inventory",
        }, kwargs={})

        assert response.status_code == 302
        print("url", url, " :", response)
        print("Comentarios creados:", CommentInventory.on_site.all().count())
        print("Notificaciones creadas:", Notification.on_site.all().count())

    @pytest.mark.django_db
    def test_edit_inventory(self):
        inventory = Inventory.on_site.get(pk=1)
        print("title: ", inventory.title)
        print("Notificaciones creadas:", Notification.on_site.all().count())
        self.client.login(username="test_provider@test.com",
                          password='Ariadna00$')
        url = reverse("inventory:edit_inventory", kwargs={'id': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)
        assert "form" in response.context
        response = self.client.post(reverse("inventory:edit_inventory", kwargs={'id': 1}), data={
            "title": "Nuevo titulo",
            "date_start_collection": "2021-01-19",
            "date_finish_collection": "2022-11-30",
            "method_document": "N",
            "nomenclature_choice": "N",
            "method_collections_choice": "Registro de datos por parte del funcionario (entrevistas)",
            "defined_form": "S",
            "frequency_choice": "A",
            "geographic_coverages_type": "Nacional",
            "organism_document_choice": "S",
            "security_choice": "A.S",
            "information_stored_choice": "S",
            "information_choice": "A",
            "centralized": "Centralizada",
            "external_user": "S",
            "create_participation": "S",
            "main_choice": "P.E",
            "statistics_user": 'S',
            "requierements_choice": 'S',
            "form_id": "createRraaForm",
        }, kwargs={})
        inventory = Inventory.on_site.get(pk=1)
        print("title: ", inventory.title)
        print("Notificaciones creadas:", Notification.on_site.all().count())
