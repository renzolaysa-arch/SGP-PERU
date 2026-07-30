from django.test import RequestFactory, TestCase
from django.test.client import Client
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User, Group
from users.models import Functionary
from datetime import datetime, timedelta
from demand.models import *
from projects.models import *
from inventory.models import *
from providers.models import *
import pytest
import random
fake = Faker()


class DemandTest(TestCase):
    def setUp(self):
        email = "test_views_cdi@test.com"
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
    def test_create_demand(self):
        print("Solcictudes creadas:", Demands.on_site.all().count())
        print("Notificaciones creadas:", Notification.on_site.all().count())
        print("MP Recepcion creadas:", Reception.on_site.all().count())
        self.client.login(username="test_views_cdi@test.com",
                          password='Ariadna00$')
        url = reverse("demand:demand_create")
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)
        assert "form" in response.context
        response = self.client.post(reverse("demand:demand_create"), data={
            "title": fake.job(),
            "inventory": 1,
            "project": 1,
            "description": fake.paragraph(nb_sentences=1),
            "use": 'ca',
            "use_other": fake.company(),
            "time": '2',
            "product": fake.paragraph(nb_sentences=1),
            "category": 1,
            "status": 1,
            "theme": 1,
            "topic": 1,
            "file_demand": fake.file_name(extension='.pdf'),
            "functionary": 1,
            "form_id": "demandCreateForm",
        }, kwargs={})

        assert response.status_code == 302
        print("url", url, " :", response)
        print("Solcictudes creadas:", Demands.on_site.all().count())
        print("Notificaciones creadas:", Notification.on_site.all().count())
        print("MP Recepcion creadas:", Reception.on_site.all().count())
        
    @pytest.mark.django_db
    def test_create_note_demand(self):
        print("Notas creadas:", Note.on_site.all().count())
        self.client.login(username="test_views_cdi@test.com",
                          password='Ariadna00$')
        url = reverse("demand:demand_detail", kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)
        assert "form" in response.context
        response = self.client.post(reverse("demand:demand_detail", kwargs={'id_demand': 1}), data={
            "demand": 1,
            "commentary": fake.paragraph(nb_sentences=1),
            "functionary": 1,
            "form_id": "noteDemands",
        }, kwargs={})

        assert response.status_code == 302
        print("url", url, " :", response)
        print("Notas creadas:", Note.on_site.all().count())

    @pytest.mark.django_db
    def test_list_demand(self):
        self.client.login(username="test_views_cdi@test.com",
                          password='Ariadna00$')
        url = reverse("demand:demand_list")
        response = self.client.get(url)
        assert response.status_code == 200
        print("url", url, " :", response)
        print(response.context['demand_custom'])
        print(response.context['demand_page_obj'])
        print(response.context['demand_total'])
        print(response.context['demand_page'])

    @pytest.mark.django_db
    def test_detail_demand(self):
        self.client.login(username="test_views_cdi@test.com",
                          password='Ariadna00$')
        url = reverse("demand:demand_detail", kwargs={'id_demand': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        print("Notas:", Note.on_site.filter(demand=1).count())
        print("url", url, " :", response)
        print(response.context['demand'])
        print(response.context['process_board'])

    @pytest.mark.django_db
    def test_detail_demand_not_found(self):
        self.client.login(username="test_views_cdi@test.com",
                          password='Ariadna00$')
        url = reverse("demand:demand_detail", kwargs={'id_demand': 10})
        response = self.client.get(url)
        assert response.status_code == 404
        print("url", url, " :", response)
